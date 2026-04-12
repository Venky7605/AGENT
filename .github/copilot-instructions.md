# NVIDIA API Integration Project Setup

This project demonstrates secure integration with NVIDIA's API using the OpenAI Python client library.

## Setup Checklist

- [x] Project dependencies installed (openai, python-dotenv)
- [x] Main script created with streaming support
- [x] VS Code tasks configured for easy execution
- [x] Python syntax validated
- [x] Environment configuration file template provided
- [x] Git ignore rules configured to protect secrets
- [x] Complete documentation in README.md

## Project Structure

```
.
├── nvidia_chat.py         # Main script with streaming chat completions
├── requirements.txt       # Python dependencies
├── .env                   # Local config (add your API key here)
├── .env.example          # Template for environment variables
├── .gitignore            # Git configuration to protect secrets
├── README.md             # Complete project documentation
└── .vscode/
    └── tasks.json        # VS Code tasks for running the script
```

## Getting Started

### 1. Add Your API Key
Edit `.env` and replace the placeholder with your actual NVIDIA API key:
```
NVIDIA_API_KEY=nvapi-your-actual-api-key-here
```

### 2. Run the Script
Use the VS Code task or terminal:
```bash
python nvidia_chat.py
```

Or use the pre-configured VS Code task: Press `Ctrl+Shift+B` (Run Build Task)

## Available VS Code Tasks

1. **Run NVIDIA Chat Script** (Default) - Executes the main script
2. **Install Dependencies** - Installs required packages
3. **Check Python Syntax** - Validates Python syntax

## Features Implemented

✅ Secure API key handling via environment variables  
✅ Streaming responses for real-time output  
✅ Error handling for missing configuration  
✅ Proper exception handling  
✅ Comprehensive docstrings  
✅ Type hints for better IDE support  

## Customization

Modify the `chat_with_nvidia()` function parameters in `nvidia_chat.py`:

```python
chat_with_nvidia(
    user_message="Your question here",
    temperature=0.7,  # Lower = more deterministic
    max_tokens=1024   # Shorter responses
)
```

## Security Notes

- Never commit `.env` to version control (protected by .gitignore)
- Treat your API key like a password
- Regenerate keys if accidentally exposed
- Store keys in environment variables, not in code

## Troubleshooting

**Configuration Error:** Ensure `.env` file is in the project root with `NVIDIA_API_KEY` set  
**Import Error:** Run `pip install -r requirements.txt` to install dependencies  
**Connection Issues:** Verify internet connection and API key validity

## Next Steps

- Modify `nvidia_chat.py` to add custom prompts or features
- Integrate with your application
- Add logging for production use
- Implement retry logic for network resilience

---

For detailed information, see [README.md](../README.md)
