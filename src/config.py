"""
Configuration module for Binance Futures Testnet Trading Bot
Handles environment variables and API configuration
"""

import os
from typing import Optional


class Config:
    """Configuration class for trading bot settings"""

    # Binance Futures Testnet URL (MANDATORY)
    FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"

    # API Keys from environment variables
    API_KEY: Optional[str] = os.getenv("BINANCE_API_KEY")
    API_SECRET: Optional[str] = os.getenv("BINANCE_API_SECRET")

    # Environment
    TESTNET = True

    # Default trading settings
    DEFAULT_SYMBOL = "BTCUSDT"

    # Logging
    LOG_FILE = "bot.log"
    LOG_LEVEL = "INFO"

    # Order limits
    MIN_QUANTITY = 0.001
    MAX_QUANTITY = 1000

    @classmethod
    def validate_credentials(cls) -> None:
        """Validate that API credentials are set"""
        if not cls.API_KEY:
            raise ValueError("BINANCE_API_KEY environment variable not set")
        if not cls.API_SECRET:
            raise ValueError("BINANCE_API_SECRET environment variable not set")

    @classmethod
    def get_futures_client_kwargs(cls) -> dict:
        """
        Get kwargs for initializing Binance Futures client
        Returns dict with api_key, api_secret, and testnet flag
        """
        cls.validate_credentials()
        return {
            "api_key": cls.API_KEY,
            "api_secret": cls.API_SECRET,
            "testnet": True,  # 🔥 CRITICAL for Futures Testnet
        }