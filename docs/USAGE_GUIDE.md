# 🎯 Sensei MCP v0.6.0: Complete Usage Guide

## 🏗️ Architecture Overview

**How it works now (v0.6.0):**

```
You (in Claude Code)
    ↓
    "I'm designing an authentication API. What should I consider?"
    ↓
Claude Code calls → suggest_personas_for_query()
    ↓
Sensei MCP returns → ["security-sentinel", "api-platform-engineer", "pragmatic-architect"]
    ↓
Claude Code calls → get_persona_content("security-sentinel")
    ↓
Sensei MCP returns → Full Security Sentinel SKILL.md (expertise, principles, guidelines)
    ↓
Claude Code calls → get_persona_content("api-platform-engineer")
    ↓
Sensei MCP returns → Full API Platform Engineer SKILL.md
    ↓
Claude Code calls → get_persona_content("pragmatic-architect")
    ↓
Sensei MCP returns → Full Pragmatic Architect SKILL.md
    ↓
Claude Code analyzes your question using all 3 persona perspectives
    ↓
Claude Code synthesizes → Comprehensive multi-perspective answer
    ↓
Claude Code calls → record_consultation()
    ↓
You get → Holistic engineering guidance from 3 expert viewpoints
```

**Key insight:** Sensei MCP provides **content** (persona expertise definitions), Claude performs **analysis** (applies that expertise to your question).

---

## 📚 Real-World Use Cases

### Use Case 1: API Design Review

**Scenario:** You're designing a new REST API for user management in a multi-tenant SaaS application.

**What you do:**
```
You: "I'm designing a REST API for user management in our multi-tenant SaaS.
What should I consider for the endpoints, authentication, and data isolation?"
```

**What Claude Code does automatically:**

1. **Calls `suggest_personas_for_query()`:**
   ```python
   suggest_personas_for_query(
       query="REST API for user management in multi-tenant SaaS...",
       max_suggestions=5
   )
   ```

2. **Gets suggestions:**
   ```json
   {
     "detected_context": "SECURITY",
     "suggestions": [
       {"name": "api-platform-engineer", "relevance": 0.95, "rationale": "Expert in API design, contracts"},
       {"name": "security-sentinel", "relevance": 0.92, "rationale": "Expert in authentication, authorization"},
       {"name": "pragmatic-architect", "relevance": 0.78, "rationale": "Expert in system design, scalability"}
     ]
   }
   ```

3. **Gets each persona's expertise:**
   ```python
   api_content = get_persona_content("api-platform-engineer")
   security_content = get_persona_content("security-sentinel")
   architect_content = get_persona_content("pragmatic-architect")
   ```

4. **Analyzes from each perspective:**
   - **API Platform Engineer perspective:** "Your endpoints should follow RESTful conventions with clear resource hierarchies. For multi-tenant, I recommend `/tenants/{tenantId}/users` structure. Use versioning from day one (`/v1/...`). Document with OpenAPI spec..."

   - **Security Sentinel perspective:** "For multi-tenant SaaS, authentication is CRITICAL. Use JWT with tenant claims embedded. NEVER allow user A to access tenant B's data. Row-level security in your database. Rate limiting per tenant..."

   - **Pragmatic Architect perspective:** "Keep it simple initially. Start with synchronous CRUD. Avoid microservices unless you truly need them. Consider pagination from day one. Think about caching strategy..."

5. **Synthesizes all perspectives:**
   ```
   Claude: "Here's a comprehensive approach combining API design, security, and architectural best practices:

   ## API Structure (API Platform Engineer)
   - Base path: /api/v1/tenants/{tenantId}/users
   - Endpoints:
     - GET /api/v1/tenants/{tenantId}/users (list with pagination)
     - POST /api/v1/tenants/{tenantId}/users (create)
     - GET /api/v1/tenants/{tenantId}/users/{userId} (read)
     - PATCH /api/v1/tenants/{tenantId}/users/{userId} (update)
     - DELETE /api/v1/tenants/{tenantId}/users/{userId} (delete)

   ## Security Measures (Security Sentinel)
   - JWT authentication with tenant_id claim
   - Middleware validates tenant_id in JWT matches {tenantId} in URL
   - Database row-level security policies
   - Rate limiting: 100 req/min per tenant
   - Input validation on all fields

   ## Implementation Approach (Pragmatic Architect)
   - Start with monolithic API service (not microservices)
   - PostgreSQL with multi-tenant schema design
   - Redis for session caching
   - Implement pagination (page/limit) from start
   - OpenAPI documentation auto-generated from code

   ## Code Example:
   [Claude would provide actual implementation code here]

   ## Next Steps:
   1. Set up OpenAPI spec
   2. Implement tenant isolation middleware
   3. Write integration tests for cross-tenant access prevention
   4. Document rate limits and auth flow
   ```

