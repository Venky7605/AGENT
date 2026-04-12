#!/usr/bin/env python3
"""Diagnostic script to test NVIDIA API connection"""

import os
import sys

# Force fresh environment
if 'NVIDIA_API_KEY' in os.environ:
    del os.environ['NVIDIA_API_KEY']

# Load from .env
from dotenv import load_dotenv
load_dotenv(override=True)

api_key = os.getenv("NVIDIA_API_KEY")
print(f"[1] API Key loaded: {bool(api_key)}")
if api_key:
    print(f"    Key format: {api_key[:10]}...{api_key[-10:]}")
    print(f"    Key length: {len(api_key)}")

# Initialize client
from openai import OpenAI

print(f"[2] Initializing OpenAI client...")
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)
print(f"    Client created successfully")

print(f"[3] Testing API connection...")
print(f"    Model: minimaxai/minimax-m2.7")
print(f"    Endpoint: https://integrate.api.nvidia.com/v1")

try:
    completion = client.chat.completions.create(
        model="minimaxai/minimax-m2.7",
        messages=[{"role": "user", "content": "Hi"}],
        temperature=0.5,
        max_tokens=20,
        stream=False  # First try non-streaming
    )
    print(f"\n[SUCCESS] API is working!")
    print(f"Response: {completion.choices[0].message.content}")
    
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}")
    print(f"Details: {str(e)}")
    print(f"\nPossible causes:")
    print(f"  - API key is invalid or expired")
    print(f"  - API key doesn't have access to this model")
    print(f"  - Account is not activated")
    sys.exit(1)
