# NORIA PRODUCT REQUIREMENTS DOCUMENT (PRD)

## Goals and Background Context

### Goals

• Graduate college students from AI dependency to authentic human relationships
• Provide evidence-based social coaching that builds real friendship skills 
• Create the first AI social platform designed to reduce rather than increase digital dependency
• Achieve 70% user graduation rate through measurable conversation quality improvement
• Establish sustainable business model focused on transformation outcomes rather than engagement metrics
• Validate novel 3-stage progression methodology (Individual → Small Group → Real World)

### Background Context

60% of college students experience severe loneliness despite being surrounded by peers. Current AI companion solutions (Replika, Character.AI) optimize for engagement and retention, creating digital dependency that worsens real-world social isolation rather than solving it. Noria addresses this by being the first AI social coaching platform designed to graduate users to authentic human relationships rather than create digital dependency.

Our evidence-based approach uses the ChAT (Conversational Human-likeness Assessment Tool) methodology to measure and improve conversation quality, helping users build genuine social confidence and friendship skills. Success is measured not by user retention, but by user graduation: students successfully completing our program and building meaningful real-world friendships, no longer needing our platform.

### Change Log

| Date | Version | Description | Author |
| :--- | :------ | :---------- | :----- |
| January 11, 2025 | 1.1 | Updated with Python FastAPI Architecture and MVP scope consensus | John |
| December 2024 | 1.0 | Initial PRD creation with comprehensive feature set | John |

## Requirements

### Functional

- FR1: The system shall provide secure user account creation and authentication using email/password
- FR2: The system shall maintain persistent WhatsApp-style conversation threads between users and AI coach
- FR3: The system shall integrate Claude Sonnet 4 API for personalized social coaching responses
- FR4: The system shall analyze conversation quality using Claude-based ChAT scoring methodology
- FR5: The system shall track ChAT scores internally without displaying them to users during MVP phase
- FR6: The system shall provide encouraging progress messages when conversation improvement is detected
- FR7: The system shall implement real-time crisis keyword detection with immediate resource display
- FR8: The system shall allow users to select from predefined social goals during onboarding
- FR9: The system shall determine Stage 1 graduation readiness based on sustained ChAT score improvement (10.5+/14)
- FR10: The system shall provide static wellness resource library accessible to all users
- FR11: The system shall process background conversation analysis every 25 messages
- FR12: The system shall maintain conversation history with infinite scroll functionality
- FR13: The system shall provide crisis escalation protocols when concerning patterns are detected

### Non Functional

- NFR1: Message response latency **must** be under 2 seconds under normal conditions
- NFR2: The system **must** handle 10,000+ concurrent users through serverless architecture
- NFR3: PWA **must** start up in under 3 seconds from home screen installation
- NFR4: Data encryption **must** be implemented for all personal conversations
- NFR5: COPPA and HIPAA-adjacent compliance **must** be maintained for wellness data handling
- NFR6: Claude API costs **must** be monitored with budget protection and usage caps
- NFR7: Crisis detection false positive rate **must** be under 10%
- NFR8: System availability **must** be 99.5% uptime for core chat functionality
- NFR9: Mobile-first design **must** be optimized for college student usage patterns
- NFR10: Accessibility **must** meet WCAG 2.1 AA compliance standards

## User Interface Design Goals

### Overall UX Vision

Noria provides a clean, mobile-first coaching experience that clearly distinguishes itself from AI companionship apps. The interface emphasizes clarity, progress, and motivation without manipulation. Users should feel they're engaging with a professional coach, not a digital friend, with every interaction building toward real-world social confidence.

### Key Interaction Paradigms

- **WhatsApp-Style Conversation**: Single persistent thread between user and AI coach for natural, continuous coaching dialogue
- **Implicit Progress Feedback**: Progress communicated through improved coaching quality and encouraging messages rather than gamified dashboards
- **Crisis-Aware Design**: Immediate resource overlays when safety concerns are detected without disrupting conversation flow
- **Coaching Clarity**: Clear visual distinction from companion apps through professional coaching branding and messaging

### Core Screens and Views

- Welcome & Onboarding Flow (coaching model explanation, goal selection, agreement)
- Main Chat Interface (persistent conversation with Noria AI coach)
- Profile Management (goals, privacy settings, account info)
- Wellness Resource Library (mental health resources, crisis helplines)
- Crisis Support Overlay (immediate resources when triggered)

### Accessibility: WCAG 2.1 AA

Full compliance with WCAG 2.1 AA standards to ensure inclusive access for all college students, including those with visual, auditory, motor, or cognitive disabilities.

### Branding

Professional coaching aesthetic that clearly differentiates from entertainment AI companions:
- Clean, clinical interface design suggesting professional development
- "Noria - Your AI Coach" branding (never friend/companion)
- Encouraging but not manipulative progress messaging
- Evidence-based methodology communicated through design choices

