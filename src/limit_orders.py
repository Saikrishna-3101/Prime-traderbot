#!/usr/bin/env python3
"""
Limit Orders CLI Module for Binance Futures Testnet
Usage: python src/limit_orders.py BTCUSDT SELL 0.01 42000
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


class LimitOrderBot:
    """Limit order implementation for Binance Futures Testnet"""
    
    def __init__(self):
        """Initialize the limit order bot"""
        try:
            Config.validate_credentials()
            self.client = Client(Config.API_KEY, Config.API_SECRET)
            self.client.API_URL = Config.BASE_URL
            trading_logger.log_info("Limit Order Bot initialized for Binance Futures Testnet")
        except Exception as e:
            TradingUtils.print_error_and_exit(f"Failed to initialize bot: {e}")
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        """Place a limit order"""
        try:
            # Prepare order parameters
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'quantity': quantity,
                'price': price,
                'timeInForce': 'GTC'  # Good Till Cancelled
            }
            
            trading_logger.log_api_request("POST", "/fapi/v1/order", params)
            
            # Place the order
            order = self.client.futures_create_order(**params)
            
            trading_logger.log_api_response("/fapi/v1/order", order)
            trading_logger.log_order_placed("LIMIT", symbol, side, quantity, order)
            
            return order
            
        except BinanceAPIException as e:
            trading_logger.log_error(e, f"Limit order placement - {symbol} {side}")
            raise ValueError(f"Limit order failed: {e.message}")
        except BinanceRequestException as e:
            trading_logger.log_error(e, f"Limit order placement - {symbol} {side}")
            raise ConnectionError(f"Network error during limit order: {e}")


def main():
    """Main function for CLI execution"""
    # Check command line arguments
    if len(sys.argv) != 5:
        TradingUtils.print_usage_and_exit("limit_orders.py", "<SYMBOL> <SIDE> <QUANTITY> <PRICE>")
    
    script_name, symbol, side, quantity, price = sys.argv
    
    try:
        # Validate inputs
        validated_symbol = TradingUtils.validate_symbol(symbol)
        validated_side = TradingUtils.validate_side(side)
        validated_quantity = TradingUtils.validate_quantity(quantity)
        validated_price = TradingUtils.validate_price(price)
        
        print(f"\n🚀 Placing LIMIT {validated_side} order...")
        print(f"   Symbol: {validated_symbol}")
        print(f"   Quantity: {validated_quantity}")
        print(f"   Price: {validated_price}")
        
        # Initialize bot and place order
        bot = LimitOrderBot()
        order_response = bot.place_limit_order(validated_symbol, validated_side, validated_quantity, validated_price)
        
        # Print result
        TradingUtils.print_order_result("LIMIT", order_response)
        
    except ValidationError as e:
        TradingUtils.print_error_and_exit(f"Validation Error: {e}")
    except ValueError as e:
        TradingUtils.print_error_and_exit(f"Order Error: {e}")
    except Exception as e:
        TradingUtils.print_error_and_exit(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
