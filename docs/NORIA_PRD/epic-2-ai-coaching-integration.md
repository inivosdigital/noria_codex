# Epic 2: AI Coaching Integration

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
