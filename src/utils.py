"""
Utility functions for Binance Futures Trading Bot
Provides input validation and helper functions
"""

import re
import sys
from typing import Optional, Tuple
from decimal import Decimal, InvalidOperation

from config import Config
from logger import trading_logger


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class TradingUtils:
    """Utility class for trading operations and validation"""
    
    # Valid order sides
    VALID_ORDER_SIDES = {'BUY', 'SELL'}
    
    # Symbol pattern (e.g., BTCUSDT, ETHUSDT)
    SYMBOL_PATTERN = re.compile(r'^[A-Z]{6,12}$')
    
    @classmethod
    def validate_symbol(cls, symbol: str) -> str:
        """Validate trading symbol format"""
        if not symbol:
            raise ValidationError("Symbol is required")
        
        symbol = symbol.upper().strip()
        
        if not cls.SYMBOL_PATTERN.match(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}. "
                               f"Expected format like 'BTCUSDT'")
        
        trading_logger.log_debug(f"Symbol validation passed: {symbol}")
        return symbol
    
    @classmethod
    def validate_side(cls, side: str) -> str:
        """Validate order side"""
        if not side:
            raise ValidationError("Order side is required")
        
        side = side.upper().strip()
        
        if side not in cls.VALID_ORDER_SIDES:
            raise ValidationError(f"Invalid order side: {side}. "
                               f"Valid sides: {', '.join(cls.VALID_ORDER_SIDES)}")
        
        trading_logger.log_debug(f"Order side validation passed: {side}")
        return side
    
    @classmethod
    def validate_quantity(cls, quantity_str: str) -> float:
        """Validate order quantity"""
        if not quantity_str:
            raise ValidationError("Quantity is required")
        
        try:
            quantity = float(quantity_str)
        except ValueError:
            raise ValidationError(f"Invalid quantity format: {quantity_str}")
        
        if quantity <= 0:
            raise ValidationError(f"Quantity must be positive: {quantity}")
        
        if quantity < Config.MIN_QUANTITY:
            raise ValidationError(f"Quantity too small: {quantity}. "
                               f"Minimum: {Config.MIN_QUANTITY}")
        
        if quantity > Config.MAX_QUANTITY:
            raise ValidationError(f"Quantity too large: {quantity}. "
                               f"Maximum: {Config.MAX_QUANTITY}")
        
        trading_logger.log_debug(f"Quantity validation passed: {quantity}")
        return quantity
    
    @classmethod
    def validate_price(cls, price_str: str) -> float:
        """Validate price"""
        if not price_str:
            raise ValidationError("Price is required")
        
        try:
            price = float(price_str)
        except ValueError:
            raise ValidationError(f"Invalid price format: {price_str}")
        
        if price <= 0:
            raise ValidationError(f"Price must be positive: {price}")
        
        # Validate decimal places (max 8 for most crypto pairs)
        try:
            decimal_price = Decimal(str(price))
            if decimal_price.as_tuple().exponent < -8:
                raise ValidationError(f"Price has too many decimal places: {price}")
        except InvalidOperation:
            raise ValidationError(f"Invalid price format: {price}")
        
        trading_logger.log_debug(f"Price validation passed: {price}")
        return price
    
    @classmethod
    def validate_positive_integer(cls, value_str: str, field_name: str) -> int:
        """Validate positive integer"""
        if not value_str:
            raise ValidationError(f"{field_name} is required")
        
        try:
            value = int(value_str)
        except ValueError:
            raise ValidationError(f"Invalid {field_name.lower()} format: {value_str}")
        
        if value <= 0:
            raise ValidationError(f"{field_name} must be positive: {value}")
        
        trading_logger.log_debug(f"{field_name} validation passed: {value}")
        return value
    
    @classmethod
    def print_order_result(cls, order_type: str, order_response: dict):
        """Print formatted order result"""
        print(f"\n✅ {order_type.upper()} ORDER PLACED SUCCESSFULLY")
        print(f"   Order ID: {order_response.get('orderId', 'N/A')}")
        print(f"   Symbol: {order_response.get('symbol', 'N/A')}")
        print(f"   Side: {order_response.get('side', 'N/A')}")
        print(f"   Type: {order_response.get('type', 'N/A')}")
        print(f"   Quantity: {order_response.get('origQty', 'N/A')}")
        print(f"   Price: {order_response.get('price', 'MARKET')}")
        print(f"   Status: {order_response.get('status', 'N/A')}")
        print(f"   Timestamp: {order_response.get('time', 'N/A')}")
    
    @classmethod
    def print_error_and_exit(cls, message: str):
        """Print error message and exit"""
        print(f"❌ ERROR: {message}")
        trading_logger.log_error(Exception(message), "CLI execution")
        sys.exit(1)
    
    @classmethod
    def print_usage_and_exit(cls, script_name: str, usage: str):
        """Print usage message and exit"""
        print(f"\n📖 USAGE: python {script_name} {usage}")
        print("\n📋 EXAMPLES:")
        if script_name.endswith("market_orders.py"):
            print("   python src/market_orders.py BTCUSDT BUY 0.01")
        elif script_name.endswith("limit_orders.py"):
            print("   python src/limit_orders.py BTCUSDT SELL 0.01 42000")
        elif script_name.endswith("stop_limit.py"):
            print("   python src/advanced/stop_limit.py BTCUSDT BUY 0.01 41500 41600")
        elif script_name.endswith("twap.py"):
            print("   python src/advanced/twap.py BTCUSDT BUY 0.05 5 10")
        
        print("\n⚙️  ENVIRONMENT VARIABLES REQUIRED:")
        print("   BINANCE_API_KEY=your_api_key")
        print("   BINANCE_API_SECRET=your_api_secret")
        
        sys.exit(1)
