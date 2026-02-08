# Python + Anthropic - Claude Tool Use with Streaming

**Language**: Python
**Technology**: Anthropic Claude API
**Feature/Pattern**: Agentic tool use with streaming responses
**Difficulty**: advanced

---

## Prerequisites

**Required Packages**:
```bash
pip install anthropic
```

**Required Knowledge**:
- Claude API Messages format
- Tool use (function calling) patterns
- Python generators and yield
- Streaming API responses
- Agentic workflows (multi-step reasoning)

---

## Overview

This snippet demonstrates Claude's agentic tool use with streaming responses. Claude can autonomously call tools (functions), process results, and iterate until the task is complete. This pattern is ideal for SQL query execution, API calls, or any multi-step workflow where Claude needs to make decisions based on intermediate results.

Key features:
- Tool definitions with input schemas
- Streaming text and tool calls simultaneously
- Multi-iteration agentic loops (Claude decides when to stop)
- Error handling and retry logic
- Tool result feedback to Claude
- Extended thinking mode for complex reasoning

---

## Implementation

### Basic Usage

#### Define Tools for Claude

```python
SQL_TOOLS = [
    {
        "name": "execute_sql",
        "description": "Execute a SQL query against the database and return results. Use this to answer questions about the data. Only SELECT queries are allowed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL SELECT query to execute. Must be a valid SELECT or WITH (CTE) query."
                },
                "reasoning": {
                    "type": "string",
                    "description": "Brief explanation of why you're running this query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "ask_clarification",
        "description": "Ask the user to clarify their question when there are multiple possible interpretations. Use this BEFORE answering when you detect ambiguity.",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The clarifying question to ask the user"
                },
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of specific options for the user to choose from (2-5 options)"
                },
                "context": {
                    "type": "string",
                    "description": "Brief explanation of why clarification is needed"
                }
            },
            "required": ["question", "options"]
        }
    }
]
```

**Key Points**:
- `input_schema`: JSON Schema defining required/optional parameters
- `description`: Instructions for Claude on when/how to use the tool
- `required`: List of mandatory fields (Claude will always provide these)

#### Simple Tool Use (Non-Streaming)

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Build system prompt with context
system_prompt = """You are a helpful SQL assistant.
Available tables: users (id, name, email), orders (id, user_id, amount)

Use execute_sql tool to answer questions about the data."""

messages = [{"role": "user", "content": "How many users do we have?"}]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=system_prompt,
    tools=SQL_TOOLS,
    messages=messages
)

# Check if Claude wants to use a tool
if response.stop_reason == "tool_use":
    for block in response.content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input
            tool_use_id = block.id

            if tool_name == "execute_sql":
                sql_query = tool_input["query"]
                print(f"Claude wants to execute: {sql_query}")

                # Execute the query (your implementation)
                result = execute_query(sql_query)

                # Send result back to Claude
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": f"Query returned {len(result)} rows: {result}"
                    }]
                })

                # Continue conversation
                response2 = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4096,
                    system=system_prompt,
                    tools=SQL_TOOLS,
                    messages=messages
                )

                # Extract final answer
                for block in response2.content:
                    if block.type == "text":
                        print(f"Claude's answer: {block.text}")
```

### Advanced Usage

#### Agentic Loop with Multiple Iterations

```python
from typing import Callable, Generator, Any

def process_with_tools(
    client: anthropic.Anthropic,
    user_question: str,
    system_prompt: str,
    execute_sql_func: Callable[[str], dict],
    max_iterations: int = 15
) -> tuple[str, list[tuple[str, dict]]]:
    """
    Agentic processing loop - Claude calls tools until task is complete.

    Returns:
        (final_response, list of (sql_query, result) pairs)
    """
    messages = [{"role": "user", "content": user_question}]
    executed_queries = []

    for iteration in range(max_iterations):
        # Call Claude with tools
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            tools=SQL_TOOLS,
            messages=messages
        )

        print(f"Iteration {iteration + 1}: stop_reason={response.stop_reason}")

        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            assistant_content = response.content
            tool_results = []

            for block in assistant_content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_use_id = block.id

                    if tool_name == "execute_sql":
                        sql_query = tool_input.get("query", "")
                        reasoning = tool_input.get("reasoning", "")

                        print(f"Tool call: execute_sql - {reasoning}")
                        print(f"SQL: {sql_query}")

                        # Execute query
                        result = execute_sql_func(sql_query)
                        executed_queries.append((sql_query, result))

                        if result.get("error"):
                            # Send error back to Claude for retry
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": tool_use_id,
                                "content": f"Error: {result['error']}",
                                "is_error": True
                            })
                        else:
                            # Send results to Claude
                            result_str = format_result(result)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": tool_use_id,
                                "content": result_str
                            })

            # Add assistant response and tool results to conversation
            messages.append({"role": "assistant", "content": assistant_content})
            messages.append({"role": "user", "content": tool_results})

        else:
            # Claude is done - extract final response
            final_response = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_response += block.text

            print(f"Complete after {iteration + 1} iterations")
            return final_response, executed_queries

    # Max iterations reached
    return "Unable to complete within iteration limit.", executed_queries
