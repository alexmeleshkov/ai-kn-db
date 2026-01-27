# Technical Details: ITFC Analysis

## Technology Decisions

### Why React + TypeScript?
- Type safety for complex chat state management
- Rich ecosystem for UI components
- Fast development with Vite hot reload
- Strong community and tooling

### Why FastAPI?
- Native async/await support for SSE streaming
- Automatic OpenAPI/JSON Schema generation
- Fast performance (comparable to Node.js)
- Pydantic for request/response validation
- Python ecosystem for data processing

### Why Claude Opus 4?
- Extended thinking for complex multi-step reasoning
- Tool use capability (execute_sql, ask_clarification)
- Best-in-class natural language understanding
- Reliable SQL generation from English
- Large context window for schema and examples

**Sources**: ARCHITECTURE.md:L206-L214, README.md:L356

### Why Azure SQL Server?
- Live Ipswich fan data already hosted there
- Direct connection faster than DuckDB + S3 (previous architecture)
- Mature enterprise database with good Python support
- Read-only access reduces risk

### Why RDS PostgreSQL?
- Self-hosted alternative to Supabase (cost control)
- Reliable, mature database
- Good Python support (psycopg2)
- No storage limits like Supabase free tier
- Full control over data and schema

### Why JWT + bcrypt?
- Self-hosted authentication (no third-party dependency)
- Industry-standard security (HMAC SHA-256)
- Stateless tokens (no session storage needed)
- bcrypt with 12 rounds provides strong password hashing

### Why SSE (Server-Sent Events)?
- One-way streaming from server to client (perfect for chat)
- Built into browsers (no WebSocket library needed)
- Simpler than WebSockets for this use case
- Automatic reconnection handling
- Works with Heroku HTTP routing

### Why Heroku?
- Simple deployment (git push)
- Managed infrastructure (no server maintenance)
- Add-ons (QuotaGuard for SOCKS5 proxy)
- Automatic SSL/HTTPS
- Easy scaling (dyno resizing)

## Key Technical Challenges & Solutions

### Challenge 1: Heroku 55-second Timeout
**Problem**: Heroku terminates connections after 55s of inactivity
**Solution**: Heartbeat messages every 10s during SSE streaming

### Challenge 2: Azure SQL IP Whitelist
**Problem**: Heroku dynos have dynamic IPs, Azure SQL requires static IPs
**Solution**: QuotaGuard Static add-on provides SOCKS5 proxy with static IPs

### Challenge 3: Slow Query Times (DuckDB + S3)
**Problem**: Initial architecture downloaded Parquet files from S3 (40s-9min)
**Solution**: Migrated to direct Azure SQL connection (now 100ms-2s)

### Challenge 4: Supabase Storage Limits
**Problem**: Exceeded 1.1GB free tier storage with conversations
**Solution**: Migrated to AWS RDS PostgreSQL (no storage limits)

### Challenge 5: SQL Generation Accuracy
**Problem**: Claude sometimes generates incorrect SQL on first try
**Solution**: 
- Few-shot examples (ipswich_examples.py)
- Universal learning system (stores successful queries)
- Extended thinking (5000 token budget)
- Retry logic (max 15 iterations)

### Challenge 6: Complex Schema with Prefixed Columns
**Problem**: Ipswich database uses prefixed column names like [fan.id], [ticket.fan_id]
**Solution**: 
- Schema introspection with full column names
- Examples showing correct column usage
- Glossary in prompt explaining naming convention

### Challenge 7: Frontend/Backend Integration
**Problem**: Separate frontend build needs to be served by backend
**Solution**: Build script (`build.sh`) copies frontend dist to backend static folder

## Performance Optimizations

### Schema Caching
Cache database schema in memory to avoid repeated introspection (100-200ms saved per query)

### Connection Pooling
PostgreSQL connection pool (psycopg2) reduces connection overhead

### Learned Queries
Retrieve similar successful queries to guide LLM (improves accuracy, reduces retries)

### Streaming Responses
SSE streaming provides immediate feedback instead of waiting for full response

### Row Limiting
Max 1000 rows per query prevents overwhelming frontend and reduces network transfer

## Security Measures

### SQL Injection Prevention
- Only SELECT queries allowed
- Query validation before execution
- Parameterized queries where applicable

### Authentication Security
- bcrypt password hashing (12 rounds, salted)
- JWT tokens with HS256 signature
- 7-day token expiration
- Token stored in localStorage (XSS risk mitigated by HTTPS + CSP)

### API Security
- CORS configured for production domain only
- Read-only database access
- Protected routes require valid JWT
- Rate limiting (optional, not implemented yet)

### Database Security
- Azure SQL requires IP whitelist
- Read-only user credentials
- No DELETE, UPDATE, INSERT allowed
- Connection over TLS

## Testing Strategy

### Current Testing
- Basic API tests (`backend/tests/test_api.py`)
- Manual testing via production deployment

### Testing Gaps
- No frontend unit tests (should test hooks, components)
- No integration tests (should test full chat flow)
- No E2E tests (should test UI interactions)
- No load tests (should test concurrent users, large queries)

### Recommended Testing Approach
1. **Unit Tests**: pytest for backend services, Jest for frontend hooks
2. **Integration Tests**: Test API endpoints with real database connection
3. **E2E Tests**: Playwright or Cypress for full user flows
4. **Load Tests**: Locust or k6 for concurrent user simulation

## Deployment Process

### Local Development
1. Run backend: `cd backend && uvicorn app.main:app --reload`
2. Run frontend: `cd frontend && npm run dev`
3. Access at http://localhost:5173

### Production Deployment
1. Build frontend: `cd frontend && npm run build`
2. Copy to backend: `cp -r dist ../backend/static`
3. Commit backend changes: `cd backend && git add . && git commit -m "Deploy"`
4. Push to Heroku: `git push heroku master`
5. View logs: `heroku logs -a db-chat-nl-app --tail`

### Environment Configuration
- Development: `.env` file in backend/
- Production: Heroku config vars (`heroku config:set KEY=value`)

## Monitoring & Observability

### Current Monitoring
- Heroku logs
- Manual health check endpoint (`/api/v1/health`)

### Missing Monitoring
- Application performance monitoring (APM)
- Error tracking (e.g., Sentry)
- Usage analytics
- Database query performance metrics
- LLM API usage/cost tracking

## Cost Breakdown

| Service | Monthly Cost |
|---------|--------------|
| Heroku Standard-2X | ~$50 |
| AWS RDS db.t3.micro | ~$15-20 |
| Azure SQL Server | Client-provided |
| Anthropic Claude API | Usage-based |
| QuotaGuard Static | Included with Heroku |
| Domain (GoDaddy) | ~$12/year |
| **Total** | **~$65-70/month** |

**Note**: Cost breakdown is estimated based on typical Heroku and AWS pricing. Actual costs may vary.

## Future Technical Improvements

### High Priority
1. Add comprehensive test suite
2. Implement API documentation (Swagger)
3. Add error tracking (Sentry)
4. Implement query result pagination
5. Add rate limiting

### Medium Priority
6. Multi-tenant architecture
7. Role-based access control (RBAC)
8. Query scheduling/automation
9. Improved caching strategy (Redis)
10. Database connection health checks

### Low Priority
11. Dark mode
12. Mobile app (React Native)
13. Query templates/saved queries
14. Advanced visualizations (D3.js)
15. Export to Excel/PDF
