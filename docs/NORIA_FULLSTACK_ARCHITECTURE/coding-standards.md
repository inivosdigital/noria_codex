# Coding Standards

## Critical Fullstack Rules

- **Type Sharing:** Always define types in packages/shared and import from there - prevents frontend/backend type drift
- **API Error Handling:** All API routes must use consistent error response format with proper HTTP status codes
- **Database Queries:** Use Row Level Security (RLS) policies - never bypass with service role key in user-facing functions
- **Claude Integration:** Always include safety prompts and context limits - never send raw user input without coaching context
- **State Management:** Use Zustand stores for global state, React state for component-local state only
- **Crisis Detection:** All user messages must go through crisis detection before AI processing
- **Environment Variables:** Access config through validated environment schemas, never process.env directly
- **Authentication:** Use Supabase Auth helpers consistently - never manually verify JWTs

## Naming Conventions

| Element | Frontend | Backend | Example |
| :------ | :------- | :------ | :------ |
| Components | PascalCase | - | `ChatInterface.tsx` |
| Hooks | camelCase with 'use' | - | `useAuth.ts` |
| API Routes | - | kebab-case | `/api/chat/send` |
| Database Tables | - | snake_case | `conversations` |
| Database Columns | - | snake_case | `user_id`, `created_at` |
| Store Actions | camelCase | - | `sendMessage`, `updateProfile` |
| Types/Interfaces | PascalCase | PascalCase | `User`, `ConversationMessage` |
