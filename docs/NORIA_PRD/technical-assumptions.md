# Technical Assumptions

### Repository Structure: Monorepo

Single repository containing both frontend and backend components for simplified development and deployment coordination.

### Service Architecture

**MVP Architecture**: Next.js PWA frontend + Python FastAPI backend with serverless deployment
- **Frontend**: Next.js 15 PWA with Vercel deployment
- **Backend**: Python FastAPI with Vercel Functions
- **Database**: PostgreSQL (local Docker container for development, Supabase-managed in production)
- **Queue System**: Celery + Redis for background analysis
- **AI Integration**: Claude Sonnet 4 via Anthropic Python SDK

**Rationale**: Python FastAPI backend leverages the mature AI/ML ecosystem for sophisticated conversation analysis while maintaining rapid development velocity. PWA approach provides native-like experience without app store complexity.

### Testing requirements

- **Unit Testing**: Jest for frontend, pytest for backend Python code
- **Integration Testing**: API endpoint testing with test database
- **End-to-End Testing**: Playwright for critical user flows (account creation, chat functionality, crisis detection)
- **Manual Testing**: Crisis detection scenarios and conversation quality validation

### Additional Technical Assumptions and Requests

- **uv Package Manager**: Lightning-fast Python dependency management (10-100x faster than pip)
- **Cost Monitoring**: Built-in Claude API usage tracking with automated budget alerts
- **Async Operations**: All AI API calls must use async patterns for scalability
- **Error Handling**: Graceful fallbacks for AI API failures to maintain conversation continuity
- **Security**: JWT session management with 24-hour expiration
- **Real-time Features**: WebSocket support through Supabase (or compatible Postgres listeners) for live conversation updates

