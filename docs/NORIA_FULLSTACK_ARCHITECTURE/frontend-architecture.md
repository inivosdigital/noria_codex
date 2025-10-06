# Frontend Architecture

## Component Architecture

**Component Organization:**

```
src/
├── app/                        # Next.js 15 App Router
│   ├── (auth)/                # Auth route group
│   │   ├── login/
│   │   └── signup/
│   ├── chat/                  # Main chat interface
│   ├── onboarding/            # Goal selection flow
│   ├── profile/               # User settings
│   └── wellness/              # Resources
├── components/                # Reusable components
│   ├── ui/                    # shadcn/ui components
│   ├── chat/                  # Chat-specific components
│   ├── forms/                 # Form components
│   └── layout/                # Layout components
├── hooks/                     # Custom React hooks
├── services/                  # API client services
├── stores/                    # Zustand stores
├── lib/                       # Utilities and configuration
└── types/                     # TypeScript definitions
```

## Design System Foundations

### Tokens & Theming

- **Color Palette:**
  - Primary: `hsl(212, 92%, 43%)`
  - Secondary: `hsl(163, 64%, 44%)`
  - Accent: `hsl(39, 84%, 57%)`
  - Neutral Surface: `hsl(215, 16%, 24%)`
  - Neutral Text: `hsl(210, 20%, 98%)`
- **Typography:** Inter for body text, Space Grotesk for headings (configure via Tailwind `fontFamily`).
- **Radius & Spacing:** Use shadcn defaults (`--radius: 0.75rem`) with Tailwind 4px spacing scale.
- **Dark Mode:** Default to dark theme; add `<ThemeProvider attribute="class">` in `layout.tsx`.

Tokens live in `apps/web/styles/tokens.css` and sync with Tailwind variables.

### shadcn/ui Workflow

1. Add primitives using `pnpm dlx shadcn-ui@latest add <component>`.
2. Store base primitives under `components/ui/` and compose feature components in domain folders.
3. Document new components in `docs/ui/components.md` with usage instructions.
4. Run `pnpm lint` and `pnpm --filter web test` after additions to ensure consistency.

## Visual Asset & Performance Strategy

- Use Next.js `<Image>` for media; configure allowed domains in `next.config.js`.
- Keep large UI chunks lazy-loaded via `React.lazy` to benefit from route-level code splitting.
- Tailwind purge runs automatically; ensure new directories are added to the `content` array.
- Preload core fonts with `next/font/google`.
- Serve icons via Lucide (bundled with shadcn) to avoid custom sprite hosting.

## Form Patterns & Validation

- Use React Hook Form + Zod; schemas live in `lib/validation/`.
- Display errors with shadcn `<FormMessage>` and consistent helper text.
- Mirror constraints on the backend so Supabase errors map cleanly to UI messages.
- For multi-step forms, persist intermediate state in Zustand stores.

## Component Contribution Workflow

1. Build component + tests in feature folder.
2. Document usage (MDX snippet) in `docs/ui/components.md`.
3. Run `pnpm --filter web test`, `pnpm --filter web test:a11y`, and `pnpm lint`.
4. Request UX review on PRs to maintain design fidelity.

**Component Template:**

```typescript
'use client'

import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { chatService } from '@/services/chatService';

interface ChatInterfaceProps {
  userId: string;
  initialMessages?: Message[];
}

export function ChatInterface({ userId, initialMessages = [] }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  const sendMessage = async (text: string) => {
    setLoading(true);
    try {
      const response = await chatService.sendMessage(text);
      setMessages(prev => [...prev, response.userMessage, response.assistantMessage]);
      
      // Handle crisis detection
      if (response.crisis_detected) {
        // Show crisis resources overlay
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <MessageList messages={messages} />
      <MessageInput onSend={sendMessage} disabled={loading} />
    </div>
  );
}
```

## State Management Architecture

**State Structure:**

