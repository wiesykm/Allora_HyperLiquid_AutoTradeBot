from utils.setup import setup
from core.orders import OrderManager
from utils.helpers import display_leverage_info
from hyperliquid.utils import constants
from hyperliquid.exchange import Exchange
from allora.allora_mind import AlloraMind


def main():
    base_url = constants.MAINNET_API_URL
    (address, info, exchange, vault, allora_upshot_key, check_for_trades, price_gap,
     allowed_amount_per_trade, max_leverage, allora_topics) = setup(base_url)
    print(address)

    manager = OrderManager(exchange, vault, allowed_amount_per_trade, max_leverage, info)
    allora_mind = AlloraMind(manager, allora_upshot_key, threshold=price_gap)
    allora_mind.set_topic_ids(allora_topics)
    allora_mind.start_allora_trade_bot(interval=check_for_trades)


if __name__ == "__main__":
    main()
