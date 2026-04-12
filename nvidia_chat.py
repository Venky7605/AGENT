"""
NVIDIA API Integration with OpenAI Client

This script demonstrates how to use the NVIDIA API through the OpenAI client library
with proper environment variable handling for API keys.
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Load environment variables from .env file
load_dotenv()

def chat_with_nvidia(
    user_message: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    system_prompt: str = None,
    verbose: bool = True
) -> str:
    """
    Send a message to the NVIDIA Minimax API and stream the response.

    Args:
        user_message: The user's message to send
        temperature: Sampling temperature (0-2). Lower = more deterministic, higher = more creative
        max_tokens: Maximum tokens in the response (1-8192)
        system_prompt: Optional system prompt to customize AI behavior
        verbose: Print response to stdout (default: True)

    Returns:
        The complete response text

    Raises:
        ValueError: If API key is not configured
        PermissionDeniedError: If API key is invalid or expired
    """
    # Get API key from environment variable
    api_key = os.getenv("NVIDIA_API_KEY")
    
    if not api_key or api_key.startswith("nvapi-your"):
        raise ValueError(
            "[ERROR] NVIDIA_API_KEY not configured.\n"
            "   1. Get your key from: https://build.nvidia.com/\n"
            "   2. Edit .env and set: NVIDIA_API_KEY=nvapi-...\n"
            "   3. Re-run the script"
        )

    # Initialize OpenAI client with NVIDIA's API endpoint
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )

    # Prepare messages with optional system prompt
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    if verbose:
        print("[NVIDIA] Streaming response from NVIDIA Minimax AI:\n")

    full_response = ""

    try:
        # Create chat completion with streaming enabled
        completion = client.chat.completions.create(
            model="minimaxai/minimax-m2.7",
            messages=messages,
            temperature=temperature,
            top_p=0.95,
            max_tokens=max_tokens,
            stream=True
        )

        # Process streaming chunks
        for chunk in completion:
            if not getattr(chunk, "choices", None):
                continue
            
            # Extract content from delta if available
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                if verbose:
                    print(content, end="", flush=True)

    except Exception as e:
        error_msg = f"❌ API Error: {str(e)}"
        if verbose:
            print(f"\n[API ERROR] {str(e)}")
        raise

    if verbose:
        print("\n")  # Add newline at the end

    return full_response


class Conversation:
    """
    Manages a multi-turn conversation with the NVIDIA API.
    
    Maintains conversation history and provides context to the AI
    for coherent multi-turn interactions.
    """
    
    def __init__(
        self,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        verbose: bool = True
    ):
        """
        Initialize a new conversation session.
        
        Args:
            system_prompt: Optional system prompt to customize AI behavior
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in each response
            verbose: Print responses to stdout
        """
        self.messages = []
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.verbose = verbose
        
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
    
    def add_user_message(self, message: str) -> None:
        """Add a user message to the conversation history."""
        self.messages.append({"role": "user", "content": message})
    
    def add_ai_response(self, response: str) -> None:
        """Add an AI response to the conversation history."""
        self.messages.append({"role": "assistant", "content": response})
    
    def send(self, user_message: str) -> str:
        """
        Send a message and get AI response within this conversation context.
        
        Args:
            user_message: The user's message
            
        Returns:
            The AI's response text
        """
        self.add_user_message(user_message)
        
        # Get API key
        api_key = os.getenv("NVIDIA_API_KEY")
        
        if not api_key or api_key.startswith("nvapi-your"):
            raise ValueError(
                "[ERROR] NVIDIA_API_KEY not configured.\n"
                "   1. Get your key from: https://build.nvidia.com/\n"
                "   2. Edit .env and set: NVIDIA_API_KEY=nvapi-...\n"
                "   3. Re-run the script"
            )
        
        # Initialize client
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        
        if self.verbose:
            print("[NVIDIA] Streaming response:\n")
        
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="minimaxai/minimax-m2.7",
                messages=self.messages,
                temperature=self.temperature,
                top_p=0.95,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            for chunk in completion:
                if not getattr(chunk, "choices", None):
                    continue
                
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    if self.verbose:
                        print(content, end="", flush=True)
            
            if self.verbose:
                print("\n")
            
            # Add AI response to history
            self.add_ai_response(full_response)
            
            return full_response
            
        except Exception as e:
            if self.verbose:
                print(f"\n[API ERROR] {str(e)}")
            raise
    
    def get_history(self) -> list:
        """Return the full conversation history."""
        return self.messages.copy()
    
    def clear_history(self) -> None:
        """Clear conversation history but keep system prompt."""
        if self.system_prompt:
            self.messages = [{"role": "system", "content": self.system_prompt}]
        else:
            self.messages = []
    
    def display_history(self) -> None:
        """Print the conversation history in a readable format."""
        print("\n" + "=" * 60)
        print("CONVERSATION HISTORY")
        print("=" * 60)
        
        for i, msg in enumerate(self.messages):
            role = msg["role"].upper()
            content = msg["content"]
            
            if role == "SYSTEM":
                print(f"\n[{role}]:\n{content[:100]}{'...' if len(content) > 100 else ''}")
            else:
                # Split long messages for readability
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"\n[{role}]: {preview}")
        
        print("\n" + "=" * 60 + "\n")


def interactive_mode():
    """Run an interactive multi-turn conversation session."""
    print("\n" + "=" * 60)
    print("NVIDIA CHAT - INTERACTIVE MODE")
    print("=" * 60)
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'history' to see the conversation history")
    print("Type 'clear' to clear the conversation history")
    print("=" * 60 + "\n")
    
    # Create conversation with optional system prompt
    system_prompt = input("Optional system prompt (press Enter to skip): ").strip()
    if not system_prompt:
        system_prompt = None
    
    conv = Conversation(system_prompt=system_prompt, verbose=True)
    
    print("\n[OK] Conversation started. Start typing your messages!\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n[OK] Ending conversation. Goodbye!")
                conv.display_history()
                break
            
            if user_input.lower() == "history":
                conv.display_history()
                continue
            
            if user_input.lower() == "clear":
                conv.clear_history()
                print("[OK] Conversation history cleared.\n")
                continue
            
            # Send message and get response
            try:
                conv.send(user_input)
            except ValueError as e:
                print(f"\n[CONFIG ERROR] {e}\n")
                break
            except Exception as e:
                print(f"\n[ERROR] {e}\n")
                break
                
        except KeyboardInterrupt:
            print("\n\n[OK] Conversation interrupted. Goodbye!")
            conv.display_history()
            break


if __name__ == "__main__":
    # Example 1: Simple question
    print("=" * 60)
    print("EXAMPLE 1: Simple Question")
    print("=" * 60)
    
    try:
        response = chat_with_nvidia("What is the capital of France?")
        print(f"\n[OK] Response length: {len(response)} characters\n")
    except ValueError as e:
        print(f"[CONFIG ERROR]\n{e}\n")
    except Exception as e:
        print(f"[ERROR] {e}\n")

    # Example 2: Custom temperature (more creative)
    print("=" * 60)
    print("EXAMPLE 2: Creative Response (Higher Temperature)")
    print("=" * 60)
    
    try:
        response = chat_with_nvidia(
            user_message="Write a haiku about Python programming",
            temperature=1.5,  # More creative
            max_tokens=256
        )
        print(f"\n[OK] Response length: {len(response)} characters\n")
    except Exception as e:
        print(f"[ERROR] {e}\n")

    # Example 3: With system prompt (role-based AI)
    print("=" * 60)
    print("EXAMPLE 3: Expert Assistant with System Prompt")
    print("=" * 60)
    
    try:
        response = chat_with_nvidia(
            user_message="How do I debug Python code?",
            system_prompt="You are an expert Python developer. Give concise, practical advice.",
            temperature=0.5,  # More deterministic
            max_tokens=512
        )
        print(f"\n[OK] Response length: {len(response)} characters\n")
    except Exception as e:
        print(f"[ERROR] {e}\n")