```

---

## Complete Example

### Streaming Tool Use with Events

```python
import anthropic
from typing import Generator, Any, Callable

SYSTEM_PROMPT = """You are a data analyst assistant that helps users query databases.

## Database Schema

{schema}

## Your Capabilities

You have access to:
1. `execute_sql` - Run SQL queries against the database
2. `ask_clarification` - Ask the user to clarify when there's ambiguity

## Instructions

1. Study the schema carefully to understand table relationships
2. Execute SQL queries to answer questions
3. If a query fails, fix it based on the error message
4. Provide clear natural language answers with the results

## SQL Guidelines

- Only SELECT queries are allowed
- Use exact column names from the schema
- Use JOINs to combine data from multiple tables"""

SQL_TOOLS = [
    {
        "name": "execute_sql",
        "description": "Execute a SQL query and return results",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "SQL SELECT query"},
                "reasoning": {"type": "string", "description": "Why you're running this query"}
            },
            "required": ["query"]
        }
    }
]

def process_with_tools_streaming(
    client: anthropic.Anthropic,
    user_question: str,
    schema: str,
    execute_sql_func: Callable[[str], dict],
    max_iterations: int = 15
) -> Generator[dict[str, Any], None, None]:
    """
    Process question with streaming output.

    Yields events:
    - {"type": "text", "content": "..."} - text chunks
    - {"type": "thinking", "content": "..."} - extended thinking (if enabled)
    - {"type": "tool_start", "tool": "execute_sql", "query": "..."} - tool execution start
    - {"type": "tool_result", "query": "...", "success": bool, "rows": int} - tool result
    - {"type": "error", "message": "..."} - errors
    - {"type": "done", "queries": [...]} - completion
    """
    system_prompt = SYSTEM_PROMPT.format(schema=schema)
    messages = [{"role": "user", "content": user_question}]
    executed_queries = []

    for iteration in range(max_iterations):
        try:
            # Build API parameters
            api_params = {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 4096,
                "system": system_prompt,
                "tools": SQL_TOOLS,
                "messages": messages,
            }

            # Optional: Enable extended thinking for complex reasoning
            # api_params["thinking"] = {
            #     "type": "enabled",
            #     "budget_tokens": 4096
            # }

            # Call Claude with streaming
            with client.messages.stream(**api_params) as stream:
                collected_content = []
                current_text = ""
                is_thinking = False

                for event in stream:
                    # Track content block type
                    if event.type == "content_block_start":
                        if hasattr(event.content_block, "type"):
                            if event.content_block.type == "thinking":
                                is_thinking = True
                                yield {"type": "thinking_start"}
                            elif event.content_block.type == "text":
                                is_thinking = False
                                current_text = ""
                            elif event.content_block.type == "tool_use":
                                is_thinking = False

                    # Stream delta content
                    elif event.type == "content_block_delta":
                        if hasattr(event.delta, "thinking"):
                            # Extended thinking content
                            yield {"type": "thinking", "content": event.delta.thinking}
                        elif hasattr(event.delta, "text"):
                            # Regular text content
                            text_chunk = event.delta.text
                            current_text += text_chunk
                            yield {"type": "text", "content": text_chunk}

                    # Mark end of thinking block
                    elif event.type == "content_block_stop":
                        if is_thinking:
                            yield {"type": "thinking_end"}
                            is_thinking = False

                # Get the final message
                response = stream.get_final_message()

            print(f"Iteration {iteration + 1}: stop_reason={response.stop_reason}")

            # Check if Claude wants to use a tool
            if response.stop_reason == "tool_use":
                assistant_content = response.content
                tool_results = []

                for block in assistant_content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        tool_use_id = block.id

                        if tool_name == "execute_sql":
                            sql_query = tool_input.get("query", "")
                            reasoning = tool_input.get("reasoning", "")

                            # Emit tool start event
                            yield {
                                "type": "tool_start",
                                "tool": "execute_sql",
                                "query": sql_query,
                                "reasoning": reasoning
                            }

                            # Execute query
                            result = execute_sql_func(sql_query)

                            if result.get("error"):
                                # Emit error event
                                yield {
                                    "type": "tool_result",
                                    "query": sql_query,
                                    "success": False,
                                    "error": result["error"]
                                }

                                # Send error back to Claude
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_id,
                                    "content": f"Error: {result['error']}",
                                    "is_error": True
                                })
                            else:
                                # Emit success event
                                yield {
                                    "type": "tool_result",
                                    "query": sql_query,
                                    "success": True,
                                    "rows": len(result.get("rows", [])),
                                    "execution_time": result.get("execution_time_ms", 0)
                                }

                                executed_queries.append({
                                    "query": sql_query,
                                    "rows": len(result["rows"])
                                })

                                # Send results to Claude
                                result_str = format_result_for_claude(result)
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_id,
                                    "content": result_str
                                })

                # Continue conversation
                messages.append({"role": "assistant", "content": assistant_content})
                messages.append({"role": "user", "content": tool_results})

            else:
                # Claude is done - send completion event
                yield {"type": "done", "queries": executed_queries}
                return

        except anthropic.APIError as e:
            yield {"type": "error", "message": f"API error: {str(e)}"}
            yield {"type": "done", "queries": executed_queries}
            return

    # Max iterations reached
    yield {"type": "error", "message": "Max iterations reached"}
    yield {"type": "done", "queries": executed_queries}