6. **Records the consultation:**
   ```python
   record_consultation(
       query="REST API for user management...",
       personas_used=["api-platform-engineer", "security-sentinel", "pragmatic-architect"],
       synthesis="[Full synthesis above]"
   )
   ```

**Expected outcome:** You get a comprehensive, multi-perspective answer that covers API design patterns, security considerations, and pragmatic implementation approach - all from specialized expert viewpoints.

---

### Use Case 2: Production Crisis Response

**Scenario:** Your production database is experiencing high CPU and slow queries. Users are complaining.

**What you do:**
```
You: "URGENT: Production PostgreSQL CPU at 95%, queries taking 10+ seconds.
Users timing out. What do I do right now?"
```

**What Claude Code does:**

1. **Detects CRISIS context:**
   ```python
   suggest_personas_for_query(
       query="URGENT: Production PostgreSQL CPU at 95%...",
       context_hint="CRISIS"
   )
   ```

2. **Gets crisis specialists:**
   ```json
   {
     "detected_context": "CRISIS",
     "suggestions": [
       {"name": "incident-commander", "relevance": 0.98, "rationale": "Expert in crisis management"},
       {"name": "site-reliability-engineer", "relevance": 0.95, "rationale": "Expert in database operations"},
       {"name": "database-architect", "relevance": 0.90, "rationale": "Expert in query optimization"}
     ]
   }
   ```

3. **Multi-perspective crisis response:**

   **Incident Commander:**
   ```
   "IMMEDIATE ACTIONS (next 5 minutes):
   1. Check: Is this affecting all users or specific tenants?
   2. Communicate: Post status page update + notify team
   3. Triage: Can we fail over to read replica?
   4. Log: Start incident timeline doc

   DO NOT blindly restart the database yet - we need to understand the cause."
   ```

   **Site Reliability Engineer:**
   ```
   "DIAGNOSTICS (run these commands NOW):

   1. Check active connections:
      SELECT count(*), state FROM pg_stat_activity GROUP BY state;

   2. Find slow queries:
      SELECT pid, now() - query_start AS duration, query
      FROM pg_stat_activity
      WHERE state = 'active' AND now() - query_start > interval '5 seconds'
      ORDER BY duration DESC;

   3. Check for locks:
      SELECT * FROM pg_locks WHERE NOT granted;

   4. Connection pool exhaustion?
      SHOW max_connections;

   MITIGATION:
   - If specific query is the culprit: KILL it (SELECT pg_terminate_backend(pid))
   - If connection pool exhausted: Scale up pool or add read replicas
   - Enable slow query log for forensics"
   ```

   **Database Architect:**
   ```
   "ROOT CAUSE ANALYSIS:

   Common causes I see:
   1. Missing index on a frequently queried column
   2. N+1 query problem from application code
   3. Lock contention on hot tables
   4. Runaway analytics query
   5. Connection leak in application

   IMMEDIATE FIX CANDIDATES:
   - If missing index: CREATE INDEX CONCURRENTLY (non-blocking)
   - If bad query: Add to blocklist in PgBouncer
   - If lock: Identify locking transaction and consider killing it

   POST-INCIDENT:
   - Run EXPLAIN ANALYZE on top slow queries
   - Review recent deployments (new code?)
   - Check query patterns vs. index strategy"
   ```

