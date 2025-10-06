# Testing Strategy

## Testing Pyramid

```
        E2E Tests (10%)
       /                \
    Integration Tests (20%)
   /                        \
Frontend Unit (35%)    Backend Unit (35%)
```

## Real Data Policy

Integration and end-to-end suites MUST exercise the actual application stack running locally (Next.js + FastAPI + Supabase). Do not stub domain data or swap in fake service responses when validating end-to-end behaviour. Seed data using the documented migration/seed workflow and interact through public APIs. Only unit-level tests may use mocks or fakes to isolate logic.

## Test Organization

**Frontend Tests:**

```
tests/
├── components/           # Component unit tests
│   ├── ChatInterface.test.tsx
│   ├── MessageInput.test.tsx
│   └── CrisisOverlay.test.tsx
├── hooks/               # Custom hook tests
│   ├── useAuth.test.ts
│   └── useChat.test.ts
├── services/            # Service layer tests
│   ├── chatService.test.ts
│   └── userService.test.ts
└── stores/              # State management tests
    ├── authStore.test.ts
    └── chatStore.test.ts
```

**Backend Tests:**

```
tests/api/
├── auth/
│   ├── signup.test.ts
│   └── profile.test.ts
├── chat/
│   ├── send.test.ts
│   ├── history.test.ts
│   └── analysis.test.ts
└── crisis/
    ├── detect.test.ts
    └── resources.test.ts
```

**E2E Tests:**

```
tests/e2e/
├── auth-flow.spec.ts         # Registration and login
├── coaching-conversation.spec.ts # Complete coaching flow
├── crisis-detection.spec.ts      # Crisis handling
└── graduation-flow.spec.ts       # Full user journey to graduation
```

## Test Examples

**Frontend Component Test:**

```typescript
// tests/components/ChatInterface.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChatInterface } from '@/components/chat/ChatInterface';
import { chatService } from '@/services/chatService';

jest.mock('@/services/chatService');
const mockChatService = chatService as jest.Mocked<typeof chatService>;

describe('ChatInterface', () => {
  it('sends message and displays response', async () => {
    const mockResponse = {
      userMessage: { id: '1', text: 'Hello', sender_type: 'user' },
      assistantMessage: { id: '2', text: 'Hi there!', sender_type: 'assistant' },
      crisis_detected: false
    };
    
    mockChatService.sendMessage.mockResolvedValue(mockResponse);

    render(<ChatInterface userId="user-1" />);
    
    const input = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: 'Send' });
    
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.click(sendButton);
    
    await waitFor(() => {
      expect(screen.getByText('Hello')).toBeInTheDocument();
      expect(screen.getByText('Hi there!')).toBeInTheDocument();
    });
    
    expect(mockChatService.sendMessage).toHaveBeenCalledWith('Hello');
  });
});
```

**Backend API Test:**

```typescript
// tests/api/chat/send.test.ts
import { createMocks } from 'node-mocks-http';
import { POST } from '@/app/api/chat/send/route';

jest.mock('@/lib/claudeService');
jest.mock('@supabase/auth-helpers-nextjs');

describe('/api/chat/send', () => {
  it('processes message and returns response', async () => {
    const { req } = createMocks({
      method: 'POST',
      body: { message: 'Hello coach' },
    });

    const response = await POST(req);
    const data = await response.json();
    
    expect(response.status).toBe(200);
    expect(data).toHaveProperty('userMessage');
    expect(data).toHaveProperty('assistantMessage');
    expect(data.crisis_detected).toBe(false);
  });

  it('handles crisis detection', async () => {
    const { req } = createMocks({
      method: 'POST',
      body: { message: 'I want to hurt myself' },
    });

    const response = await POST(req);
    const data = await response.json();
    
    expect(data.crisis_detected).toBe(true);
    expect(data.resources).toHaveLength(greaterThan(0));
  });
});
```

**E2E Test:**

```typescript
// tests/e2e/coaching-conversation.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Coaching Conversation Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock authentication
    await page.goto('/chat');
    // Assume user is already authenticated
  });

  test('complete coaching conversation with progress', async ({ page }) => {
    // Send initial message
    await page.fill('[data-testid="message-input"]', 'I feel lonely at college');
    await page.click('[data-testid="send-button"]');

    // Wait for AI response
    await expect(page.locator('[data-testid="message"]').last()).toContainText('understand');

    // Continue conversation
    await page.fill('[data-testid="message-input"]', 'Yes, I struggle with making friends');
    await page.click('[data-testid="send-button"]');

    // Check that messages are saved and displayed
    await expect(page.locator('[data-testid="message"]')).toHaveCount(4); // 2 user + 2 assistant

    // Wait for background analysis job (Supabase pg-boss worker) to complete
    await page.waitForTimeout(2000);
    await expect(page.locator('[data-testid="progress-badge"]').first()).toBeVisible();
  });

  test('crisis detection and resource display', async ({ page }) => {
    await page.fill('[data-testid="message-input"]', 'I want to end it all');
    await page.click('[data-testid="send-button"]');

    // Crisis overlay should appear
    await expect(page.locator('[data-testid="crisis-overlay"]')).toBeVisible();
    
    // Resources should be displayed
    await expect(page.locator('[data-testid="crisis-resource"]')).toHaveCount(greaterThan(0));
    
    // User can acknowledge
    await page.click('[data-testid="acknowledge-button"]');
    await expect(page.locator('[data-testid="crisis-overlay"]')).not.toBeVisible();
  });
});
```
## Tooling Setup

Install test tooling immediately after the Day-0 bootstrap so stories can rely on a consistent harness.

```bash
# Frontend packages
pnpm --filter web add -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/user-event
pnpm --filter web add -D playwright @playwright/test axe-core

# Backend packages
uv run --cwd apps/api pip install --upgrade pytest pytest-asyncio pytest-cov httpx respx factory-boy

# Shared lint/test scripts
pnpm pkg set scripts.test="turbo run test"
pnpm pkg set scripts.test:e2e="playwright test"
```

These commands belong in Story 1.0 acceptance testing steps so they execute before feature development begins.

## Test Environment Configuration

- **Frontend:** Vitest config lives at `apps/web/vitest.config.ts`; alias `@/*` matches Next.js imports. Add `setupTests.ts` to register Testing Library helpers and bootstrap the Supabase client (no mocks in integration suites).
- **Backend:** `apps/api/pytest.ini` configures async markers and points to `tests/conftest.py`, which boots a transactional PostgreSQL database via the local Docker Compose service and yields session fixtures.
- **E2E:** `apps/web/playwright.config.ts` reads `NEXT_PUBLIC_API_URL` from `.env`. Playwright tests run against local servers (`pnpm --filter web dev` + `uvicorn`) with the Dockerized Postgres service.

## Unit-Test Fakes (Allowed for Isolation Only)

- **Claude API:** Unit tests may use `services/integrations/fakes/claude.ts` to simulate edge cases. Integration/e2e tests must call the real Claude adapter hitting the local queue/worker pipeline.
- **Supabase Auth:** Use `tests/mocks/supabase_auth.ts` only in component/unit tests; integration suites rely on actual Supabase sessions.
- **Realtime events:** `tests/fixtures/ws_client.ts` can simulate WebSocket payloads in unit scenarios. End-to-end tests should observe messages through the real Supabase channel.
- **Seed data:** `tests/fixtures/seed.sql` primes users, goals, and crisis resources. Load via `supabase db reset --seed` in test setup scripts.

Document new mocks or fixtures in this section whenever integrations change, keeping the checklist traceable for QA.