def format_result_for_claude(result: dict, max_rows: int = 50) -> str:
    """Format query result for sending back to Claude."""
    if result.get("error"):
        return f"Error: {result['error']}"

    rows = result.get("rows", [])
    if not rows:
        return "Query executed successfully. No rows returned."

    lines = [
        f"Query returned {len(rows)} rows.",
        f"Columns: {', '.join(result.get('columns', []))}",
        ""
    ]

    # Format as simple table
    display_rows = rows[:max_rows]
    for row in display_rows:
        row_str = " | ".join(str(cell) if cell is not None else "NULL" for cell in row)
        lines.append(row_str)

    if len(rows) > max_rows:
        lines.append(f"... ({len(rows) - max_rows} more rows)")

    return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    client = anthropic.Anthropic(api_key="your-api-key")

    def mock_execute_sql(query: str) -> dict:
        """Mock SQL execution."""
        return {
            "columns": ["count"],
            "rows": [[42]],
            "execution_time_ms": 15
        }

    # Stream events
    for event in process_with_tools_streaming(
        client=client,
        user_question="How many users do we have?",
        schema="users (id, name, email)",
        execute_sql_func=mock_execute_sql
    ):
        if event["type"] == "text":
            print(event["content"], end="", flush=True)
        elif event["type"] == "tool_start":
            print(f"\n[Executing: {event['query']}]")
        elif event["type"] == "tool_result":
            print(f"[Result: {event['rows']} rows]")
        elif event["type"] == "done":
            print(f"\n[Done - {len(event['queries'])} queries executed]")
```

---

## Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    anthropic_model: str = "claude-sonnet-4-20250514"
    anthropic_max_tokens: int = 4096

    # Extended thinking (for complex reasoning)
    enable_extended_thinking: bool = False
    thinking_budget_tokens: int = 4096  # Min 1024, affects cost

    class Config:
        env_file = ".env"
```

**Environment Variables** (.env):
```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-20250514
ANTHROPIC_MAX_TOKENS=4096
ENABLE_EXTENDED_THINKING=false
THINKING_BUDGET_TOKENS=4096
```

---

## Error Handling