4. **Synthesized action plan:**
   ```
   Claude: "Here's your immediate action plan combining incident response, operations, and database expertise:

   ## PHASE 1: Stabilize (Next 5 minutes)

   1. **Communication** (Incident Commander):
      - Post to status page: "Database performance degradation - investigating"
      - Alert on-call team in Slack

   2. **Diagnostics** (SRE):
      Run these queries on production (safe, read-only):

      ```sql
      -- Find the problem query
      SELECT pid, now() - query_start AS duration, query, state
      FROM pg_stat_activity
      WHERE state = 'active'
        AND now() - query_start > interval '5 seconds'
      ORDER BY duration DESC
      LIMIT 10;
      ```

   3. **Triage Decision**:
      - If you see ONE query dominating → Kill it: `SELECT pg_terminate_backend(<pid>)`
      - If you see MANY slow queries → Likely missing index or connection exhaustion

   ## PHASE 2: Mitigate (Next 15 minutes)

   [Detailed mitigation steps based on findings...]

   ## PHASE 3: Root Cause (Post-incident)

   [Forensics and prevention steps...]
   ```

**Expected outcome:** You get a structured crisis response plan with immediate diagnostics, mitigation steps, and post-incident analysis - combining incident command, operational expertise, and database knowledge.

---

### Use Case 3: Cost Optimization Review

**Scenario:** Your AWS bill jumped from $5k/month to $15k/month and you need to understand why.

**What you do:**
```
You: "Our AWS bill went from $5k to $15k/month. How do I figure out what's causing this and optimize it?"
```

**What Claude Code does:**

1. **Detects COST context:**
   ```json
   {
     "detected_context": "COST",
     "suggestions": [
       {"name": "finops-optimizer", "relevance": 0.98, "rationale": "Expert in cloud cost optimization"},
       {"name": "site-reliability-engineer", "relevance": 0.75, "rationale": "Expert in infrastructure efficiency"},
       {"name": "pragmatic-architect", "relevance": 0.70, "rationale": "Expert in architectural decisions"}
     ]
   }
   ```

2. **Multi-perspective cost analysis:**

   **FinOps Optimizer:**
   ```
   "COST FORENSICS:

   1. Identify the culprit (use AWS Cost Explorer):
      - Group by: Service
      - Look for: Biggest delta month-over-month
      - Common culprits: EC2, RDS, Data Transfer, S3

   2. Quick wins I always check:
      - Zombie resources (unused EBS volumes, old snapshots)
      - Overprovisioned instances (CPU < 20% avg)
      - Unattached Elastic IPs ($3.60/month each)
      - Non-production running 24/7 (should be 8-5)

   3. Data transfer is EXPENSIVE:
      - Cross-region transfers
      - NAT Gateway data processing
      - CloudFront → S3 in different regions

   INVESTIGATION COMMANDS:
   ```
   aws ce get-cost-and-usage \
     --time-period Start=2025-01-01,End=2025-01-31 \
     --granularity MONTHLY \
     --metrics BlendedCost \
     --group-by Type=DIMENSION,Key=SERVICE
   ```
   ```

   **Site Reliability Engineer:**
   ```
   "OPERATIONAL PERSPECTIVE:

   What changed in the last month that correlates with cost spike?

   Checklist:
   - Did traffic increase 3x? Check CloudWatch metrics
   - Did we deploy a new service? Review deployments
   - Are logs exploding? Check CloudWatch Logs storage
   - Is a background job running wild? Check ECS/Lambda invocations

   RED FLAGS I'd investigate:
   1. Lambda invocations: Should be < 1M/day unless high traffic
   2. RDS IOPS: Sudden spike = missing index or bad query
   3. Data transfer: > $1k/month = architectural problem

   MONITORING:
   Set up AWS Budgets with alerts at:
   - 50% of monthly budget
   - 80% of monthly budget
   - 100% of monthly budget"
   ```

   **Pragmatic Architect:**
   ```
   "ARCHITECTURAL COST PATTERNS:

   Common design mistakes that cause cost explosions:

   1. **The Chatty Microservices Problem**:
      - 10 services calling each other = 100x data transfer
      - Solution: Consolidate or use VPC endpoints

   2. **The "We'll cache everything" Problem**:
      - Running massive Redis/ElastiCache cluster
      - Often cheaper to optimize queries

   3. **The Multi-Region Mistake**:
      - Data replication + transfer costs add up FAST
      - Question: Do you really need multi-region?

   4. **The Logging Everything Problem**:
      - CloudWatch Logs at $0.50/GB can spiral
      - Solution: Sample logs, use S3 for archival

   DECISION FRAMEWORK:
   Before adding ANY new AWS service, ask:
   - What's the monthly cost at 10x our current scale?
   - Is there a simpler alternative?
   - Can we batch/aggregate to reduce API calls?"
   ```

