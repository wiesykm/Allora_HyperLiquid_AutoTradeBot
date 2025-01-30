# 🚀 AlloraNetwork, HyperLiquid & DeepSeek AI Auto Trade Bot

Welcome to the **AlloraNetwork HyperLiquid Auto Trading Bot**! This project leverages **[AlloraNetwork](https://www.allora.network/) inference** to enable **automatic trading** on the decentralized exchange [HyperLiquid](https://hyperliquid.gitbook.io/hyperliquid-docs). The bot uses AI-driven predictions from AlloraNetwork, combined with **DeepSeek AI trade validation**, to make informed trading decisions based on customizable strategies. 📈🤖

By default, the bot uses a **volatility-based strategy**, but you can define your own custom strategy to suit your trading preferences.

---

## 🛠️ Prerequisites

Before you get started, make sure you have the following:

1. **HyperLiquid Account**:
   - Create an account on [HyperLiquid](https://hyperliquid.gitbook.io/hyperliquid-docs).
   - Set up your **Vault** for trading.
2. **API and Wallet Setup**:
   - Go to **More Options** > **API** in HyperLiquid.
   - Generate your **Private Key** and **Wallet Address**.
   - 🔒 Record this information securely.
3. **Allora API Key**:
   - Create an API key from the [Upshot Developer Portal](https://developer.upshot.xyz/).
4. **DeepSeek API Key**:
   - Obtain your [DeepSeek API](https://deepseek.com/) key for AI-powered trade validation.

<img src="https://github.com/HarbhagwanDhaliwal/Allora_HyperLiquid_AutoTradeBot/blob/5f815d3fb8de1fc98c5c49f6a041dedab476ce07/hyper_api.jpeg" alt="HyperLiquid API Setup" width="500"/>

---

## 🚀 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/HarbhagwanDhaliwal/Allora_HyperLiquid_AutoTradeBot.git
   ```
2. **Create a Virtual Environment and Activate It**:
   ```bash
   python3 -m venv venv && source venv/bin/activate
   ```
3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure the Bot**:
   - Rename the `.env.example` file to `.env`:
     ```bash
     mv .env.example .env
     ```
   - Open the `.env` file and update the following fields with your details:
     ```bash
     # HyperLiquid Credentials
     HL_SECRET_KEY=      # Your HyperLiquid secret key
     HL_ACCOUNT_ADDRESS= # Your HyperLiquid account address
     HL_VAULT=           # Your HyperLiquid vault identifier

     # Set to True to run the bot on the mainnet, False for testnet
     MAINNET=False

     # DeepSeek API
     DEEPSEEK_API_KEY=   # Your DeepSeek API key

     # Allora API
     ALLORA_UPSHOT_KEY=  # Your Allora Upshot API key

     # Trading Parameters
     PRICE_GAP=0.25
     ALLOWED_AMOUNT_PER_TRADE=10
     MAX_LEVERAGE=1
     CHECK_FOR_TRADES=300
     VOLATILITY_THRESHOLD=0.02

     # Database
     DB_PATH=trading_logs.db

     # Topic IDs
     BTC_TOPIC_ID=14
     ETH_TOPIC_ID=13
     ```
   - Save the file by pressing `CTRL+X`, then `Y`, and `Enter`. 💾
5. **Running the Bot**:
   ```bash
   python3 main.py
   ```

---

## ⚙️ Configuration Details

- **PRICE_GAP**: The percentage difference between the Allora prediction and the current price to trigger a trade. Example: `0.25` means a 0.25% gap is required to initiate a trade.
- **ALLOWED_AMOUNT_PER_TRADE**: 💵 The maximum amount (in USD) to open a trade. Note: Total trade value will include leverage.
- **MAX_LEVERAGE**: Leverage multiplier for trades. Example: `1` means 1x leverage.
- **CHECK_FOR_TRADES**: Interval (in seconds) for the bot to check open positions and trading opportunities.
- **VOLATILITY_THRESHOLD**: The volatility threshold to consider before executing a trade.
- **BTC_TOPIC_ID** and **ETH_TOPIC_ID**: Map tradable tokens (e.g., BTC, ETH) to their Allora prediction topic IDs. Ensure tokens match HyperLiquid symbols.

---

## 🧠 Default Volatility Strategy

By default, the bot uses a **volatility-based strategy** to make trading decisions. This strategy evaluates market conditions and Allora's predictions to determine whether to enter or exit trades. The default strategy is implemented in the `volatility_strategy` module.

---

## 🛠️ Custom Strategy

You can define your own custom trading strategy by modifying the `custom_strategy` function in `strategy/custom_strategy.py`. This function allows you to incorporate your own logic and override the default volatility strategy.

### Custom Strategy Function
```python
def custom_strategy(token, price=None, allora_signal=None, allora_prediction=None):
    """
    Modified custom strategy that trades counter to Allora's predictions
    during high volatility periods.
    """
    if price is None or allora_signal is None or allora_prediction is None:
        return None

    # Use the default volatility strategy or implement your own logic here
    return volatility_strategy.execute(token, price, allora_signal, allora_prediction)
```

### How to Use
1. Open `strategy/custom_strategy.py`.
2. Modify the `custom_strategy` function to implement your own logic.

---

## 🤖 DeepSeek AI Trade Reviewer

The bot integrates **DeepSeek AI** as an additional layer of trade validation. This AI reviewer analyzes each potential trade before execution, considering multiple factors:

### How It Works

1. **Trade Analysis**: Before executing any trade, DeepSeek AI reviews:
   - Current price vs Allora prediction
   - Market volatility
   - Trade direction (BUY/SELL)
   - Historical performance in similar conditions

2. **Decision Metrics**:
   - `approval` (true/false): Whether the trade should proceed
   - `confidence` (0-100): Confidence level in the decision
   - `reasoning`: Detailed explanation of the decision
   - `risk_score` (1-10): Risk assessment of the trade

3. **Trade Requirements**:
   - Minimum 70% confidence score
   - DeepSeek approval must be true
   - Risk score is logged for analysis

### Example Output
```
Trade Review by DeepSeek AI:
  Confidence: 85%
  Reasoning: "Strong directional alignment between Allora prediction and current market momentum. 
             Volatility within acceptable range. Recent similar setups showed 70% success rate."
  Risk Score: 3/10
```

### Benefits
- 🎯 Reduced false positives
- 📊 Enhanced risk management
- 🧠 AI-powered trade validation
- 📝 Detailed trade reasoning

---

## 🔄 Example Workflow

1. **Allora Prediction**: Indicates a "BUY" signal for BTC. 📊
2. **Custom Strategy**: Evaluates the trade based on your custom logic or the default volatility strategy.
3. **DeepSeek AI Review**:
   - Analyzes the trade for risk, confidence, and reasoning.
   - Approves the trade if confidence is above 70% and risk is acceptable.
4. **Bot Action**:
   - If **Allora**, **Custom Strategy**, and **DeepSeek AI** all agree, the bot executes the trade. ✅
   - If any of the three components disagree, the bot does not execute the trade. ❌

---

## 🔧 Advanced Usage

You can combine the bot with other strategies or modify it further. Just import your custom strategy:
```python
from strategy.custom_strategy import custom_strategy
```

---

## 💬 Support

For any questions, feel free to contact me via GitHub. Don’t forget to give this repository a ⭐ if you find it helpful!

---

## 🤝 Contribute

This project is open source, and contributions are welcome! If you have ideas for improvements, feel free to fork the repository and submit a pull request. Together, we can make this bot even better. 🌟

---

Happy Trading! 🚀📈