### Target Device and Platforms

Web Progressive Web App (PWA) optimized for mobile-first usage across iOS Safari, Android Chrome, and desktop browsers. PWA features include home screen installation, push notifications, and offline message queuing.

## Technical Assumptions

### Repository Structure: Monorepo

Single repository containing both frontend and backend components for simplified development and deployment coordination.

### Service Architecture

**MVP Architecture**: Next.js PWA frontend + Python FastAPI backend with serverless deployment
- **Frontend**: Next.js 15 PWA with Vercel deployment
- **Backend**: Python FastAPI with Vercel Functions
- **Database**: Supabase (PostgreSQL + Real-time + Auth)
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
- **Real-time Features**: WebSocket support through Supabase for live conversation updates

## Epics

### Epic List

1. **Foundation & Core Infrastructure**: Establish project setup, database, authentication, and basic chat functionality
2. **AI Coaching Integration**: Implement Claude API integration with personalized coaching and background analysis
3. **Safety & Crisis Detection**: Build comprehensive crisis detection and resource systems
4. **Progress Tracking & Graduation**: Implement ChAT scoring analysis and Stage 1 graduation system

## Epic 1: Foundation & Core Infrastructure

Establish the foundational technical infrastructure including database schema, user authentication, and basic chat interface to enable core platform functionality and provide immediate value through functional user account management and conversation capability.

### Story 1.1: Database Foundation & User Management

As a system administrator,
I want to establish core database infrastructure and user account functionality,
so that users can create accounts and the platform can store essential user data.

#### Acceptance Criteria

- 1.1.1: PostgreSQL database connection established via local Docker container (Supabase-compatible for deployment)
- 1.1.2: User table schema created (id, email, password_hash, created_at, goals, stage_status)
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

## Epic 2: AI Coaching Integration

Integrate Claude Sonnet 4 API to provide personalized social coaching responses and implement background conversation analysis using ChAT methodology to track user progress and improve coaching effectiveness over time.

### Story 2.1: Claude API Integration

As a system,
I want to establish reliable connection to Claude Sonnet 4 API,
so that I can generate personalized coaching responses for users.

#### Acceptance Criteria

- 2.1.1: Claude Sonnet 4 API connection established and tested
- 2.1.2: API key authentication configured securely with environment variables
- 2.1.3: Rate limiting implemented for Claude API to prevent overuse
- 2.1.4: Error handling for API failures with graceful fallback responses
- 2.1.5: Async operation patterns implemented for scalability
- 2.1.6: Cost monitoring and usage tracking for budget protection

### Story 2.2: Personalized Coaching Responses

As a user,
I want to receive personalized coaching responses that address my specific social goals,
so that the guidance I receive is relevant and helpful for my situation.

#### Acceptance Criteria

- 2.2.1: User goals automatically incorporated into Claude system prompts
- 2.2.2: Safety guidelines and coaching methodology embedded in prompts
- 2.2.3: User messages sent to Claude with personalized context
- 2.2.4: Claude responses received, parsed, and displayed as Noria messages
- 2.2.5: Typing indicator shows while generating response
- 2.2.6: Response time under 2 seconds for normal conversations

### Story 2.3: Goal Selection Onboarding

As a new user,
I want to select my social coaching goals during onboarding,
so that my coaching experience is personalized from the first conversation.

#### Acceptance Criteria

- 2.3.1: Welcome screen explaining coaching model vs AI companionship
- 2.3.2: 3-stage journey visualization (Individual → Group → Real World)
- 2.3.3: Predefined social goals list (8-10 relevant options for college students)
- 2.3.4: Custom goal input field for specific user needs
- 2.3.5: Multiple goal selection capability
- 2.3.6: Goal data stored in user profile for coaching personalization
- 2.3.7: Coaching agreement terms with explicit consent checkbox

### Story 2.4: Background ChAT Analysis

As a system,
I want to analyze conversations using ChAT methodology every 25 messages,
so that I can track user progress internally and provide encouraging feedback.

#### Acceptance Criteria

- 2.4.1: Analysis triggered automatically every 25 messages
- 2.4.2: Claude-based conversation analysis using ChAT methodology prompts
- 2.4.3: Conversation segments formatted appropriately for Claude analysis
- 2.4.4: ChAT scores (0-14) generated and parsed from Claude responses
- 2.4.5: Scores stored with timestamp, message range, and analysis insights
- 2.4.6: Background processing remains invisible to user experience
- 2.4.7: Encouraging messages sent when improvement detected

## Epic 3: Safety & Crisis Detection

Implement comprehensive safety systems including real-time crisis detection, resource provision, and conversation safety guardrails to ensure user wellbeing and appropriate coaching boundaries throughout the platform experience.

### Story 3.1: Crisis Keyword Detection

