import os
import json
import eth_account
from hyperliquid.info import Info
from core.exchange import ExchangeWrapper
from hyperliquid.exchange import Exchange
from utils.helpers import convert_percentage_to_decimal


def setup(base_url):
    config_path = os.path.join(os.path.dirname(__file__), "../config/config.json")
    with open(config_path) as f:
        config = json.load(f)

    account = eth_account.Account.from_key(config["secret_key"])
    address = config["account_address"] or account.address
    vault = config["vault"]
    allora_upshot_key = config["allora_upshot_key"]
    allora_topics = config["allora_topics"]
    check_for_trades = config["check_for_trades"]
    allowed_amount_per_trade = config["allowed_amount_per_trade"]
    max_leverage = config["max_leverage"]
    price_gap = config["price_gap"]
    price_gap = convert_percentage_to_decimal(price_gap)
    print(f"Running with vault: {vault}")

    info = Info(base_url, skip_ws=True)
    exchange = Exchange(account, base_url, account_address=address, vault_address=vault)
    return (address, info, exchange, vault, allora_upshot_key, check_for_trades,
            price_gap, allowed_amount_per_trade, max_leverage, allora_topics)

