# Security and Performance

## Security Requirements

**Frontend Security:**

- CSP Headers: `script-src 'self' 'unsafe-inline' *.vercel.app; object-src 'none';`
- XSS Prevention: Content sanitization, React's built-in protections
- Secure Storage: JWT tokens in httpOnly cookies, sensitive data in secure storage

**Backend Security:**

- Input Validation: Joi/Zod schemas for all API inputs
- Rate Limiting: 100 requests/minute per user, 10 requests/minute for auth endpoints
- CORS Policy: Restricted to app domains only
- Conversation Data Encryption: Encrypt conversation text, analysis insights, and crisis notes at the FastAPI layer using Fernet (AES-256) with keys sourced from Vercel encrypted environment variables (future upgrade path: AWS KMS). Rotate keys quarterly; store key IDs alongside ciphertext for re-encryption during rotation.

**Authentication Security:**

- Token Storage: JWT in secure, httpOnly cookies with SameSite=Strict
- Session Management: Auto-refresh tokens, 24-hour session expiry
- Password Policy: Minimum 8 characters, mixed case, numbers required

## Performance Optimization

**Frontend Performance:**

- Bundle Size Target: <300KB main bundle, <100KB per route
- Loading Strategy: Lazy loading for non-critical components, code splitting by route
- Caching Strategy: SWR for API calls, service worker for offline capability
- **CI Lighthouse Budget:** Run Lighthouse (or Next.js Analysis) in CI with performance budgets (LCP ≤ 2.5s, TTI ≤ 3s). Fail the pipeline if budgets are exceeded to prevent regressions.
- **RUM Monitoring:** Use Vercel Analytics to track real user startup times (PWA boot + first message). Set alerts when the 95th percentile exceeds 3s and investigate root causes.

**Backend Performance:**

- Response Time Target: <2 seconds for chat responses, <500ms for API calls
- Database Optimization: Proper indexing, connection pooling, query optimization
- Caching Strategy: Supabase built-in caching, Claude response caching for common patterns

## Scalability Strategy

- **Primary approach (MVP):** Rely on Vercel Edge Functions for stateless API execution and Supabase's managed Postgres autoscaling (connection pooling + vertical scaling). Load tests must demonstrate support for 10,000 concurrent chat sessions while monitoring Supabase limits (connections, CPU) and tuning if necessary.
- **Monitoring:** Track concurrency, latency, and Supabase resource utilisation via Vercel Analytics and Supabase metrics dashboards; set alerts when utilisation exceeds 70% of quotas.
- **Future enhancement:** If synchronous Claude requests begin to impact latency, introduce a pg-boss queue + dedicated worker (Option 2) to offload analysis/Claude calls while keeping the synchronous API responsive.


## Privacy & Compliance

- **User Consent Management:** Capture explicit consent during onboarding (timestamp + policy version) and store in Supabase `consent_events` table. Redisplay consent on major policy updates and require acceptance before continuing.
- **Data Minimization & Retention:** Restrict access to conversation/crisis logs via Supabase RLS; automatically purge crisis event metadata after 12 months; offer admin endpoints to export or delete user data on request.
- **Crisis Data Handling:** Store crisis events with anonymized user identifiers for analytics; ensure PII is limited to what is required for safety follow-up; log access to crisis data with actor and timestamp.
- **Incident Response & Auditing:** Maintain an incident playbook (who, what, when) and log all admin access via Supabase Audit Logs + Vercel logging. Review access logs monthly.
- **Vendor Compliance:** Leverage Supabase's HIPAA-adjacent posture and Vercel's secure hosting; document DPAs and review vendor SOC2 reports annually.

## Uptime & Incident Response

- **Health Monitoring:** Ping `/api/health` and key chat endpoints every minute via Better Stack/UptimeRobot. Alert on >2 consecutive failures and track monthly uptime to ensure ≥99.5%.
- **Rollback Procedure:** Use Vercel preview deployments; if production degrades, run `vercel rollback <deployment-id>` and redeploy once fixed. Maintain a rollback checklist in the ops runbook.
- **Database Recovery:** Enable Supabase Point-in-Time Recovery (PITR) and schedule weekly backup verification. Document restore steps and rehearse quarterly.
- **Incident Playbook:** Define on-call rotation, communication template, and post-incident review. Record timeline, root cause, corrective actions.
- **Future Expansion:** For higher SLAs (99.9%+), add warm-standby Supabase project + scripted failover as next phase.
