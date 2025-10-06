# Data Models

## User

**Purpose:** Represents authenticated users (college students) in the coaching system

**Key Attributes:**

- id: string (UUID) - Unique identifier from Supabase Auth
- email: string - University email address
- goals: string[] - Selected social coaching goals
- stage: enum - Current coaching stage (1, 2, 3, graduated)
- created_at: timestamp - Account creation
- last_active: timestamp - Last conversation activity
- graduation_date: timestamp? - When user completed coaching

**TypeScript Interface:**

```typescript
interface User {
  id: string; // Supabase Auth UUID
  email: string;
  goals: SocialGoal[];
  stage: CoachingStage;
  profile: UserProfile;
  preferences: UserPreferences;
  created_at: string;
  updated_at: string;
  last_active: string;
  graduation_date?: string;
}

interface UserProfile {
  university?: string;
  year_in_school?: string;
  timezone?: string;
}

interface UserPreferences {
  crisis_resources_acknowledged: boolean;
  coaching_style: 'encouraging' | 'direct' | 'gentle';
  notification_preferences: NotificationSettings;
}

type SocialGoal = 
  | 'build_confidence'
  | 'make_friends'
  | 'improve_conversations'
  | 'overcome_anxiety'
  | 'join_activities'
  | 'dating_skills'
  | 'roommate_relations';

type CoachingStage = 1 | 2 | 3 | 'graduated';
```

**Relationships:**

- Has many Conversations (1:n)
- Has many AnalysisResults (1:n)
- Has many CrisisEvents (1:n)

## Conversation

**Purpose:** Stores all messages between users and Noria AI coach for persistent chat history

**Key Attributes:**

- id: string (UUID) - Unique message identifier
- user_id: string - Foreign key to User
- message_text: string - Message content
- sender_type: enum - 'user' or 'assistant'
- timestamp: timestamp - Message creation time
- message_metadata: json - Additional context (emotion, intent, etc.)

**TypeScript Interface:**

```typescript
interface Conversation {
  id: string;
  user_id: string;
  message_text: string;
  sender_type: 'user' | 'assistant';
  timestamp: string;
  message_metadata: MessageMetadata;
  analysis_included: boolean; // Whether this message was included in ChAT analysis
}

interface MessageMetadata {
  emotion_detected?: string;
  intent_category?: string;
  crisis_keywords?: string[];
  coaching_topic?: string;
  response_time_ms?: number;
}
```

**Relationships:**

- Belongs to User (n:1)
- Referenced by AnalysisResults (n:m)

## AnalysisResult

**Purpose:** Stores ChAT scoring results and coaching insights from conversation analysis

**Key Attributes:**

- id: string (UUID) - Unique analysis identifier
- user_id: string - Foreign key to User
- chat_score: number - ChAT score (0-14)
- analysis_type: enum - Type of analysis performed
- message_range: json - Range of messages analyzed
- insights: json - Structured analysis insights
- timestamp: timestamp - When analysis was performed

**TypeScript Interface:**

```typescript
interface AnalysisResult {
  id: string;
  user_id: string;
  chat_score: number; // 0-14 scale
  analysis_type: AnalysisType;
  message_range: MessageRange;
  insights: AnalysisInsights;
  improvement_areas: string[];
  strengths_identified: string[];
  timestamp: string;
  triggered_milestone: boolean;
}

interface MessageRange {
  start_message_id: string;
  end_message_id: string;
  total_messages: number;
  analysis_window: string; // e.g., "last_25_messages"
}

interface AnalysisInsights {
  conversation_quality: ConversationQuality;
  social_skills_progress: SocialSkillsProgress;
  coaching_effectiveness: CoachingEffectiveness;
}

interface ConversationQuality {
  naturalness_score: number;
  engagement_level: number;
  emotional_awareness: number;
  question_asking: number;
}

type AnalysisType = 'chat_scoring' | 'milestone_check' | 'graduation_assessment' | 'crisis_review';
```

**Relationships:**

- Belongs to User (n:1)
- References Conversation messages (n:m)

## CrisisEvent

**Purpose:** Tracks crisis detection events and safety interventions for user protection

**Key Attributes:**

- id: string (UUID) - Unique crisis identifier
- user_id: string - Foreign key to User
- trigger_type: enum - What triggered the crisis detection
- severity_level: enum - Assessed severity level
- message_id: string - Message that triggered detection
- resources_shown: json - Which resources were displayed
- timestamp: timestamp - When crisis was detected

**TypeScript Interface:**

```typescript
interface CrisisEvent {
  id: string;
  user_id: string;
  trigger_type: CrisisType;
  severity_level: SeverityLevel;
  message_id: string;
  keywords_detected: string[];
  resources_shown: CrisisResource[];
  user_acknowledged: boolean;
  followup_required: boolean;
  timestamp: string;
  resolution_timestamp?: string;
}

type CrisisType = 
  | 'suicide_ideation'
  | 'self_harm'
  | 'severe_depression'
  | 'abuse_disclosure'
  | 'eating_disorder'
  | 'substance_abuse';

type SeverityLevel = 'low' | 'moderate' | 'high' | 'critical';

interface CrisisResource {
  type: 'hotline' | 'chat' | 'text' | 'website';
  name: string;
  contact: string;
  description: string;
  availability: string;
}
```

**Relationships:**

- Belongs to User (n:1)
- References specific Conversation message (n:1)