3. **Synthesized cost optimization plan:**
   ```
   Claude: "Here's your systematic cost investigation and optimization plan:

   ## PHASE 1: Find the Culprit (Today)

   1. Open AWS Cost Explorer → Group by Service → Compare Jan vs Feb
   2. Run this CLI command for breakdown:
      [Command provided]
   3. Expected: You'll see ONE service with major increase

   ## PHASE 2: Service-Specific Investigation

   ### If it's EC2:
   - Check instance utilization (should be > 50% CPU avg)
   - Look for: Oversized instances, wrong instance families
   - Action: Right-size or use auto-scaling

   ### If it's Data Transfer:
   - Check: Cross-region transfer, NAT Gateway costs
   - Common fix: Use VPC endpoints ($7/month vs $100/month data transfer)

   ### If it's RDS:
   - Check IOPS usage, storage growth, backup retention
   - Action: Optimize queries, reduce IOPS tier if underutilized

   [More service-specific guides...]

   ## PHASE 3: Ongoing Optimization

   1. Set up AWS Budgets with $6k/month alert
   2. Tag all resources by team/project for accountability
   3. Automate non-prod shutdown (8am-6pm weekdays only)
   4. Review monthly with team

   ## Expected Savings

   Quick wins typically save 20-40%:
   - Zombie resources: $500-1000/month
   - Right-sizing: $1000-2000/month
   - Non-prod automation: $500-1500/month
   - Total: $2000-4500/month savings
   ```

**Expected outcome:** You get a systematic cost investigation methodology, service-specific optimization strategies, and architectural guidance to prevent future cost explosions.

---

### Use Case 4: Code Review Before Merge

**Scenario:** You've written a new payment processing module and want comprehensive review before merging to main.

**What you do:**
```
You: "I've implemented a payment processing module using Stripe.
Can you review this for security, reliability, and code quality?

[You paste the code or file paths]"
```

**What Claude Code does:**

1. **Gets relevant session context:**
   ```python
   context = get_session_context(session_id="payment-service")
   # Returns: Your project's constraints, patterns, past decisions
   ```

2. **Suggests review personas:**
   ```json
   {
     "suggestions": [
       {"name": "security-sentinel", "rationale": "Payment security is critical"},
       {"name": "pragmatic-architect", "rationale": "Code quality and patterns"},
       {"name": "site-reliability-engineer", "rationale": "Reliability and error handling"},
       {"name": "qa-automation-engineer", "rationale": "Test coverage"}
     ]
   }
   ```

