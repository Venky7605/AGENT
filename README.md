# NVIDIA API Chat with OpenAI Client

This project demonstrates how to integrate with NVIDIA's API using the OpenAI Python client library with the Minimax model.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Your API Key

**⚠️ IMPORTANT: Never commit your actual API key to version control!**

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your NVIDIA API key:
   ```
   NVIDIA_API_KEY=nvapi-your-actual-key-here
   ```

3. Get your API key from [NVIDIA API Console](https://build.nvidia.com/mistralai/mistral-7b-instruct)

### 3. Run the Script

```bash
python nvidia_chat.py
```

## Files

- **nvidia_chat.py**: Main script with streaming chat completions
- **.env.example**: Template for environment variables
- **.env**: Your local configuration (not committed to git)
- **requirements.txt**: Python dependencies

## Features

- ✅ Secure API key handling via environment variables
- ✅ Streaming responses for real-time output
- ✅ Error handling for missing configuration
- ✅ Clean, documented code structure

## API Details

- **Base URL**: `https://integrate.api.nvidia.com/v1`
- **Model**: `minimaxai/minimax-m2.7`
- **Default Settings**:
  - Temperature: 1.0
  - Top P: 0.95
  - Max Tokens: 8192

## Security Best Practices

1. **Never share your API key** - treat it like a password
2. **Use `.env` files locally** - add `.env` to `.gitignore`
3. **Rotate keys regularly** - regenerate if compromised
4. **Use environment variables** - keep secrets out of source code

## Customization

To modify the chat parameters, edit the `chat_with_nvidia()` function:

```python
chat_with_nvidia(
    user_message="Your question here",
    temperature=0.7,  # Lower = more deterministic
    max_tokens=1024   # Shorter responses
)
```

## Troubleshooting

**"NVIDIA_API_KEY environment variable not set"**
- Ensure `.env` file exists and has the correct API key
- Verify you're running from the project directory

**"Authentication failed"**
- Check that your API key is correct and active
- Regenerate the key from the NVIDIA console if needed

**Connection errors**
- Verify internet connection
- Check that the API endpoint is accessible

## License

MIT
