import openai
from ..core.interceptor import interceptor

class ClawedOpenAI(openai.AsyncOpenAI):
    """
    A drop-in replacement for AsyncOpenAI that automatically 
    instruments the TokenClaw recovery protocol with safety guardrails.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Safety threshold: don't trigger clawback for very short responses
        self.min_token_threshold = 15 
        
        self.chat.completions.create = interceptor.wrap_request(
            self.chat.completions.create
        )

    def _should_trigger_recovery(self, completion_tokens: int) -> bool:
        """Internal safety check to prevent premature termination."""
        return completion_tokens >= self.min_token_threshold
