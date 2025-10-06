# Epic 3: Safety & Crisis Detection

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
