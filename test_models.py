#!/usr/bin/env python3
"""Test different NVIDIA API models"""

import os
from dotenv import load_dotenv
load_dotenv(override=True)

from openai import OpenAI

api_key = os.getenv("NVIDIA_API_KEY")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# Test different model names that might be available
models_to_try = [
    "meta/llama-2-70b-chat",
    "mistralai/mistral-7b-instruct-v0.3",
    "meta/llama-3-70b-instruct",
    "minimaxai/minimax-m2.7",
]

print("Testing available models...\n")

for model in models_to_try:
    print(f"Testing: {model}")
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.5,
            max_tokens=20,
            stream=False,
            timeout=5  # 5 second timeout
        )
        print(f"  [OK] Model works!")
        print(f"  Response: {completion.choices[0].message.content[:50]}")
        break
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "not found" in error_msg.lower():
            print(f"  [SKIP] Model not available (404)")
        elif "403" in error_msg:
            print(f"  [DENIED] Access denied (check API key)")
        elif "timeout" in error_msg.lower():
            print(f"  [TIMEOUT] Request timed out")
        else:
            print(f"  [ERROR] {type(e).__name__}: {error_msg[:60]}...")
    print()
