#!/usr/bin/env python3
"""Quick test of NVIDIA API connection"""

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
print(f"API Key configured: {bool(api_key and not api_key.startswith('nvapi-your'))}")
print(f"API Key starts with: {api_key[:15] if api_key else 'None'}...")

if api_key and not api_key.startswith('nvapi-your'):
    from openai import OpenAI
    
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    print("OpenAI client initialized successfully!")
    print("Sending test request...")
    
    try:
        completion = client.chat.completions.create(
            model="minimaxai/minimax-m2.7",
            messages=[{"role": "user", "content": "Say 'Hello' in one word."}],
            temperature=0.5,
            max_tokens=50,
            stream=True
        )
        
        print("Response: ", end="")
        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n[SUCCESS] API connection works!")
        
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
else:
    print("[ERROR] API key not configured!")
