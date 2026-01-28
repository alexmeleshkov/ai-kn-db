# Core modules

## Backend Services

### 1. auth.py - Authentication Service

**Responsibilities**:
- User registration with password hashing (bcrypt)
- Login validation and JWT token generation
- Token verification for protected routes

**Key Functions**:
- `create_user(username, email, password)` - Register new user with hashed password
- `verify_password(plain_password, hashed_password)` - Validate login credentials
- `create_access_token(user_id)` - Generate JWT with expiration
- `verify_token(token)` - Decode and validate JWT, return user_id

**Code Pattern**:
```python
# JWT token generation
def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

# Password hashing with bcrypt
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
```

**Dependencies**: PyJWT, bcrypt, fastapi
**Environment Variables**: JWT_SECRET, JWT_ALGORITHM

---

### 2. llm.py - Claude AI Integration

**Responsibilities**:
- Interface with Anthropic Claude API
- Generate SQL queries from natural language
- Stream responses via SSE
- Provide explanations and query validation

**Key Functions**:
- `generate_sql(question, schema, history)` - Convert NL to SQL using Claude Opus 4
- `stream_response(prompt)` - Async generator for SSE streaming
- `build_prompt(question, schema, examples)` - Construct Claude prompt with context

**Code Pattern**:
```python
# Streaming Claude response
async def stream_response(prompt: str):
    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async with client.messages.stream(
        model="claude-opus-4-5-20250929",
        max_tokens=4096,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        async for text in stream.text_stream:
            yield text
```

**Dependencies**: anthropic>=0.40.0
**Environment Variables**: ANTHROPIC_API_KEY

---

### 3. database_azure.py - Azure SQL Server Connector

**Responsibilities**:
- Connect to Azure SQL Server for fan data
- Execute SELECT queries
- Extract schema metadata
- Handle connection pooling

**Code Pattern**:
```python
def get_connection():
    return pytds.connect(
        server=settings.AZURE_SQL_SERVER,
        database=settings.AZURE_SQL_DATABASE,
        user=settings.AZURE_SQL_USER,
        password=settings.AZURE_SQL_PASSWORD,
        port=1433,
        timeout=30
    )
```

**Dependencies**: python-tds>=1.15.0
**Environment Variables**: AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USER, AZURE_SQL_PASSWORD

---

### 4. chat.py - Chat Orchestration

**Responsibilities**:
- Coordinate NL to SQL to Results pipeline
- Stream SSE responses
- Handle errors and fallbacks

**Code Pattern**:
```python
async def stream_sse_response(question: str, schema: dict):
    yield f"data: {json.dumps({'type': 'status', 'content': 'Generating SQL...'})}\n\n"
    sql = await llm.generate_sql(question, schema)
    yield f"data: {json.dumps({'type': 'sql', 'content': sql})}\n\n"
    results = database_azure.execute_query(sql)
    yield f"data: {json.dumps({'type': 'results', 'data': results})}\n\n"
```

**Dependencies**: fastapi, llm.py, database_azure.py

---

## Frontend Components

### 5. ChatContainer.tsx - Main Chat Interface

**Component Contract**:
```typescript
interface ChatContainerProps {
  conversationId?: string;
  onNewMessage?: (message: Message) => void;
}
```

**Code Pattern**:
```typescript
const streamMessage = async (question: string) => {
  const eventSource = new EventSource(
    `/api/v1/chat/stream?question=${encodeURIComponent(question)}`
  );

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    switch (data.type) {
      case 'status': setStatus(data.content); break;
      case 'sql': setCurrentSQL(data.content); break;
      case 'results': setQueryResults(data.data); break;
    }
  };
};
```

**Dependencies**: react, useChat hook

---

### 6. DataViewer.tsx - Query Results Display

**Component Contract**:
```typescript
interface DataViewerProps {
  data: QueryResult[];
  sql: string;
}
```

**Code Pattern**:
```typescript
const DataViewer: React.FC<DataViewerProps> = ({ data, sql }) => {
  const columns = Object.keys(data[0]);
  return (
    <table>
      <thead>
        <tr>{columns.map(col => <th key={col}>{col}</th>)}</tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i}>
            {columns.map(col => <td key={col}>{row[col]}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  );
};
```

**Dependencies**: react

---

### 7. QueryChart.tsx - Data Visualization

**Component Contract**:
```typescript
interface QueryChartProps {
  data: QueryResult[];
  chartType?: 'bar' | 'line' | 'pie' | 'auto';
}
```

**Code Pattern**:
```typescript
const detectChartType = (data: QueryResult[]): ChartType => {
  const columns = Object.keys(data[0]);
  const numericColumns = columns.filter(col => typeof data[0][col] === 'number');
  return numericColumns.length === 1 ? 'bar' : 'line';
};
```

**Dependencies**: chart.js, react-chartjs-2
