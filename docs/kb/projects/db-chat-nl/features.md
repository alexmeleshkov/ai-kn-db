# User-facing features

## Must-have

### Natural Language Database Queries
Users can ask questions in plain English (e.g., "Show me top scorers this season") and receive formatted results without writing SQL. The system translates natural language to SQL using Claude AI.

### Real-time Streaming Responses
Chat responses stream in real-time via Server-Sent Events, showing SQL generation, query execution, and explanations as they happen. Users see immediate feedback rather than waiting for complete responses.

### Data Visualizations
Query results automatically generate appropriate charts (bar, line, pie) based on data structure. Users can visualize trends, comparisons, and distributions without manual chart configuration.

### Conversation History
Users can save, retrieve, and resume past conversations. History includes full message threads with queries, results, and explanations for future reference.

### Multi-table Query Support
The system handles complex queries spanning multiple tables with JOIN operations, aggregations, and filtering. Schema introspection provides Claude with complete table and column metadata.

### User Authentication
Secure registration and login with JWT token-based authentication. Passwords are hashed with bcrypt. Each user has isolated conversation history.

### Query Result Tables
Results display in formatted, sortable tables with column headers. Large result sets are handled gracefully with clear data presentation.

### SQL Transparency
Generated SQL queries are displayed to users, enabling learning and verification. Users can see exactly what query was executed against the database.

### Error Handling and Recovery
When queries fail or return no results, the system provides helpful error messages and suggestions for query refinement.

### Responsive Design
Interface adapts to mobile, tablet, and desktop screens with Ipswich Town brand colors (blue #1a365d).

## Nice-to-have

### Query Learning System
Backend tracks successful query patterns to improve future SQL generation accuracy. The system learns from user interactions over time.

### Domain-Specific Examples
Pre-loaded Ipswich Town football terminology and common query examples help Claude understand fan-specific questions about players, matches, and attendance.

### Markdown Support in Responses
Claude responses support rich markdown formatting including tables, lists, bold, italic, and code blocks for better readability.

### Schema Exploration
Users can view available database tables and columns to understand what data is queryable.

### CSV Export
Users can export query results to CSV format for external analysis (not yet implemented but planned).

### Query Suggestions
System could suggest related questions based on current conversation context (not yet implemented).

### Dark Mode
Interface could support dark theme preference (not yet implemented).

### Query Performance Metrics
Display query execution time and row count for transparency (partially implemented).