3. **Multi-perspective code review:**

   **Security Sentinel:**
   ```
   "SECURITY REVIEW:

   ✅ GOOD:
   - Using Stripe SDK (not rolling your own)
   - HTTPS for webhook endpoints
   - Idempotency keys for charge creation

   ❌ CRITICAL ISSUES:

   1. **Line 45: Logging payment details**
      ```python
      logger.info(f"Processing payment: {payment_data}")
      ```
      🚨 NEVER log full payment data (PCI-DSS violation)
      FIX: Log only payment_id and status

   2. **Line 78: Missing webhook signature verification**
      Your webhook handler doesn't verify Stripe signature
      ATTACK VECTOR: Anyone can POST fake webhook data
      FIX: Use `stripe.Webhook.construct_event()` with signing secret

   3. **Line 102: Storing card tokens in database**
      🚨 You're saving `card_token` - this is NOT PCI compliant
      FIX: Only store Stripe customer_id and payment_method_id

   MUST FIX BEFORE MERGE: Issues #2 and #3
   ```

   **Pragmatic Architect:**
   ```
   "CODE QUALITY REVIEW:

   ✅ GOOD PATTERNS:
   - Separation of concerns (handler → service → repository)
   - Using dependency injection
   - Clear function names

   ⚠️ IMPROVEMENTS NEEDED:

   1. **Error handling is too broad**
      ```python
      try:
          charge = stripe.Charge.create(...)
      except Exception as e:  # ← TOO BROAD
          logger.error(e)
      ```

      Better:
      ```python
      from stripe.error import CardError, StripeError

      try:
          charge = stripe.Charge.create(...)
      except CardError as e:
          # User's card declined
          return PaymentResult(success=False, error=e.user_message)
      except StripeError as e:
          # Stripe API error
          logger.error(f"Stripe error: {e}")
          return PaymentResult(success=False, error="Payment processing failed")
      ```

   2. **Missing idempotency at service layer**
      You're using Stripe's idempotency keys, but what if your DB write fails?
      Add application-level idempotency check

   3. **Hardcoded retry logic**
      Consider using a battle-tested library like `tenacity` instead
   ```

   **Site Reliability Engineer:**
   ```
   "RELIABILITY REVIEW:

   ⚠️ CONCERNS:

   1. **No timeout on Stripe API calls**
      Stripe recommends 30-60 second timeouts
      Without this, a Stripe outage will hang your server

   2. **Synchronous payment processing**
      If Stripe is slow, your API response is slow
      RECOMMENDATION:
      - Return 202 Accepted immediately
      - Process payment async via queue (Celery/SQS)
      - Use webhooks to update status

   3. **No circuit breaker**
      If Stripe is down, you'll hammer their API with retries
      Consider: circuit breaker pattern or exponential backoff

   4. **Webhook processing is not idempotent**
      Stripe sends duplicate webhooks occasionally
      You'll double-process payments
      FIX: Check `processed_webhook_ids` table before processing

   METRICS I'd add:
   - payment_success_rate (counter)
   - payment_processing_duration_seconds (histogram)
   - stripe_api_errors_total (counter by error type)
   ```

   **QA Automation Engineer:**
   ```
   "TEST COVERAGE REVIEW:

   MISSING TESTS (CRITICAL):

   1. **Webhook signature verification test**
      Test with: valid signature, invalid signature, replay attack

   2. **Idempotency test**
      Same idempotency key sent twice → only one charge

   3. **Card declined scenario**
      Mock Stripe CardError → verify user-friendly error message

   4. **Partial failure scenario**
      Stripe charge succeeds, DB write fails → verify rollback/retry

   5. **Concurrent requests with same idempotency key**
      Race condition test

   TEST STRUCTURE I recommend:
   ```python
   # tests/unit/test_payment_service.py
   def test_charge_success(mock_stripe):
       # Happy path

   def test_charge_card_declined(mock_stripe):
       # User error

   def test_charge_stripe_api_error(mock_stripe):
       # System error

   def test_idempotency(mock_stripe):
       # Same key twice

   # tests/integration/test_payment_webhook.py
   def test_webhook_signature_valid():
       # Real Stripe signature verification

   def test_webhook_signature_invalid():
       # Should return 400
   ```
   ```

4. **Synthesized review with action items:**
   ```
   Claude: "Here's your comprehensive payment module review from 4 perspectives:

   ## 🚨 BLOCKING ISSUES (Must fix before merge)

   1. **Missing webhook signature verification** (Security Sentinel)
      - Risk: Anyone can forge webhook events
      - Fix: Add `stripe.Webhook.construct_event()` validation
      - Estimated time: 30 minutes

   2. **Logging payment data** (Security Sentinel)
      - Risk: PCI-DSS violation, potential data breach
      - Fix: Remove sensitive data from logs
      - Estimated time: 15 minutes

   3. **Storing card tokens** (Security Sentinel)
      - Risk: PCI compliance violation
      - Fix: Only store Stripe IDs, not tokens
      - Estimated time: 1 hour (requires migration)

   ## ⚠️ HIGH PRIORITY (Fix in next sprint)

   4. **No API timeout** (SRE)
   5. **Missing critical tests** (QA Engineer)
   6. **Broad exception handling** (Pragmatic Architect)

   ## 📋 RECOMMENDATIONS (Nice to have)

   7. Async payment processing for better UX
   8. Circuit breaker for Stripe API
   9. Better metrics/observability

   ## CODE CHANGES NEEDED

   ### Fix #1: Webhook Signature Verification
   ```python
   # Before
   @app.post("/webhooks/stripe")
   def handle_webhook(request):
       event = request.json()  # ← UNSAFE
       process_event(event)

   # After
   @app.post("/webhooks/stripe")
   def handle_webhook(request):
       payload = request.body
       sig_header = request.headers.get("Stripe-Signature")

       try:
           event = stripe.Webhook.construct_event(
               payload, sig_header, webhook_secret
           )
       except ValueError:
           return {"error": "Invalid payload"}, 400
       except stripe.error.SignatureVerificationError:
           return {"error": "Invalid signature"}, 400

       process_event(event)
   ```

   [More fix examples...]

   ## DECISION POINT

   Block merge until fixes #1-3 complete? (My recommendation: YES)
   ```

