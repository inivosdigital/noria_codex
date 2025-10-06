# Tech Stack

## Technology Stack Table

| Category | Technology | Version | Purpose | Rationale |
| :----------------------- | :---------------- | :---------- | :---------- | :------------- |
| **Frontend Language** | TypeScript | 5.3.3 | Type-safe frontend development | Strong typing, code sharing with backend |
| **Frontend Framework** | Next.js | 15.0.0 | React framework with SSR/SSG | PWA support, Vercel optimization, mobile-first |
| **UI Component Library** | shadcn/ui + Tailwind | Latest | Modern, accessible components | Consistent design system, mobile optimization |
| **State Management** | Zustand | 4.4.6 | Lightweight state management | Simple API, TypeScript support, no boilerplate |
| **Backend Language** | Python | 3.11+ | Backend development language | AI/ML ecosystem, mature libraries |
| **Backend Framework** | FastAPI | 0.104.0+ | Modern Python web framework | Async support, auto-docs, type hints |
| **API Style** | REST + WebSocket | - | HTTP APIs + real-time messaging | Simple, well-supported, real-time chat |
| **Database** | PostgreSQL | 15.0 | Primary data store | ACID compliance, JSON support; Docker locally, Supabase integration for hosted envs |
| **Real-time** | Supabase Realtime | 2.39.0 | WebSocket subscriptions | Live conversation updates, PostgreSQL triggers |
| **File Storage** | Supabase Storage | 2.39.0 | User files, assets | S3-compatible, integrated authentication |
| **Authentication** | Supabase Auth | 2.39.0 | User authentication | Email/password, social providers, JWTs |
| **AI Integration** | Anthropic SDK (Python) | Latest | Claude Sonnet 4 integration | Rich Python AI ecosystem, async support |
| **Frontend Testing** | Vitest + Testing Library | Latest | Component and unit testing | Fast, modern testing with TypeScript |
| **Backend Testing** | pytest + httpx | Latest | API endpoint testing | Python standard, async HTTP testing |
| **E2E Testing** | Playwright | Latest | Full user journey testing | Cross-browser, mobile testing, reliability |
| **Build Tool** | Turborepo | Latest | Monorepo build orchestration | Caching, parallel builds, Vercel integration |
| **Python Package Manager** | uv | Latest | Fast Python dependency management | 10-100x faster than pip/poetry, reliable resolution |
| **CSS Framework** | Tailwind CSS | 3.4.0 | Utility-first styling | Mobile-first design, component consistency |
| **PWA** | Next.js PWA | Latest | Progressive web app features | Offline capability, home screen install |
| **Deployment** | Vercel | - | Frontend and API hosting | Zero-config deployment, edge optimization |
| **Monitoring** | Vercel Analytics | - | Performance and error tracking | Built-in monitoring, zero configuration |
| **Queue System** | Celery + Redis | Latest | Background job processing | Mature Python task queue, scalable |
