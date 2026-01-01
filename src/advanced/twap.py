#!/usr/bin/env python3
"""
TWAP (Time-Weighted Average Price) Orders CLI Module for Binance Futures Testnet
Usage: python src/advanced/twap.py BTCUSDT BUY 0.05 5 10
"""

import sys
import os
import time
from typing import List

# Add src directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from binance import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from config import Config
from logger import trading_logger
from utils import TradingUtils, ValidationError


class TWAPOrderBot:
    """TWAP order implementation for Binance Futures Testnet"""
    
    def __init__(self):
        """Initialize the TWAP order bot"""
        try:
            # Validate credentials
            Config.validate_credentials()

            # ✅ CORRECT initialization using kwargs
            client_kwargs = Config.get_futures_client_kwargs()
            self.client = Client(**client_kwargs)

            # ✅ FORCE Futures Testnet endpoint
            self.client.FUTURES_URL = Config.FUTURES_TESTNET_URL

            trading_logger.log_info(
                "TWAP Order Bot initialized for Binance Futures Testnet"
            )

        except Exception as e:
            TradingUtils.print_error_and_exit(
                f"Failed to initialize Futures client: {e}"
            )
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """Place a market order for TWAP execution"""
        try:
            # Prepare order parameters
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'quantity': quantity
            }
            
            trading_logger.log_api_request("POST", "/fapi/v1/order", params)
            
            # ✅ Use futures_create_order for Futures API
            order = self.client.futures_create_order(**params)
            
            trading_logger.log_api_response("/fapi/v1/order", order)
            
            return order
            
        except BinanceAPIException as e:
            trading_logger.log_error(e, f"TWAP market order placement - {symbol} {side}")
            raise ValueError(f"TWAP market order failed: {e.message}")
        except BinanceRequestException as e:
            trading_logger.log_error(e, f"TWAP market order placement - {symbol} {side}")
            raise ConnectionError(f"Network error during TWAP market order: {e}")
    
    def execute_twap_strategy(self, symbol: str, side: str, total_quantity: float, 
                             chunks: int, interval_seconds: int) -> List[dict]:
        """Execute TWAP strategy by splitting order into chunks"""
        orders = []
        chunk_quantity = total_quantity / chunks
        
        print(f"\n📊 Executing TWAP Strategy:")
        print(f"   Total Quantity: {total_quantity}")
        print(f"   Chunks: {chunks}")
        print(f"   Chunk Size: {chunk_quantity:.6f}")
        print(f"   Interval: {interval_seconds} seconds")
        print(f"   Estimated Duration: {chunks * interval_seconds} seconds")
        
        trading_logger.log_info(f"Starting TWAP execution - Symbol: {symbol}, Side: {side}, "
                               f"Total Qty: {total_quantity}, Chunks: {chunks}, "
                               f"Chunk Size: {chunk_quantity}, Interval: {interval_seconds}s")
        
        for i in range(chunks):
            try:
                print(f"\n⏳ Executing chunk {i + 1}/{chunks}...")
                
                # Place market order for this chunk
                order = self.place_market_order(symbol, side, chunk_quantity)
                orders.append(order)
                
                # Log chunk execution
                trading_logger.log_info(f"TWAP chunk {i + 1}/{chunks} executed - "
                                       f"Order ID: {order.get('orderId')}, "
                                       f"Quantity: {chunk_quantity}")
                
                print(f"   ✅ Chunk {i + 1} executed - Order ID: {order.get('orderId')}")
                print(f"   📈 Filled Quantity: {order.get('executedQty', 'N/A')}")
                
                # Wait for next chunk (except after last chunk)
                if i < chunks - 1:
                    print(f"   ⏱️  Waiting {interval_seconds} seconds...")
                    time.sleep(interval_seconds)
                
            except Exception as e:
                trading_logger.log_error(e, f"TWAP chunk {i + 1} execution")
                print(f"   ❌ Chunk {i + 1} failed: {e}")
                # Continue with remaining chunks
                continue
        
        return orders
    
    def print_twap_summary(self, orders: List[dict], total_quantity: float):
        """Print TWAP execution summary"""
        print(f"\n📋 TWAP EXECUTION SUMMARY")
        print(f"   Total Chunks: {len(orders)}")
        
        total_filled = 0
        successful_orders = 0
        
        for order in orders:
            if order.get('status') == 'FILLED':
                successful_orders += 1
                try:
                    filled_qty = float(order.get('executedQty', 0))
                    total_filled += filled_qty
                except (ValueError, TypeError):
                    pass
        
        print(f"   Successful Chunks: {successful_orders}")
        print(f"   Total Quantity Requested: {total_quantity}")
        print(f"   Total Quantity Filled: {total_filled}")
        print(f"   Fill Rate: {(total_filled/total_quantity*100):.2f}%" if total_quantity > 0 else "   Fill Rate: 0.00%")
        
        trading_logger.log_info(f"TWAP execution completed - Total chunks: {len(orders)}, "
                               f"Successful: {successful_orders}, "
                               f"Total filled: {total_filled}")


def main():
    """Main function for CLI execution"""
    # Check command line arguments
    if len(sys.argv) != 6:
        TradingUtils.print_usage_and_exit("advanced/twap.py", "<SYMBOL> <SIDE> <TOTAL_QUANTITY> <CHUNKS> <INTERVAL_SECONDS>")
    
    script_name, symbol, side, total_quantity, chunks, interval_seconds = sys.argv
    
    try:
        # Validate inputs
        validated_symbol = TradingUtils.validate_symbol(symbol)
        validated_side = TradingUtils.validate_side(side)
        validated_total_quantity = TradingUtils.validate_quantity(total_quantity)
        validated_chunks = TradingUtils.validate_positive_integer(chunks, "Chunks")
        validated_interval = TradingUtils.validate_positive_integer(interval_seconds, "Interval")
        
        # Additional TWAP-specific validations
        if validated_chunks > 50:
            TradingUtils.print_error_and_exit("Maximum 50 chunks allowed for TWAP execution")
        
        if validated_interval > 300:
            TradingUtils.print_error_and_exit("Maximum 300 seconds interval allowed")
        
        # Initialize bot and execute TWAP
        bot = TWAPOrderBot()
        orders = bot.execute_twap_strategy(
            validated_symbol, validated_side, validated_total_quantity,
            validated_chunks, validated_interval
        )
        
        # Print summary
        bot.print_twap_summary(orders, validated_total_quantity)
        
        print(f"\n✅ TWAP execution completed. Check bot.log for detailed information.")
        
    except ValidationError as e:
        TradingUtils.print_error_and_exit(f"Validation Error: {e}")
    except ValueError as e:
        TradingUtils.print_error_and_exit(f"Order Error: {e}")
    except Exception as e:
        TradingUtils.print_error_and_exit(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()