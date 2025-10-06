# External APIs

## Claude Sonnet 4 API

- **Purpose:** AI coaching responses and conversation analysis
- **Documentation:** https://docs.anthropic.com/en/api/
- **Base URL(s):** `https://api.anthropic.com/v1`
- **Authentication:** Bearer token with API key
- **Rate Limits:** 1000 requests/minute, 32k context window

**Key Endpoints Used:**

- `POST /messages` - Generate coaching responses
- `POST /messages` - Perform ChAT scoring analysis
- `POST /messages` - Crisis detection and safety assessment

**Integration Notes:** 
- Circuit breaker pattern for reliability
- Streaming responses for better UX
- Context window management for long conversations
- Safety prompts integrated into all requests

## Supabase Services

- **Purpose:** Database, authentication, real-time subscriptions, file storage
- **Documentation:** https://supabase.com/docs
- **Base URL(s):** `https://{project-id}.supabase.co`
- **Authentication:** JWT tokens, API keys
- **Rate Limits:** 500 requests/second on Pro plan

**Key Endpoints Used:**

- `POST /auth/v1/signup` - User registration
- `POST /auth/v1/token` - Authentication
- `GET /rest/v1/conversations` - Conversation history
- `POST /rest/v1/conversations` - Save messages
- WebSocket endpoint for real-time updates

**Integration Notes:**
- Row Level Security (RLS) for data protection
- Real-time subscriptions for live chat
- Automatic JWT refresh handling
- Database triggers for analysis queue
