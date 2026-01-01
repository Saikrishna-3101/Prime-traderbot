"""
Logging module for Binance Futures Trading Bot
Provides structured logging with file output to root level
"""

import logging
import os
from datetime import datetime
from typing import Optional

from config import Config


class TradingLogger:
    """Custom logger for trading operations"""
    
    def __init__(self, name: str = "TradingBot"):
        self.name = name
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger with file and console handlers"""
        logger = logging.getLogger(self.name)
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))
        
        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # File handler - Log to root level
        file_handler = logging.FileHandler(Config.LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_api_request(self, method: str, endpoint: str, params: Optional[dict] = None):
        """Log API request details"""
        self.logger.info(f"API Request - {method} {endpoint}")
        if params:
            self.logger.debug(f"Request params: {params}")
    
    def log_api_response(self, endpoint: str, response: dict):
        """Log API response details"""
        self.logger.info(f"API Response - {endpoint}")
        self.logger.debug(f"Response data: {response}")
    
    def log_order_placed(self, order_type: str, symbol: str, side: str, quantity: float, order_details: dict):
        """Log successful order placement"""
        self.logger.info(f"Order placed successfully - Type: {order_type}, Symbol: {symbol}, Side: {side}, Quantity: {quantity}")
        self.logger.info(f"Order ID: {order_details.get('orderId')}")
        self.logger.debug(f"Full order response: {order_details}")
    
    def log_error(self, error: Exception, context: str = ""):
        """Log error with context and stack trace"""
        self.logger.error(f"Error in {context}: {str(error)}", exc_info=True)
        self.logger.debug(f"Error type: {type(error).__name__}")
    
    def log_validation_error(self, field: str, value: str, reason: str):
        """Log input validation errors"""
        self.logger.warning(f"Validation failed - {field}: '{value}' ({reason})")
    
    def log_info(self, message: str):
        """Log general info message"""
        self.logger.info(message)
    
    def log_debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)


# Global logger instance
trading_logger = TradingLogger()
