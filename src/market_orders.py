#!/usr/bin/env python3
"""
Market Orders CLI Module for Binance Futures Testnet
Usage: python src/market_orders.py BTCUSDT BUY 0.01
"""

import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binance import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from config import Config
from logger import trading_logger
from utils import TradingUtils, ValidationError


class MarketOrderBot:
    """Market order implementation for Binance Futures Testnet"""

    def __init__(self):
        """Initialize the market order bot"""
        try:
            # Validate credentials
            Config.validate_credentials()

            # ✅ CORRECT Binance client initialization
            self.client = Client(
                Config.API_KEY,
                Config.API_SECRET,
                testnet=True                # 🔥 MANDATORY
            )

            # ✅ FORCE Futures Testnet endpoint
            self.client.FUTURES_URL = Config.FUTURES_TESTNET_URL

            trading_logger.log_info(
                "Market Order Bot initialized for Binance Futures Testnet"
            )

        except Exception as e:
            TradingUtils.print_error_and_exit(
                f"Failed to initialize Futures client: {e}"
            )

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """Place a market order on Binance Futures Testnet"""
        try:
            params = {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": quantity,
            }

            trading_logger.log_api_request(
                "POST", "/fapi/v1/order", params
            )

            # ✅ Futures order endpoint
            order = self.client.futures_create_order(**params)

            trading_logger.log_api_response(
                "/fapi/v1/order", order
            )

            trading_logger.log_order_placed(
                "MARKET", symbol, side, quantity, order
            )

            return order

        except BinanceAPIException as e:
            trading_logger.log_error(
                e, f"Market order placement - {symbol} {side}"
            )
            raise ValueError(f"Market order failed: {e.message}")

        except BinanceRequestException as e:
            trading_logger.log_error(
                e, f"Market order placement - {symbol} {side}"
            )
            raise ConnectionError(
                f"Network error during market order: {e}"
            )


def main():
    """CLI entry point"""
    if len(sys.argv) != 4:
        TradingUtils.print_usage_and_exit(
            "market_orders.py", "<SYMBOL> <SIDE> <QUANTITY>"
        )

    _, symbol, side, quantity = sys.argv

    try:
        validated_symbol = TradingUtils.validate_symbol(symbol)
        validated_side = TradingUtils.validate_side(side)
        validated_quantity = TradingUtils.validate_quantity(quantity)

        print(f"\n🚀 Placing MARKET {validated_side} order...")
        print(f"   Symbol: {validated_symbol}")
        print(f"   Quantity: {validated_quantity}")

        bot = MarketOrderBot()
        order_response = bot.place_market_order(
            validated_symbol,
            validated_side,
            validated_quantity
        )

        TradingUtils.print_order_result("MARKET", order_response)

    except ValidationError as e:
        TradingUtils.print_error_and_exit(f"Validation Error: {e}")
    except ValueError as e:
        TradingUtils.print_error_and_exit(f"Order Error: {e}")
    except Exception as e:
        TradingUtils.print_error_and_exit(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