5. **Records the consultation:**
   ```python
   record_consultation(
       query="Code review for payment processing module",
       personas_used=["security-sentinel", "pragmatic-architect",
                      "site-reliability-engineer", "qa-automation-engineer"],
       synthesis="[Full review above]"
   )
   ```

**Expected outcome:** You get a comprehensive code review from 4 expert perspectives (security, architecture, reliability, testing) with prioritized action items, specific code fixes, and a clear decision on whether to merge.

---

### Use Case 5: Session-Aware Architecture Decision

**Scenario:** You previously decided to use PostgreSQL, and now you're wondering if you should switch to MongoDB for a new feature.

**What you do:**
```
You: "We're building a new document storage feature. Should we use MongoDB for this?
It feels like a better fit for document storage."
```

**What Claude Code does:**

1. **Gets session context first:**
   ```python
   context = get_session_context(session_id="saas-backend")
   ```

   Returns:
   ```json
   {
     "active_constraints": ["AWS only", "Python 3.11+", "PostgreSQL"],
     "patterns_agreed": ["Monolithic architecture", "Single database"],
     "recent_decisions": [
       {
         "id": "dec-042",
         "category": "database",
         "description": "Use PostgreSQL for primary data store",
         "rationale": "Team expertise, ACID guarantees, proven at scale",
         "timestamp": "2025-01-15"
       }
     ]
   }
   ```

2. **Suggests personas with session context:**
   ```python
   suggestions = suggest_personas_for_query(
       query="Should we use MongoDB for document storage feature?"
   )
   ```

