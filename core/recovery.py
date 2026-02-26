import os
import math
from typing import Any, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class RecoveryEngine:
    """
    Speculative Token Recovery (STR) & Solana Fee Rebate Engine.
    """
    def __init__(self, rebate_multiplier: float = 0.05, window_size: int = 10):
        # FIX: Now loads from .env instead of being hardcoded
        self.treasury_vault = os.getenv(
            "TOKENCLAW_VAULT_ADDRESS", 
            "5Ex8FT88ybZpDC3p4ydHoRVn2nmiNYVonXiapTT9SDTS"
        )
        self.rebate_multiplier = rebate_multiplier
        self.entropy_buffer: List[float] = []
        self.window_size = window_size 

    def calculate_potential_savings(self, context_tokens: int, current_usage: int) -> float:
        """
        FIX: Implementation of the savings logic.
        Calculates USD value of saved inference tokens.
        """
        saved_count = context_tokens - current_usage
        # Average GPT-4o pricing
        token_price = 0.000015 
        return round(saved_count * token_price, 4)

    def _update_entropy_buffer(self, new_value: float):
        self.entropy_buffer.append(new_value)
        if len(self.entropy_buffer) > self.window_size:
            self.entropy_buffer.pop(0)

    def calculate_sol_rebate(self, compute_units: int, tx_volume: float) -> float:
        rebate = (compute_units / 1000) * tx_volume * self.rebate_multiplier
        return round(rebate, 6)

    def get_vault_status(self):
        return {
            "vault": self.treasury_vault,
            "status": "Synchronized",
            "chain": "Solana-Mainnet"
        }
