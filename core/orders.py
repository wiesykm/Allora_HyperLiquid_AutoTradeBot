from hyperliquid.info import Info
import json
from utils.helpers import round_size, round_price


class OrderManager:
    def __init__(self, exchange, vault_address, allowed_amount_per_trade, leverage, info: Info):
        self.exchange = exchange
        self.info = info
        self.vault_address = vault_address
        self.allowed_amount_per_trade = allowed_amount_per_trade
        self.leverage = leverage

    def create_order(self, coin, is_buy, size, price, order_type, reduce_only=False):
        """
        Places a buy or sell order with size and price rounding.
        """
        print(f"Placing {'Buy' if is_buy else 'Sell'} order for {size} {coin} at {price}")
        return self.exchange.order(coin, is_buy, size, price, order_type, reduce_only=reduce_only)

    def cancel_order(self, coin, oid):
        print(f"Cancelling order {oid} for {coin}")
        return self.exchange.cancel(coin, oid)

    def update_leverage(self, coin, leverage, cross_margin=True):
        mode = "cross margin" if cross_margin else "isolated margin"
        print(f"Updating leverage for {coin} to {leverage}x ({mode})")
        return self.exchange.update_leverage(leverage, coin, cross_margin)

    def market_open(self, coin, is_buy, size, leverage=5, cross_margin=True):
        self.update_leverage(coin, leverage, cross_margin=cross_margin)
        print(f"Market {'Buy' if is_buy else 'Sell'} order for {size} {coin}")
        return self.exchange.market_open(coin, is_buy, size)

    def market_close(self, coin):
        print(f"Closing position for {coin}")
        return self.exchange.market_close(coin)

    def list_open_positions(self):
        print("Fetching open positions...")
        response = self.info.user_state(self.vault_address)
        asset_positions = response.get("assetPositions", [])
        if not asset_positions:
            return None

        active_positions = []
        for position in asset_positions:
            pos_details = position.get("position", {})
            if pos_details:
                active_positions.append(pos_details.get("coin"))

        return active_positions if active_positions else None

    def get_open_positions(self):
        print("Fetching open positions...")
        response = self.info.user_state(self.vault_address)
        asset_positions = response.get("assetPositions", [])
        if not asset_positions:
            return None

        active_positions = []
        for position in asset_positions:
            pos_details = position.get("position", {})
            if pos_details:
                active_positions.append(pos_details)

        return active_positions if active_positions else None

    def get_wallet_summary(self, mode="cross"):
        print("Fetching wallet summary...")
        response = self.info.user_state(self.vault_address)
        summary = response.get("crossMarginSummary", {}) if mode == "cross" else response.get("marginSummary", {})
        return {
            "account_value": summary.get("accountValue"),
            "total_position_value": summary.get("totalNtlPos"),
            "total_usd_balance": summary.get("totalRawUsd"),
            "margin_used": summary.get("totalMarginUsed"),
        }

    def create_trade_order(self, coin, is_buy, profit_limit_order=0, profit_target=5,
                           loss_target=3):
        leverage = self.leverage
        allowed_amount_per_trade = self.allowed_amount_per_trade
        print("Checking conditions for trade order...")
        coin = str(coin).upper()

        # Fetch metadata for available tokens
        meta = self.info.meta_and_asset_ctxs()

        # Parse universe and additional data
        universe_data = meta[0]["universe"]
        additional_data = meta[1] if len(meta) > 1 else []

        # Find the coin data from universe_data
        coin_index = next((index for index, asset in enumerate(universe_data) if asset["name"] == coin), None)
        if coin_index is None:
            print(f"Oops... This coin is not supported by HyperLiquid. Coin: {coin}")
            return None

        # Merge data using the same index in additional_data
        coin_data = universe_data[coin_index]
        if coin_index < len(additional_data):
            coin_data.update(additional_data[coin_index])

        # Extract required parameters from the merged data
        max_leverage = coin_data.get("maxLeverage", leverage)
        sz_decimals = coin_data.get("szDecimals", 2)

        # Adjust leverage if it exceeds the allowed max leverage
        if leverage > max_leverage:
            print(f"Adjusting leverage to max allowed value for {coin}: {max_leverage}")
            leverage = max_leverage

        # Fetch wallet summary and check balance
        wallet = self.get_wallet_summary(mode="cross")
        print(wallet)
        available_usd = float(wallet.get("total_usd_balance", 0))
        if available_usd < 10:
            print("Insufficient funds.")
            return None

        # Calculate effective trading amount based on leverage
        effective_trade_amount = min(allowed_amount_per_trade, available_usd * leverage)

        # Check for existing open positions for the given coin
        open_positions = self.list_open_positions()
        if open_positions and coin in open_positions:
            print(f"Order skipped: An open position already exists for {coin}.")
            return None

        # Fetch the current price
        current_price = coin_data.get("oraclePx")
        if current_price is None:
            print(f"We are unable to fetch the current price of the token.")
            return None
        current_price = float(current_price)

        # Calculate position size and ensure it does not exceed allowed_amount_per_trade
        size = effective_trade_amount / current_price

        # Ensure position size respects the allowed trade limit after applying leverage
        max_size_based_on_allowed = allowed_amount_per_trade / current_price
        size = min(size, max_size_based_on_allowed)

        # Round size based on szDecimals
        size = round_size(size, sz_decimals)

        # Place a market order
        market_order_result = self.market_open(coin, is_buy, size, leverage=leverage)
        print(market_order_result)

        if market_order_result.get("status") != "ok":
            print(f"Market order for {coin} failed.")
            return None

        try:
            filled_order = market_order_result["response"]["data"]["statuses"][0]["filled"]
            order_id = filled_order.get("oid", None)
            executed_price = float(filled_order.get("avgPx", current_price))
            print(f"Order executed successfully: ID {order_id}, Price {executed_price:.2f}")
        except (KeyError, IndexError, ValueError) as e:
            print(f"Failed to extract order details: {e}")
            return None

        # Calculate profit and loss target prices based on order type
        if is_buy:
            profit_price = executed_price * (1 + profit_target / 100)
            loss_price = executed_price * (1 - loss_target / 100)
        else:
            profit_price = executed_price * (1 - profit_target / 100)
            loss_price = executed_price * (1 + loss_target / 100)

        # Adjust profit and loss prices to proper rounding
        profit_price = round_price(profit_price)
        loss_price = round_price(loss_price)

        # Create stop-loss order
        stop_order_type = {"trigger": {"triggerPx": loss_price, "isMarket": True, "tpsl": "sl"}}
        stop_loss_order_result = self.create_order(
            coin=coin,
            is_buy=not is_buy,
            size=size,
            price=loss_price,
            order_type=stop_order_type,
            reduce_only=True
        )

        # Create take-profit order
        tp_order_type = {"trigger": {"triggerPx": profit_price, "isMarket": True, "tpsl": "tp"}}
        profit_limit_order_result = self.create_order(
            coin=coin,
            is_buy=not is_buy,
            size=size,
            price=profit_price,
            order_type=tp_order_type,
            reduce_only=True
        )

        print("Limit Orders Created:")
        print(f"Profit Limit Order: {profit_limit_order_result}")
        print(f"Stop-Loss Order: {stop_loss_order_result}")

        return market_order_result

    def get_price(self, coin):
        coin = str(coin).upper()
        # Fetch metadata for available tokens
        meta = self.info.meta_and_asset_ctxs()

        # Parse universe and additional data
        universe_data = meta[0]["universe"]
        additional_data = meta[1] if len(meta) > 1 else []

        # Find the coin data from universe_data
        coin_index = next((index for index, asset in enumerate(universe_data) if asset["name"] == coin), None)
        if coin_index is None:
            print(f"Oops... This coin is not supported by HyperLiquid. Coin: {coin}")
            return None

        # Merge data using the same index in additional_data
        coin_data = universe_data[coin_index]
        if coin_index < len(additional_data):
            coin_data.update(additional_data[coin_index])

        if coin_data:
            return coin_data["oraclePx"]

        return None

    def get_open_orders(self):
        return self.info.open_orders(self.vault_address)

    def modify_open_order(self, name, is_buy, sz, order_type,   order_id, limit_price):
        print("OID->",order_id)
        return self.exchange.modify_order(oid=order_id,
                                          limit_px=limit_price,
                                          name=name,
                                          sz=sz,
                                          is_buy=is_buy,
                                          order_type=order_type)