3. **Multi-perspective analysis with session awareness:**

   **Database Architect:**
   ```
   "DATABASE DECISION REVIEW:

   🔍 CONTEXT FROM SESSION:
   I see you decided on PostgreSQL 8 days ago (decision #dec-042)
   with rationale: team expertise, ACID guarantees.

   NEW QUESTION: Should we add MongoDB for document storage?

   MY PERSPECTIVE:

   ❌ I recommend AGAINST MongoDB for these reasons:

   1. **PostgreSQL HAS document storage** (since v9.4):
      - JSONB column type (binary JSON, indexed, fast)
      - GIN indexes on JSONB fields
      - Full-text search on JSON
      - All the features you need WITHOUT adding a new database

   2. **Operational complexity**:
      - Now your team needs to manage 2 databases
      - Two backup strategies
      - Two monitoring setups
      - Two security policies

   3. **Data consistency**:
      - How do you handle transactions across Postgres + MongoDB?
      - Distributed transactions are HARD

   ALTERNATIVE SOLUTION:
   ```sql
   -- Use PostgreSQL JSONB instead
   CREATE TABLE documents (
       id UUID PRIMARY KEY,
       tenant_id UUID NOT NULL,
       content JSONB NOT NULL,
       created_at TIMESTAMP DEFAULT NOW()
   );

   -- Index for fast queries
   CREATE INDEX idx_documents_content_gin ON documents USING GIN (content);

   -- Query example
   SELECT * FROM documents
   WHERE content @> '{"status": "published"}';
   ```

   WHEN MongoDB makes sense:
   - If you're already using it
   - If you need massive horizontal scaling (100+ TB)
   - If you truly have schema-less data

   Your case? Stick with PostgreSQL JSONB."
   ```

   **Pragmatic Architect:**
   ```
   "CONSISTENCY CHECK:

   📅 January 15: You decided on PostgreSQL
   📅 January 23: You're considering MongoDB (8 days later!)

   🚨 RED FLAG: This is classic "grass is greener" syndrome

   DECISION FRAMEWORK:

   Before adding ANY new technology to your stack, answer:

   1. **Can we solve this with existing tech?**
      → YES: PostgreSQL JSONB handles documents perfectly

   2. **Is this a core requirement or nice-to-have?**
      → If nice-to-have: definitely use existing tech

   3. **What's the long-term cost?**
      → MongoDB Atlas: $200-500/month minimum
      → Postgres JSONB: $0 additional (already paying for Postgres)

   4. **Team expertise?**
      → You chose Postgres for "team expertise"
      → Does your team know MongoDB? If not, training time + learning curve

   MY RECOMMENDATION:
   Stick with PostgreSQL JSONB for 6 months.

   If you hit genuine limitations (you won't), THEN revisit MongoDB.

   Remember: The best technology is the one you already have."
   ```

   **FinOps Optimizer:**
   ```
   "COST ANALYSIS:

   CURRENT STATE:
   - PostgreSQL RDS: Estimated $150-400/month (existing)

   IF YOU ADD MONGODB:
   - MongoDB Atlas M10 (minimum prod tier): $195/month
   - Total: $345-595/month
   - **Increase: $195/month = $2,340/year**

   ALTERNATIVE (PostgreSQL JSONB):
   - Storage: +10 GB = $1-2/month additional
   - IOPS: Negligible increase
   - **Increase: ~$24/year**

   COST RATIO: MongoDB is 97.5x more expensive than Postgres JSONB

   QUESTION: Will MongoDB give you 97x more value?

   OTHER COSTS YOU'LL PAY:
   - Developer time learning MongoDB: 40-80 hours = $4,000-8,000
   - Ongoing maintenance: 2-4 hours/month = $2,400-4,800/year
   - Monitoring tools: $50-100/month = $600-1,200/year

   TOTAL YEAR 1 COST OF MONGODB: $9,340 - $16,340

   Is this feature worth $10k-16k in Year 1?"
   ```

4. **Synthesized decision with session consistency:**
   ```
   Claude: "Based on your session history and multi-perspective analysis:

   ## ❌ RECOMMENDATION: Do NOT add MongoDB

   ### Why (Session-Aware):

   1. **Conflicts with January 15 decision** (8 days ago):
      - You chose PostgreSQL for team expertise and proven scalability
      - Adding MongoDB contradicts "single database" pattern

   2. **PostgreSQL already solves this**:
      - JSONB column type = native document storage
      - Full indexing, querying, transactions
      - No new infrastructure needed

   3. **Cost analysis**:
      - MongoDB: +$9,340-16,340 in Year 1
      - PostgreSQL JSONB: +$24 in Year 1
      - 97.5x cost difference

   4. **Operational complexity**:
      - 2 databases = 2x backup, monitoring, security
      - Cross-database consistency is HARD

   ## ✅ ALTERNATIVE: PostgreSQL JSONB

   Implementation:
   ```sql
   -- Your existing Postgres
   CREATE TABLE documents (
       id UUID PRIMARY KEY,
       tenant_id UUID NOT NULL,
       metadata JSONB,
       content JSONB,
       created_at TIMESTAMP DEFAULT NOW()
   );

   CREATE INDEX idx_doc_content ON documents USING GIN (content);
   ```

   Python code:
   ```python
   # Insert document
   doc = {
       "title": "My Document",
       "tags": ["important", "draft"],
       "nested": {"field": "value"}
   }
   cursor.execute(
       "INSERT INTO documents (tenant_id, content) VALUES (%s, %s)",
       (tenant_id, json.dumps(doc))
   )

   # Query documents
   cursor.execute(
       "SELECT * FROM documents WHERE content @> %s",
       (json.dumps({"tags": ["important"]}),)
   )
   ```

   ## Decision:

   Stick with PostgreSQL. Implement with JSONB.

   Revisit in 6 months ONLY if you hit concrete limitations
   (you won't - PostgreSQL JSONB handles TB-scale document data).

   This keeps you consistent with your architecture decisions and saves $10k+/year.
   ```