```typescript
// stores/authStore.ts
interface AuthState {
  user: User | null;
  session: Session | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  updateProfile: (updates: Partial<UserProfile>) => Promise<void>;
}

// stores/chatStore.ts
interface ChatState {
  messages: Message[];
  isTyping: boolean;
  connectionStatus: 'connected' | 'connecting' | 'disconnected';
  addMessage: (message: Message) => void;
  setTyping: (isTyping: boolean) => void;
  loadHistory: (limit?: number) => Promise<void>;
}

// stores/progressStore.ts
interface ProgressState {
  currentStage: CoachingStage;
  recentAnalysis: AnalysisResult | null;
  milestones: Milestone[];
  showMilestone: (milestone: Milestone) => void;
  updateStage: (stage: CoachingStage) => void;
}
```

**State Management Patterns:**

- Separate stores for different domains (auth, chat, progress)
- Persistent storage for auth state using localStorage
- WebSocket integration for real-time chat updates
- Optimistic updates for better UX

## Routing Architecture

**Route Organization:**

```
app/
├── page.tsx                   # Home redirect to /chat
├── (auth)/
│   ├── layout.tsx            # Auth-specific layout
│   ├── login/page.tsx        # Login form
│   └── signup/page.tsx       # Registration + onboarding
├── chat/
│   └── page.tsx              # Main chat interface
├── onboarding/
│   ├── page.tsx              # Goal selection
│   ├── goals/page.tsx        # Goal customization
│   └── agreement/page.tsx    # Coaching agreement
├── profile/
│   └── page.tsx              # User settings
├── wellness/
│   └── page.tsx              # Crisis resources
└── layout.tsx                # Root layout with PWA setup
```

**Protected Route Pattern:**

```typescript
// middleware.ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const supabase = createMiddlewareClient({ req, res });

  const { data: { session } } = await supabase.auth.getSession();
  
  const isAuthPage = req.nextUrl.pathname.startsWith('/login') || 
                     req.nextUrl.pathname.startsWith('/signup');
  const isProtectedPage = req.nextUrl.pathname.startsWith('/chat') ||
                          req.nextUrl.pathname.startsWith('/profile');

  // Redirect unauthenticated users to login
  if (isProtectedPage && !session) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  // Redirect authenticated users away from auth pages
  if (isAuthPage && session) {
    return NextResponse.redirect(new URL('/chat', req.url));
  }

  return res;
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

## Frontend Services Layer

**API Client Setup:**

```typescript
// lib/supabase.ts
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';

export const supabase = createClientComponentClient();

// services/apiClient.ts
class ApiClient {
  private baseURL = process.env.NEXT_PUBLIC_API_URL || '/api';

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const { data: { session } } = await supabase.auth.getSession();
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(session && { Authorization: `Bearer ${session.access_token}` }),
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }
}

export const apiClient = new ApiClient();
```

**Service Example:**

```typescript
// services/chatService.ts
interface SendMessageResponse {
  userMessage: Message;
  assistantMessage: Message;
  crisis_detected: boolean;
  resources?: CrisisResource[];
}

class ChatService {
  async sendMessage(text: string): Promise<SendMessageResponse> {
    return apiClient.request<SendMessageResponse>('/chat/send', {
      method: 'POST',
      body: JSON.stringify({ message: text }),
    });
  }

  async getHistory(limit = 50, before?: string): Promise<Message[]> {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (before) params.append('before', before);
    
    const response = await apiClient.request<{ messages: Message[] }>(
      `/chat/history?${params}`
    );
    return response.messages;
  }

  // WebSocket connection for real-time updates
  subscribeToMessages(userId: string, callback: (message: Message) => void) {
    return supabase
      .channel('conversations')
      .on('postgres_changes', 
        { event: 'INSERT', schema: 'public', table: 'conversations', filter: `user_id=eq.${userId}` },
        (payload) => callback(payload.new as Message)
      )
      .subscribe();
  }
}

export const chatService = new ChatService();
```
