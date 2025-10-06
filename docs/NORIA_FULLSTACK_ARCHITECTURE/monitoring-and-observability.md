# Monitoring and Observability

## Monitoring Stack

- **Frontend Monitoring:** Vercel Analytics (Web Vitals, user interactions, performance)
- **Backend Monitoring:** Vercel Functions metrics (execution time, memory usage, errors)
- **Error Tracking:** Vercel Analytics error reporting + custom error logging
- **Performance Monitoring:** Real User Monitoring (RUM) for chat response times
- **Database Monitoring:** Supabase built-in metrics and query performance
- **AI Usage Tracking:** Claude API usage monitoring with cost tracking

## Key Metrics

**Frontend Metrics:**

- Core Web Vitals (LCP < 2.5s, FID < 100ms, CLS < 0.1)
- Time to First Message (chat interface ready)
- Message Send Success Rate
- PWA Installation Rate
- Crisis Detection Accuracy (false positives/negatives)

**Backend Metrics:**

- API Response Time (95th percentile < 2s for chat)
- Error Rate by Endpoint
- Claude API Success Rate
- Database Query Performance
- Background Job Processing Time
- Crisis Event Response Time

**Business Metrics:**

- Daily Active Users
- Messages per Session
- ChAT Score Improvements
- Graduation Rate
- Crisis Interventions
- User Retention (pre-graduation)

**Cost Monitoring:**

- Claude API Usage & Costs
- Vercel Function Invocations
- Supabase Database & Storage Usage
- Total Cost per User per Month

This comprehensive architecture ensures Noria can deliver its unique graduation-focused coaching model while maintaining the performance, security, and scalability needed for college students' critical social development needs.