5. **Records consultation for future consistency checks:**
   ```python
   record_consultation(
       query="Should we use MongoDB for document storage?",
       personas_used=["database-architect", "pragmatic-architect", "finops-optimizer"],
       synthesis="Recommended against MongoDB, use PostgreSQL JSONB instead..."
   )

   # You could also record a decision:
   record_decision(
       category="database",
       description="Use PostgreSQL JSONB for document storage (not MongoDB)",
       rationale="Consistent with existing Postgres decision, 97x cheaper, team expertise, avoids operational complexity"
   )
   ```

**Expected outcome:** You get session-aware guidance that catches architectural drift, reminds you of past decisions, provides cost analysis, and gives you a consistent technical direction that aligns with your team's previous choices.

---

## 🎯 Key Benefits Across All Use Cases

### 1. **Multi-Perspective Analysis**
- Every question gets analyzed from 2-5 specialized expert viewpoints
- No single bias (security AND cost AND pragmatism)
- Tensions between perspectives are made explicit

### 2. **Session-Aware Consistency**
- Sensei remembers your past decisions
- Flags when new requests conflict with previous choices
- Prevents architectural drift and "rewrite everything" syndrome

### 3. **Context-Appropriate Responses**
- Crisis situations get crisis specialists (Incident Commander, SRE)
- Security questions get Security Sentinel
- Cost questions get FinOps Optimizer
- Automatic context detection from your query

### 4. **Actionable, Specific Guidance**
- Not generic advice: actual code examples
- Prioritized action items (blocking vs. nice-to-have)
- Estimated time and cost for implementations

### 5. **Knowledge Accumulation**
- Every consultation gets recorded
- Build up institutional knowledge over time
- Export as ADRs for team onboarding

---

## 🚫 What Sensei Does NOT Do

1. **Write full applications**: Sensei provides guidance and code examples, not entire codebases
2. **Make decisions for you**: It presents perspectives; YOU decide
3. **Execute changes**: It guides; you implement
4. **Replace human judgment**: It's a mentor, not a dictator

---

## 🔄 Typical Workflow Pattern

```
Developer question
    ↓
Claude calls suggest_personas_for_query()
    ↓
Claude gets 2-5 persona contents
    ↓
Claude analyzes from each perspective
    ↓
Claude synthesizes all viewpoints
    ↓
Developer gets comprehensive answer
    ↓
Claude records consultation
    ↓
Session memory updated for future consistency
```

---

## 💡 Getting Started

**Step 1: Install Sensei MCP** (if not already done)
```bash
claude mcp add sensei -- uvx sensei-mcp
```

**Step 2: Just ask questions naturally in Claude Code**
```
You: "I'm designing a new API for payments. What should I consider?"
```

**Step 3: Claude automatically:**
- Suggests relevant personas
- Gets their expertise content
- Analyzes from each perspective
- Synthesizes all viewpoints
- Records the consultation

**That's it!** No complex setup, no manual persona selection. Just ask and get multi-perspective engineering guidance.

---

## 📊 23 Available Personas

- **Core (3):** Snarky Senior Engineer, Pragmatic Architect, Legacy Archaeologist
- **Specialized (9):** API Platform Engineer, Data Engineer, Frontend/UX Specialist, ML Pragmatist, Mobile Platform Engineer, Security Sentinel, FinOps Optimizer, Database Architect, Compliance Guardian
- **Operations (4):** Site Reliability Engineer, Incident Commander, Observability Engineer, DevEx Champion
- **Platform (3):** Platform Builder, QA Automation Engineer, Technical Writer
- **Leadership (3):** Empathetic Team Lead, Product Engineering Lead, Executive Liaison
- **Meta (1):** Skill Orchestrator

Each persona has deep expertise in their domain with specific principles, patterns, and best practices.

---

## 🤝 Questions?

The key insight: **You just ask questions naturally.** Claude Code handles all the orchestration automatically.

Sensei MCP v0.6.0 makes multi-perspective engineering guidance invisible and effortless.
