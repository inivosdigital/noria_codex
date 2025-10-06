# Unified Project Structure

```plaintext
noria/
├── .github/                    # CI/CD workflows
│   └── workflows/
│       ├── ci.yml              # Test and lint
│       ├── deploy-staging.yml  # Staging deployment
│       └── deploy-prod.yml     # Production deployment
├── apps/                       # Application packages
│   ├── web/                    # Next.js frontend application
│   │   ├── app/                # App Router (Next.js 15)
│   │   │   ├── (auth)/         # Auth route group
│   │   │   │   ├── login/
│   │   │   │   └── signup/
│   │   │   ├── chat/           # Main chat interface
│   │   │   ├── onboarding/     # Goal selection flow
│   │   │   ├── profile/        # User settings
│   │   │   ├── wellness/       # Crisis resources
│   │   │   ├── layout.tsx      # Root layout
│   │   │   ├── page.tsx        # Home redirect
│   │   │   └── globals.css     # Global styles
│   │   ├── components/         # UI components
│   │   │   ├── ui/             # shadcn/ui components
│   │   │   ├── chat/           # Chat-specific components
│   │   │   ├── forms/          # Form components
│   │   │   └── layout/         # Layout components
│   │   ├── hooks/              # Custom React hooks
│   │   ├── lib/                # Utilities and configuration
│   │   │   ├── supabase.ts     # Supabase client
│   │   │   ├── apiClient.ts    # HTTP client for Python API
│   │   │   └── utils.ts        # General utilities
│   │   ├── services/           # API client services
│   │   │   ├── chatService.ts
│   │   │   ├── userService.ts
│   │   │   └── analysisService.ts
│   │   ├── stores/             # Zustand stores
│   │   │   ├── authStore.ts
│   │   │   ├── chatStore.ts
│   │   │   └── progressStore.ts
│   │   ├── types/              # TypeScript definitions
│   │   │   ├── api.ts          # API response types
│   │   │   └── index.ts        # Shared types
│   │   ├── public/             # Static assets
│   │   │   ├── icons/          # PWA icons
│   │   │   ├── manifest.json   # PWA manifest
│   │   │   └── sw.js           # Service worker
│   │   ├── tests/              # Frontend tests
│   │   │   ├── __mocks__/      # Test mocks
│   │   │   ├── components/     # Component tests
│   │   │   ├── services/       # Service tests
│   │   │   └── e2e/            # End-to-end tests
│   │   ├── .env.local.example  # Environment template
│   │   ├── next.config.js      # Next.js configuration
│   │   ├── tailwind.config.js  # Tailwind configuration
│   │   ├── middleware.ts       # Auth middleware
│   │   └── package.json
│   └── api/                    # Python FastAPI backend
│       ├── app/                # FastAPI application
│       │   ├── api/            # API routes
│       │   │   ├── v1/         # API version 1
│       │   │   │   ├── auth/
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   ├── routes.py
│       │   │   │   │   └── dependencies.py
│       │   │   │   ├── chat/
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   ├── routes.py
│       │   │   │   │   └── schemas.py
│       │   │   │   ├── crisis/
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   ├── routes.py
│       │   │   │   │   └── detection.py
│       │   │   │   ├── wellness/
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   └── routes.py
│       │   │   │   └── __init__.py
│       │   │   └── __init__.py
│       │   ├── core/           # Core configuration
│       │   │   ├── __init__.py
│       │   │   ├── config.py   # Settings and environment
│       │   │   ├── database.py # Database connection
│       │   │   ├── security.py # Auth utilities
│       │   │   └── logging.py  # Logging configuration
│       │   ├── models/         # Pydantic models
│       │   │   ├── __init__.py
│       │   │   ├── user.py     # User models
│       │   │   ├── conversation.py # Message models
│       │   │   ├── analysis.py # Analysis models
│       │   │   └── crisis.py   # Crisis models
│       │   ├── services/       # Business logic
│       │   │   ├── __init__.py
│       │   │   ├── claude_service.py # Claude integration
│       │   │   ├── conversation_service.py # Chat logic
│       │   │   ├── analysis_service.py # ChAT scoring
│       │   │   ├── crisis_service.py # Crisis detection
│       │   │   └── auth_service.py # Authentication
│       │   ├── repositories/   # Data access layer
│       │   │   ├── __init__.py
│       │   │   ├── base.py     # Base repository
│       │   │   ├── conversation.py # Conversation data
│       │   │   ├── user.py     # User data
│       │   │   ├── analysis.py # Analysis data
│       │   │   └── crisis.py   # Crisis data
│       │   ├── tasks/          # Celery tasks
│       │   │   ├── __init__.py
│       │   │   ├── analysis.py # Background analysis
│       │   │   └── notifications.py # User notifications
│       │   ├── utils/          # Utilities
│       │   │   ├── __init__.py
│       │   │   ├── validators.py # Input validation
│       │   │   ├── formatters.py # Data formatting
│       │   │   └── exceptions.py # Custom exceptions
│       │   ├── main.py         # FastAPI application
│       │   └── __init__.py
│       ├── tests/              # Backend tests
│       │   ├── conftest.py     # Test configuration
│       │   ├── test_auth.py    # Auth tests
│       │   ├── test_chat.py    # Chat API tests
│       │   ├── test_crisis.py  # Crisis detection tests
│       │   └── test_services/  # Service tests
│       ├── migrations/         # Database migrations
│       │   ├── alembic.ini     # Alembic configuration
│       │   ├── env.py          # Migration environment
│       │   └── versions/       # Migration files
│       ├── scripts/            # Utility scripts
│       │   ├── init_db.py      # Database initialization
│       │   └── seed_data.py    # Seed development data
│       ├── requirements.txt    # Python dependencies
│       ├── requirements-dev.txt # Development dependencies
│       ├── .python-version     # Python version specification
│       ├── uv.lock             # Lock file for reproducible installs
│       ├── Dockerfile          # Container configuration
│       ├── vercel.json         # Vercel deployment config
│       ├── .env.example        # Environment template
│       └── pyproject.toml      # Python project configuration
├── packages/                   # Shared packages
│   ├── shared/                 # Shared types/utilities
│   │   ├── src/
│   │   │   ├── types/          # TypeScript interfaces
│   │   │   │   ├── user.ts
│   │   │   │   ├── conversation.ts
│   │   │   │   ├── analysis.ts
│   │   │   │   └── crisis.ts
│   │   │   ├── constants/      # Shared constants
│   │   │   │   ├── goals.ts
│   │   │   │   ├── stages.ts
│   │   │   │   └── crisis-types.ts
│   │   │   └── utils/          # Shared utilities
│   │   │       ├── validation.ts
│   │   │       └── formatting.ts
│   │   └── package.json
│   └── config/                 # Shared configuration
│       ├── eslint/
│       │   └── next.js
│       ├── typescript/
│       │   └── base.json
│       └── tailwind/
│           └── base.js
├── infrastructure/             # Database migrations
│   ├── migrations/
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_rls_policies.sql
│   │   └── 003_job_queue.sql
│   ├── seed/
│   │   ├── development.sql
│   │   └── crisis_resources.sql
│   └── supabase/
│       ├── config.toml
│       └── functions/          # Edge functions (future)
├── scripts/                    # Build/deploy scripts
│   ├── setup.sh               # Local setup
│   ├── migrate.sh             # Database migrations
│   └── deploy.sh              # Deployment script
├── docs/                       # Documentation
│   ├── NORIA_PRD.md           # Product requirements
│   ├── NORIA_FULLSTACK_ARCHITECTURE.md # This document
│   └── api/                    # API documentation
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── package.json                # Root package.json
├── turbo.json                  # Turborepo configuration
└── README.md                   # Project overview
```
