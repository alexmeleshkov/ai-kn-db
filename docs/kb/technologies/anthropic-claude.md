# Anthropic Claude API

**Category**: AI Model / LLM API
**Website**: https://www.anthropic.com/
**Documentation**: https://docs.anthropic.com/

---

## Overview

Claude is Anthropic's family of large language models accessible via API. Supports text generation, analysis, coding assistance, and tool use (function calling) with strong reasoning capabilities.

---

## Key Features

**Long Context**: Up to 200k tokens (Claude 3.5 Sonnet)
**Tool Use**: Function calling for structured data extraction and API integration
**Streaming**: Server-sent events for real-time response generation
**Extended Thinking**: Chain-of-thought reasoning before answering
**Vision**: Image understanding (Claude 3 models)
**Safety**: Constitutional AI training for helpful, harmless, honest responses

---

## Common Use Cases

- **Chatbots**: Customer support, Q&A systems
- **Code Generation**: Writing, explaining, debugging code
- **Data Extraction**: Structured data from unstructured text
- **NL-to-SQL**: Converting questions to database queries
- **Content Generation**: Writing, summarization, translation
- **Analysis**: Document review, sentiment analysis

---

## Prerequisites

**API Key**:
- Sign up at https://console.anthropic.com/
- Create API key in dashboard
- Set environment variable: `ANTHROPIC_API_KEY`

**Installation**:
```bash
# Python
pip install anthropic

# Node.js
npm install @anthropic-ai/sdk
```

---

## Basic Usage

### Python
```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Simple message
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)
print(response.content[0].text)
```

### Node.js
```javascript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const message = await client.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude!' }
  ]
});

console.log(message.content[0].text);
```

---

## Advanced Patterns

### 1. Streaming Responses
```python
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain quantum computing"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### 2. Tool Use (Function Calling)
```python
tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }
]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
)

# Claude will return tool_use content block
for block in response.content:
    if block.type == "tool_use":
        print(f"Tool: {block.name}, Input: {block.input}")
```

### 3. System Prompts
```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful SQL expert. Convert questions to PostgreSQL queries.",
    messages=[
        {"role": "user", "content": "How many users signed up yesterday?"}
    ]
)
```

### 4. Extended Thinking
```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    thinking={
        "type": "enabled",
        "budget_tokens": 2000
    },
    messages=[{"role": "user", "content": "Solve this complex problem..."}]
)

# Response includes thinking content blocks
for block in response.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking}")
    elif block.type == "text":
        print(f"Answer: {block.text}")
```

---

## Model Selection

**Claude 3.5 Sonnet** (claude-3-5-sonnet-20241022):
- Best for: Most use cases (balanced performance/cost)
- Context: 200k tokens
- Use when: You need strong reasoning at reasonable cost

**Claude 3 Opus** (claude-3-opus-20240229):
- Best for: Complex tasks requiring maximum intelligence
- Context: 200k tokens
- Use when: Quality matters more than cost/speed

**Claude 3 Haiku** (claude-3-haiku-20240307):
- Best for: Simple tasks, high volume
- Context: 200k tokens
- Use when: Speed and cost are critical

---

## Best Practices

**DO**:
- Use system prompts for role/behavior definition
- Include few-shot examples for complex tasks
- Stream responses for better UX
- Use tool use for structured outputs
- Cache system prompts (beta feature)
- Handle rate limits with exponential backoff

**DON'T**:
- Don't include API keys in code (use environment variables)
- Don't exceed token limits (count tokens first)
- Don't ignore content filtering (handle refusals)
- Don't skip error handling (API can fail)
- Don't send sensitive data without encryption

---

## Pricing (as of 2024)

**Claude 3.5 Sonnet**:
- Input: $3 per million tokens
- Output: $15 per million tokens

**Claude 3 Opus**:
- Input: $15 per million tokens
- Output: $75 per million tokens

**Claude 3 Haiku**:
- Input: $0.25 per million tokens
- Output: $1.25 per million tokens

---

## Error Handling

```python
from anthropic import APIError, APIConnectionError, RateLimitError

try:
    response = client.messages.create(...)
except RateLimitError:
    # Handle rate limit (429)
    time.sleep(60)
except APIConnectionError:
    # Handle connection errors
    pass
except APIError as e:
    # Handle other API errors
    print(f"Error: {e.status_code}, {e.message}")
```

---

## Alternatives

**OpenAI GPT-4**: Strong reasoning, larger ecosystem (but different API)
**Google Gemini**: Multimodal, free tier (but less capable for coding)
**Llama 3**: Open source, self-hosted (but requires infrastructure)
**Mistral**: European alternative (but smaller context)

**Why Claude**:
- Strong reasoning and coding abilities
- Long context window (200k tokens)
- Tool use for structured outputs
- Safety-focused (Constitutional AI)

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Features**: [[natural-language-sql]], [[real-time-chat]]
**Technologies often used with**: [[fastapi]], [[sse]], [[postgresql]]