```python
import anthropic
import logging

logger = logging.getLogger(__name__)

def safe_tool_use_with_retry(
    client: anthropic.Anthropic,
    messages: list[dict],
    system_prompt: str,
    max_retries: int = 3
) -> anthropic.types.Message:
    """Call Claude with automatic retry on API errors."""
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=system_prompt,
                tools=SQL_TOOLS,
                messages=messages
            )
        except anthropic.RateLimitError as e:
            logger.warning(f"Rate limit hit (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
        except anthropic.APIConnectionError as e:
            logger.error(f"API connection error: {e}")
            raise
        except anthropic.APIError as e:
            logger.error(f"API error: {e}")
            raise

def validate_tool_input(tool_name: str, tool_input: dict) -> tuple[bool, str]:
    """Validate tool inputs before execution."""
    if tool_name == "execute_sql":
        query = tool_input.get("query", "")

        if not query:
            return False, "Query cannot be empty"

        # Only allow SELECT queries
        if not query.strip().upper().startswith(("SELECT", "WITH")):
            return False, "Only SELECT queries are allowed"

        # Check for dangerous keywords
        dangerous = ["DROP", "DELETE", "INSERT", "UPDATE", "TRUNCATE"]
        if any(keyword in query.upper() for keyword in dangerous):
            return False, f"Query contains forbidden operations"

    return True, ""
```

**Common Errors**:
1. **RateLimitError**: API rate limit exceeded - implement exponential backoff
2. **APIConnectionError**: Network issues - retry with timeout
3. **InvalidToolResultError**: Malformed tool result sent to Claude - validate format
4. **MaxIterationsExceeded**: Safety limit reached - review prompt or increase limit
5. **ToolValidationError**: Tool input validation failed - return error to Claude with clear message

---

## Testing

```python
import pytest
from unittest.mock import Mock, patch

def test_tool_use_basic():
    """Test basic tool use flow."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.stop_reason = "tool_use"
    mock_response.content = [
        Mock(type="tool_use", name="execute_sql", input={"query": "SELECT 1"}, id="tool_123")
    ]
    mock_client.messages.create.return_value = mock_response

    # Simulate tool execution
    result, queries = process_with_tools(
        client=mock_client,
        user_question="Test",
        system_prompt="Test prompt",
        execute_sql_func=lambda q: {"rows": [[1]], "columns": ["result"]}
    )

    assert len(queries) >= 1
    assert queries[0][0] == "SELECT 1"

def test_streaming_events():
    """Test streaming event types."""
    mock_client = Mock()

    events = list(process_with_tools_streaming(
        client=mock_client,
        user_question="Test",
        schema="users (id)",
        execute_sql_func=lambda q: {"rows": [], "columns": []}
    ))

    event_types = {e["type"] for e in events}
    assert "done" in event_types

def test_error_handling():
    """Test error propagation in tool use."""
    def failing_execute(query: str) -> dict:
        return {"error": "Syntax error"}

    # Should handle error gracefully
    result, queries = process_with_tools(
        client=client,
        user_question="Test",
        system_prompt="Test",
        execute_sql_func=failing_execute,
        max_iterations=2
    )

    assert len(queries) > 0
    assert queries[0][1].get("error") is not None
```

---

## Performance Considerations

- **Token Usage**: Tool definitions count toward prompt tokens - keep descriptions concise
- **Iteration Limits**: Set reasonable max_iterations (10-15) to prevent infinite loops
- **Extended Thinking**: Costs extra tokens but improves complex reasoning - use selectively
- **Streaming**: Reduces perceived latency for users but doesn't reduce total time
- **Result Truncation**: Limit rows returned to Claude (max 50-100) to reduce token usage
- **Caching**: Enable prompt caching for repeated system prompts (can save 90% on tokens)

**Prompt Caching Example**:
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=[
        {
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"}  # Cache this block
        }
    ],
    tools=SQL_TOOLS,
    messages=messages
)
```

---

## Security Considerations

- **Input Validation**: Always validate tool inputs before execution (SQL injection, command injection)
- **Query Restrictions**: Enforce SELECT-only queries - reject INSERT/UPDATE/DELETE/DROP
- **Rate Limiting**: Limit tool calls per user to prevent abuse
- **Timeout**: Set execution timeouts for long-running queries
- **Result Sanitization**: Strip sensitive data from results before sending to Claude
- **API Key**: Store Anthropic API key in environment variables, never in code
- **Audit Logging**: Log all tool executions with user context for security review
- **Tool Permissions**: Consider implementing tool-level access control (which users can use which tools)

---

## Related

**Feature**: [[nl-to-sql]], [[agentic-workflows]]
**Technology**: [[anthropic-claude]], [[tool-use]], [[streaming]]
**Language**: [[python]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[openai-function-calling.md]], [[langchain-agents.md]]
