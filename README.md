# 🚀 AlloraNetwork HyperLiquid Auto Trading Bot

<p align="center">
  <img src="https://github.com/HarbhagwanDhaliwal/Allora_HyperLiquid_AutoTradeBot/blob/ef2285971f1bdeaec53c46f86e9b13c3ccf653b3/AlloraLogo.jpeg" alt="Allora Logo" width="300">
</p>

This project implements the **[AlloraNetwork](https://www.allora.network/) inference** to enable **automatic trading** on the decentralized exchange [HyperLiquid](https://hyperliquid.gitbook.io/hyperliquid-docs). The bot uses AI-driven predictions from AlloraNetwork to make informed trading decisions based on customizable strategies. 📈🤖

## 🛠️ Prerequisites

1. **HyperLiquid Account**:
   - Create an account on HyperLiquid.
   - Set up your **Vault** for trading.
2. **API and Wallet Setup**:
   - Go to **More Options** > **API** in HyperLiquid.
   - Generate your **Private Key** and **Wallet Address**.
   - 🔒 Record this information securely.
3. **Allora API Key**:
   - Create an API key from [Upshot Developer Portal](https://developer.upshot.xyz/).

![HyperLiquid API Setup](#) <!-- Replace with an actual image link -->

## 🚀 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/HarbhagwanDhaliwal/Allora_HyperLiquid_AutoTradeBot.git
   ```

2. **Configure the Bot**:
   - Open the configuration file using `nano`:
     ```bash
     nano config/config.json
     ```
   - Update the following fields with your details:
     ```json
     {
         "secret_key": "Your Hyper Liquid Wallet Private Key",
         "account_address": "Your Hyper Liquid Wallet Address",
         "vault": "Your Vault Address on HyperLiquid",
         "allora_upshot_key": "Your Allora Upshot API Key",
         "allora_topics": {
             "BTC": 14,
             "ETH": 13
         },
         "price_gap": 0.25,
         "allowed_amount_per_trade": 500,
         "max_leverage": 5,
         "check_for_trades": 300
     }
     ```
   - Save the file by pressing `CTRL+X`, then `Y`, and `Enter`. 💾

## ⚙️ Configuration Details

- **price_gap**: The percentage difference between the Allora prediction and the current price to trigger a trade. Example: `0.25` means a 0.25% gap is required to initiate a trade.
- **allowed_amount_per_trade**: 💵 The maximum amount (in USD) to open a trade. Note: Total trade value will include leverage.
- **max_leverage**: Leverage multiplier for trades. Example: `5` means 5x leverage.
- **check_for_trades**: Interval (in seconds) for the bot to check open positions and trading opportunities.
- **allora_topics**: Map tradable tokens (e.g., BTC, ETH) to their Allora prediction topic IDs. Ensure tokens match HyperLiquid symbols.

## 🧠 Custom Strategy

You can integrate your custom trading strategy with the bot. Define your logic in the following function located in `strategy/custom_strategy.py`:

```python
def custom_strategy(token, price=None):
    """
    Function that takes 'token' and 'price' (optional, default None).
    Returns either 'BUY', 'SELL', 'HOLD', or None based on the logic.
    """
    # Default behavior is to return None (no decision)
    return None
```

### Example Workflow:
1. **Allora Prediction**: Indicates a "BUY" signal for BTC. 📊
2. **Custom Strategy**: Also returns "BUY" for BTC.
3. **Bot Action**: Opens a trade based on combined decisions. ✅

If there’s a conflict (e.g., Allora says "BUY," but your strategy says "HOLD"), the bot will not execute the trade. ❌

## 🔧 Advanced Usage

You can combine the bot with other strategies or modify it further. Just import your custom strategy:
```python
from strategy.custom_strategy import custom_strategy
```

## 💬 Support

For any questions, feel free to contact me via GitHub. Don’t forget to give this repository a ⭐ if you find it helpful!

## 🤝 Contribute

This project is open source, and contributions are welcome! If you have ideas for improvements, feel free to fork the repository and submit a pull request. Together, we can make this bot even better. 🌟

---