As a system,
I want to detect crisis indicators in user messages in real-time,
so that I can immediately provide appropriate support resources when users are in distress.

#### Acceptance Criteria

- 3.1.1: Real-time keyword analysis on every user message send
- 3.1.2: Crisis indicator detection (suicide, self-harm, abuse, severe depression keywords)
- 3.1.3: Immediate crisis resource overlay displayed within conversation
- 3.1.4: Crisis events logged with severity level for follow-up review
- 3.1.5: False positive rate maintained under 10%
- 3.1.6: Resource overlay includes crisis helplines and emergency contacts

### Story 3.2: Wellness Resource Library

As a user,
I want to access mental health resources and wellness content,
so that I have additional support options beyond my coaching conversations.

#### Acceptance Criteria

- 3.2.1: Curated mental health resource library accessible from navigation
- 3.2.2: Crisis helpline numbers and websites prominently displayed
- 3.2.3: Resource categorization (anxiety, depression, social skills, emergency)
- 3.2.4: External resource linking with proper attribution
- 3.2.5: Resources regularly updated and validated for accuracy
- 3.2.6: Quick access to resources from crisis detection overlay

### Story 3.3: Conversation Safety Guardrails

As a system,
I want to maintain safe conversation boundaries and detect concerning AI responses,
so that coaching stays appropriate and users receive helpful rather than harmful guidance.

#### Acceptance Criteria

- 3.3.1: Pre-send analysis of Claude responses for harmful content
- 3.3.2: Alternative response generation if primary response is problematic  
- 3.3.3: Safety guardrails prevent therapeutic overreach or clinical advice
- 3.3.4: Response safety incidents logged and reviewed
- 3.3.5: Gentle redirection when conversation drifts into inappropriate territory
- 3.3.6: Professional referral triggers for complex mental health concerns

## Epic 4: Progress Tracking & Graduation

Implement ChAT score trend analysis and Stage 1 graduation system to measure user progress, determine coaching completion readiness, and celebrate transformation achievements while preparing users for real-world application.

### Story 4.1: Progress Trend Analysis

As a system,
I want to calculate ChAT score trends across multiple conversation sessions,
so that I can measure user improvement and predict graduation readiness.

#### Acceptance Criteria

- 4.1.1: ChAT score trending algorithm using minimum 3 analysis sessions
- 4.1.2: Improvement velocity calculation across time periods
- 4.1.3: Pattern recognition for consistent upward improvement
- 4.1.4: Trend data stored for graduation decision making
- 4.1.5: Conversation quality progression tracking
- 4.1.6: Goal progress mapping from conversation content

### Story 4.2: Implicit Progress Communication

As a user,
I want to experience my progress through improved coaching quality and encouraging messages,
so that I feel motivated and aware of my growth without focusing on metrics.

#### Acceptance Criteria

- 4.2.1: NO visual charts, dashboards, or progress bars displayed to users
- 4.2.2: NO ChAT scores shown to users (internal tracking only)
- 4.2.3: Encouraging messages like "Your conversations are getting more natural!"
- 4.2.4: Progress felt through improved coaching conversation quality
- 4.2.5: Milestone achievements communicated through chat messages only
- 4.2.6: Natural, conversational celebration of improvements

### Story 4.3: Stage 1 Graduation System

As a user,
I want to be recognized when I've mastered individual coaching conversations,
so that I can celebrate my achievement and understand my readiness for real-world application.

#### Acceptance Criteria

- 4.3.1: ChAT score threshold sustained (10.5+/14 average across 5 recent analyses)
- 4.3.2: Minimum coaching duration requirement (3-4 weeks active engagement)
- 4.3.3: Consistent upward ChAT score improvement trajectory validation
- 4.3.4: Graduation readiness notification in chat: "Your conversation skills have reached Stage 2 readiness!"
- 4.3.5: Stage 1 completion celebration message sequence
- 4.3.6: Before/after ChAT score visualization showing improvement journey
- 4.3.7: Evidence portfolio displaying conversation quality progress
- 4.3.8: Stage 2 introduction and preparation content
- 4.3.9: "Stage 2 Ready" status displayed in profile
- 4.3.10: Educational materials about future group coaching concepts

## Checklist Results Report

*PM Checklist execution pending - will be completed after user approval of PRD structure*

## Next Steps

### Design Architect Prompt

"Please review this Noria PRD and create the UI/UX design architecture. Focus on mobile-first PWA design that clearly differentiates coaching from AI companionship, emphasizing professional development aesthetic with implicit progress feedback through conversation quality rather than gamified dashboards."

### Architect Prompt

"Please review this Noria PRD and create the technical architecture. Implement Python FastAPI backend with Next.js PWA frontend, focusing on Claude Sonnet 4 integration, ChAT-based conversation analysis, crisis detection systems, and scalable infrastructure supporting the specified epic and story sequence."
