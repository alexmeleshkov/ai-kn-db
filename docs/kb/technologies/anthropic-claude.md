# Anthropic Claude API

**Technology**: Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
**Category**: AI Model / API

---

## Overview

Claude API integration for natural language to SQL conversion with streaming, extended thinking, and tool use pattern.

---

## Usage Files

- `backend/app/services/llm.py`
- `backend/app/services/chat.py`

---

## Complete Usage Patterns

### Streaming with Extended Thinking (llm.py)

**Pattern**:
```python
import anthropic

client = anthropic.Anthropic(api_key=api_key)

with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    temperature=1.0,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": question}],
    system=system_prompt,
    tools=[execute_sql_tool, ask_clarification_tool]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                yield {"type": "thinking", "content": event.delta.thinking}
            elif event.delta.type == "text_delta":
                yield {"type": "text", "content": event.delta.text}
```

**All Behaviors**:
- Streaming response with delta events
- Extended thinking preview
- Tool use for SQL execution
- System prompt with schema context
- Max 4096 output tokens

---

## Configuration

```python
max_tokens=4096
temperature=1.0
thinking_budget=10000  # Full budget first try
thinking_budget=2500   # 1/4 budget on retry
```
