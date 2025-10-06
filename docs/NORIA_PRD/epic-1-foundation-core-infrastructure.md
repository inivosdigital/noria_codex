# Epic 1: Foundation & Core Infrastructure

Establish the foundational technical infrastructure including database schema, user authentication, and basic chat interface to enable core platform functionality and provide immediate value through functional user account management and conversation capability.

### Story 1.0: Project Initialization & Repository Setup

As a project maintainer,
I want to establish the base mono-repo scaffolding and documentation,
so that subsequent stories can build on a consistent architecture-aligned foundation.

#### Acceptance Criteria

- 1.0.1: Turborepo workspace initialized with folders matching the structure defined in docs/NORIA_FULLSTACK_ARCHITECTURE/unified-project-structure.md.
- 1.0.2: Next.js app scaffolded under apps/web with placeholder routes, layout, and configuration files aligned to the architecture plan.
- 1.0.3: FastAPI service scaffolded under apps/api with minimal app entrypoint, dependency files, and configuration matching the architecture.
- 1.0.4: Shared packages (packages/shared and packages/config) created with placeholder exports and package metadata to enable reuse.
- 1.0.5: Baseline repository configuration committed including .gitignore, README.md stub, turbo.json, package.json, and environment template files.
- 1.0.6: docs/NORIA_FULLSTACK_ARCHITECTURE/development-workflow.md updated with reproducible local setup steps and prerequisite tooling.
- 1.0.7: Initial commit or branch records the scaffolding so future work starts from a clean state.

### Story 1.1: Database Foundation & User Management

As a system administrator,
I want to establish core database infrastructure and user account functionality,
so that users can create accounts and the platform can store essential user data.

#### Acceptance Criteria

- 1.1.1: PostgreSQL database connection established via local Docker container (Supabase-compatible for deployment)
- 1.1.2: User table schema created (id, email, password_hash, created_at, goals, stage)
- 1.1.3: Conversation table schema created (id, user_id, message_text, timestamp, sender_type)
- 1.1.4: Analysis table schema created (id, user_id, chat_score, timestamp, message_range)
- 1.1.5: Basic CRUD operations tested and working
- 1.1.6: Account creation form with email/password validation
- 1.1.7: Password requirements enforced (8+ chars, mixed case, numbers)

### Story 1.2: Authentication System

As a user,
I want to securely log in and out of my account,
so that I can access my personal coaching conversations safely.

#### Acceptance Criteria

- 1.2.1: Login form with email/password authentication
- 1.2.2: Password verification against hash with secure session token generation
- 1.2.3: Session timeout configured for 24 hours
- 1.2.4: Logout functionality clearing session properly
- 1.2.5: Password reset flow with secure token generation and email delivery
- 1.2.6: Authentication guards protecting all user-specific routes

### Story 1.3: Basic Chat Interface

As a user,
I want to access a clean chat interface immediately after login,
so that I can start my coaching conversation with Noria.

#### Acceptance Criteria

- 1.3.1: App opens directly to persistent chat interface after authentication
- 1.3.2: Clear "Noria - Your AI Coach" header distinguishing from companion apps
- 1.3.3: Message input field with send button functionality
- 1.3.4: Basic message display with user messages on right, system messages on left
- 1.3.5: Messages stored in database with proper timestamp and sender identification
- 1.3.6: Infinite scroll loading of conversation history (50 messages per batch)

### Story 1.4: Navigation & Profile Management

As a user,
I want to navigate between core app screens and manage my profile information,
so that I can control my account settings and access different platform features.

#### Acceptance Criteria

- 1.4.1: Bottom navigation bar with Chat, Profile, and Resources screens
- 1.4.2: Active screen highlighting in navigation
- 1.4.3: Profile screen displaying current goals, stage status, and account info
- 1.4.4: Goal editing functionality with save confirmation
- 1.4.5: Privacy settings for data usage and sharing preferences
- 1.4.6: Account deletion option with confirmation flow
