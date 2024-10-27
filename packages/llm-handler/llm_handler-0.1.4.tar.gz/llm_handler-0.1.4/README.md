# LLM Handler

A unified Python package for handling LLM API calls across multiple providers (OpenAI, Anthropic, and Google).

## Features

- Unified interface for multiple LLM providers
- Async and sync support
- Token limit validation
- Consistent token counting across providers
- Built-in error handling
- Environment variable configuration

## Installation

```bash
pip install llm-handler
```

## Usage

### Async Usage

```python
import asyncio
from llm_handler import LLMHandler

async def main():
    handler = LLMHandler()
    
    response = await handler.get_completion(
        prompt="Tell me a joke",
        model="gpt-4o",
        temperature=0.7,
        max_tokens=100
    )
    
    print(f"Response: {response.text}")
    print(f"Prompt tokens: {response.prompt_tokens}")
    print(f"Completion tokens: {response.completion_tokens}")

asyncio.run(main())
```

### Synchronous Usage

```python
from llm_handler import LLMHandler

handler = LLMHandler()
response = handler.get_completion_sync(
    prompt="Tell me a joke",
    model="gpt-4o",
    temperature=0.7,
)
print(response.text)
```

## Supported Models

### OpenAI
- gpt-4o
- gpt-4o-mini
- o1-preview
- o1-mini

### Anthropic
- claude-3-opus-latest
- claude-3-sonnet-latest

### Google
- gemini-1.5-pro

## Configuration

Create a `.env` file in your project root:

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

## License

MIT License - see LICENSE file for details