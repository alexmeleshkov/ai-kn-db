# TypeScript - Polling Task Status with Timeout

**Language**: TypeScript
**Technology**: Fetch API, Async/Await
**Feature/Pattern**: Polling Loop, Task Status Checking, Timeout Handling
**Difficulty**: intermediate

---

## Prerequisites

**Required Packages**:
```bash
# No external packages required - uses native APIs
npm install typescript
```

**Required Knowledge**:
- Async/await patterns
- Promise handling
- setTimeout and timing
- TypeScript interfaces
- HTTP status codes
- Polling vs WebSocket vs SSE

---

## Overview

This snippet demonstrates a production-ready polling implementation for checking asynchronous task status. It handles long-running operations by repeatedly checking status with configurable intervals and timeouts, suitable for operations that don't need real-time updates.

Key features:
- Configurable polling interval and timeout
- Status-based completion detection
- Error handling for failed tasks
- Timeout with user-friendly error
- Type-safe status responses
- Efficient delay with Promise

---

## Implementation

### Basic Usage

```typescript
import { pollTaskStatus } from './api';

// Start async task
const response = await fetch('/api/start-task', { method: 'POST' });
const { task_id } = await response.json();

// Poll until complete
try {
  const result = await pollTaskStatus(task_id);
  console.log('Task completed:', result);
} catch (err) {
  console.error('Task failed or timed out:', err);
}
```

**Explanation**:
- Start task and get task_id
- pollTaskStatus waits until complete or timeout
- Returns result when status is 'completed'
- Throws error if status is 'failed' or timeout reached

### Advanced Usage with Custom Configuration

```typescript
// Poll with custom settings
async function processLargeDataset(data: any) {
  // Start task
  const response = await fetch('/api/process', {
    method: 'POST',
    body: JSON.stringify(data),
  });
  const { task_id } = await response.json();

  try {
    // Poll with 30 minute timeout, check every 2 seconds
    const result = await pollTaskStatus(
      task_id,
      1800000, // 30 minutes
      2000     // 2 seconds
    );
    return result;
  } catch (err) {
    if (err.message.includes('timed out')) {
      console.error('Task still running after 30 minutes');
      // Optionally cancel the task
      await fetch(`/api/tasks/${task_id}/cancel`, { method: 'POST' });
    }
    throw err;
  }
}

// Poll with progress callback
async function pollWithProgress(
  taskId: string,
  onProgress: (progress: number) => void
): Promise<ChatResponse> {
  const startTime = Date.now();
  const maxWaitMs = 300000; // 5 minutes
  const pollIntervalMs = 1000;

  while (Date.now() - startTime < maxWaitMs) {
    const status = await getTaskStatus(taskId);

    // Update progress
    onProgress(status.progress);

    if (status.status === 'completed' && status.result) {
      return status.result;
    }

    if (status.status === 'failed') {
      throw new ApiError(500, status.error || 'Task failed');
    }

    // Wait before next poll
    await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
  }

  throw new ApiError(408, 'Task timed out');
}
```

**Key Points**:
- Timeout and interval configurable per use case
- Progress tracking available with custom implementation
- Task cancellation on timeout
- Status transitions: pending → running → completed/failed

---

## Complete Example

```typescript
/**
 * Task status response interface.
 */
export interface TaskStatusResponse {
  task_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  result?: ChatResponse;
  error?: string;
}

/**
 * Get task status from API.
 */
export async function getTaskStatus(taskId: string): Promise<TaskStatusResponse> {
  return fetchApi<TaskStatusResponse>(`/tasks/${taskId}`);
}

/**
 * Poll for task completion with timeout.
 *
 * @param taskId - Task ID to poll
 * @param maxWaitMs - Maximum time to wait (default: 5 minutes)
 * @param pollIntervalMs - Time between polls (default: 1 second)
 * @returns Task result when completed
 * @throws ApiError if task fails or times out
 */
async function pollTaskStatus(
  taskId: string,
  maxWaitMs: number = 300000, // 5 minutes max
  pollIntervalMs: number = 1000
): Promise<ChatResponse> {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitMs) {
    const status = await getTaskStatus(taskId);

    if (status.status === 'completed' && status.result) {
      return status.result;
    }

    if (status.status === 'failed') {
      throw new ApiError(500, status.error || 'Query failed');
    }

    // Wait before next poll
    await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
  }

  throw new ApiError(408, 'Query timed out');
}

/**
 * Send a chat message with async task handling.
 * If the response indicates async processing, polls for results.
 */
export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetchApi<ChatResponse>('/chat', {
    method: 'POST',
    body: JSON.stringify(request),
  });

  // If async, poll for results
  if (response.is_async && response.task_id) {
    return pollTaskStatus(response.task_id);
  }

  return response;
}
```

---

## Configuration

```typescript
// Polling configuration based on use case
const POLLING_CONFIGS = {
  // Fast operations (1-5 seconds)
  fast: {
    maxWaitMs: 10000,    // 10 seconds
    pollIntervalMs: 200, // 200ms
  },
  // Normal operations (5-30 seconds)
  normal: {
    maxWaitMs: 60000,    // 1 minute
    pollIntervalMs: 1000, // 1 second
  },
  // Slow operations (1-5 minutes)
  slow: {
    maxWaitMs: 300000,   // 5 minutes
    pollIntervalMs: 2000, // 2 seconds
  },
  // Very slow operations (5+ minutes)
  verySlow: {
    maxWaitMs: 1800000,  // 30 minutes
    pollIntervalMs: 5000, // 5 seconds
  },
};

// Usage
async function pollTask(taskId: string, type: keyof typeof POLLING_CONFIGS) {
  const config = POLLING_CONFIGS[type];
  return pollTaskStatus(taskId, config.maxWaitMs, config.pollIntervalMs);
}
```

