# Requirements

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