---

## Error Handling

```typescript
async function robustPollTaskStatus(taskId: string): Promise<ChatResponse> {
  const maxRetries = 3;
  let retryCount = 0;

  while (retryCount < maxRetries) {
    try {
      return await pollTaskStatus(taskId);
    } catch (err) {
      if (err instanceof ApiError) {
        switch (err.status) {
          case 404:
            // Task not found - might have been cleaned up
            throw new Error('Task not found. It may have expired.');

          case 408:
            // Timeout - don't retry
            throw new Error('Task timed out. Try a simpler query.');

          case 500:
            // Task failed - don't retry
            throw new Error(err.message || 'Task failed');

          case 429:
            // Rate limited - wait and retry
            console.warn('Rate limited, retrying in 5 seconds...');
            await new Promise(resolve => setTimeout(resolve, 5000));
            retryCount++;
            continue;

          default:
            // Network error - retry
            console.warn(`Network error, retry ${retryCount + 1}/${maxRetries}`);
            await new Promise(resolve => setTimeout(resolve, 2000));
            retryCount++;
            continue;
        }
      }

      // Non-API error
      throw err;
    }
  }

  throw new Error('Max retries exceeded');
}

// Polling with exponential backoff
async function pollWithBackoff(taskId: string): Promise<ChatResponse> {
  const startTime = Date.now();
  const maxWaitMs = 300000; // 5 minutes
  let pollIntervalMs = 500; // Start with 500ms

  while (Date.now() - startTime < maxWaitMs) {
    try {
      const status = await getTaskStatus(taskId);

      if (status.status === 'completed' && status.result) {
        return status.result;
      }

      if (status.status === 'failed') {
        throw new ApiError(500, status.error || 'Task failed');
      }

      // Exponential backoff: 500ms → 1s → 2s → 4s (max 5s)
      await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
      pollIntervalMs = Math.min(pollIntervalMs * 2, 5000);

    } catch (err) {
      if (err instanceof ApiError && err.status >= 500) {
        // Server error - wait and retry
        await new Promise(resolve => setTimeout(resolve, 2000));
        continue;
      }
      throw err;
    }
  }

  throw new ApiError(408, 'Task timed out');
}
```

**Common Errors**:
1. **408 Timeout**: Task exceeded max wait time - suggest shorter query or resume later
2. **500 Task Failed**: Task encountered error during processing - show error message
3. **404 Task Not Found**: Task expired or invalid ID - task may have been cleaned up
4. **429 Rate Limited**: Too many status checks - use exponential backoff

---

## Testing

```typescript
import { pollTaskStatus, getTaskStatus } from './api';

// Mock getTaskStatus
jest.mock('./api', () => ({
  getTaskStatus: jest.fn(),
}));

describe('pollTaskStatus', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('returns result when task completes', async () => {
    const mockResult = { message: 'Success' };
    (getTaskStatus as jest.Mock)
      .mockResolvedValueOnce({
        status: 'pending',
        progress: 0,
      })
      .mockResolvedValueOnce({
        status: 'running',
        progress: 50,
      })
      .mockResolvedValueOnce({
        status: 'completed',
        progress: 100,
        result: mockResult,
      });

    const result = await pollTaskStatus('task123', 10000, 100);

    expect(result).toEqual(mockResult);
    expect(getTaskStatus).toHaveBeenCalledTimes(3);
  });

  it('throws error when task fails', async () => {
    (getTaskStatus as jest.Mock).mockResolvedValueOnce({
      status: 'failed',
      error: 'Processing error',
    });

    await expect(pollTaskStatus('task123')).rejects.toThrow('Processing error');
  });

  it('throws timeout error when exceeded', async () => {
    (getTaskStatus as jest.Mock).mockResolvedValue({
      status: 'running',
      progress: 50,
    });

    await expect(
      pollTaskStatus('task123', 1000, 200)
    ).rejects.toThrow('Query timed out');
  });

  it('polls at correct interval', async () => {
    jest.useFakeTimers();

    (getTaskStatus as jest.Mock).mockResolvedValue({
      status: 'running',
      progress: 50,
    });

    const promise = pollTaskStatus('task123', 5000, 1000);

    // Fast-forward 2 seconds
    await jest.advanceTimersByTimeAsync(2000);

    expect(getTaskStatus).toHaveBeenCalledTimes(2);

    jest.useRealTimers();
  });
});
```

---

## Performance Considerations

- **Interval Selection**: Balance between responsiveness and server load
  - Fast queries: 200-500ms intervals
  - Normal queries: 1-2s intervals
  - Slow queries: 2-5s intervals
- **Exponential Backoff**: Reduces server load for long-running tasks
- **Timeout Configuration**: Prevent indefinite waiting with reasonable limits
- **Server Resources**: Each poll is a HTTP request - use SSE/WebSocket for real-time needs
- **Promise Timing**: setTimeout wrapped in Promise for accurate delays

---

## Security Considerations

- **Task ID Validation**: Validate task_id format to prevent injection
- **Rate Limiting**: Backend should limit status check frequency
- **Task Cleanup**: Expire completed/failed tasks after reasonable time
- **Authorization**: Verify user owns task before returning status
- **Timeout Limits**: Prevent resource exhaustion with max timeout
- **Error Messages**: Don't expose internal details in error messages

---

## Related

**Feature**: [[nl-to-sql/claude-tool-use]]
**Technology**: [[typescript]], [[fastapi]]
**Language**: [[typescript]]
**Used in projects**: [[db-chat-nl-complete]]
**Alternative implementations**: [[typescript-sse-client-streaming.md]] (better for real-time updates)
