# Playwright MCP Integration Guide

**Version:** 0.8.0
**MCP Server:** [@playwright/mcp-server](https://github.com/microsoft/playwright-mcp) or [@modelcontextprotocol/server-playwright](https://github.com/modelcontextprotocol/servers/tree/main/src/playwright)
**Alternative:** Chrome DevTools MCP
**Purpose:** Live system inspection, performance analysis, debugging

---

## 🎯 What is Playwright MCP?

Playwright MCP lets Sensei personas **interact with live web applications**:
- **Performance Engineer:** Measure Core Web Vitals (LCP, CLS, FID)
- **Frontend UX Specialist:** Inspect UI, test user flows, check accessibility
- **Security Sentinel:** Analyze network traffic, inspect cookies, check CSP headers
- **Site Reliability Engineer:** Verify health checks, test failover, measure uptime

### Why This Matters

**Before Playwright:**
```
You: "Why is our checkout page slow?"
Sensei: "Common causes are: large bundles, blocking scripts, API latency..."
// Generic advice, no real data
```

**After Playwright:**
```
You: "Why is our checkout page slow?"
Sensei:
1. Navigates to checkout page
2. Captures network waterfall
3. Measures LCP: 4.2s (POOR)
4. Identifies: 2.1s blocked by analytics script
5. Recommends: Defer analytics, reduce to 1.8s LCP (GOOD)
// Real diagnostics, actionable fixes
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Playwright MCP

Playwright MCP comes in two flavors:

**Option A: Official Playwright MCP** (Recommended)
```bash
npx -y @playwright/mcp-server
```

**Option B: MCP Servers Collection**
```bash
npx -y @modelcontextprotocol/server-playwright
```

**Option C: Chrome DevTools MCP** (Alternative with more debugging features)
```bash
npx -y @modelcontextprotocol/server-chrome-devtools
```

> **Note:** This guide covers Playwright MCP. For Chrome DevTools, see [Chrome DevTools Integration Guide](./CHROME_DEVTOOLS.md).

### 2. Install Browser Dependencies

Playwright needs browser binaries:

```bash
# Install Chromium (required)
npx playwright install chromium

# Optional: Install all browsers
npx playwright install
```

### 3. Configure MCP Client

**Claude Code:**
```bash
claude mcp add playwright -- npx -y @playwright/mcp-server
```

**Claude Desktop (macOS):**
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    }
  }
}
```

**Claude Desktop (Windows):**
```json
// %APPDATA%\Claude\claude_desktop_config.json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    }
  }
}
```

### 4. Test Integration

Restart your MCP client and try:

```
You: "Navigate to https://example.com and take a screenshot"

Expected workflow:
1. Playwright opens browser
2. Navigates to example.com
3. Takes screenshot
4. Returns image for analysis
```

---

## 📚 How to Use Playwright with Sensei

### Pattern: Live Inspection + Expert Analysis

**User Query:** "Why is our login page slow?"

**Sensei + Playwright Flow:**
1. **Sensei suggests:** `[performance-engineer, frontend-ux-specialist]`
2. **Playwright actions:**
   ```javascript
   browser_navigate("https://app.example.com/login")
   browser_snapshot()  // Capture accessibility tree
   browser_network_requests()  // Get all network calls
   performance_start_trace({ reload: true })  // Measure Core Web Vitals
   ```
3. **Synthesis:**
   - Performance Engineer: Bottleneck analysis (network waterfall, JS execution)
   - Frontend UX Specialist: UX impact (perceived performance)
   - **Playwright data:** Real metrics (LCP: 3.8s, CLS: 0.15, 12 blocking scripts)

**Output:**
```markdown
## Login Page Performance Analysis

### Core Web Vitals (Playwright - Live Measurement)
- **LCP (Largest Contentful Paint):** 3.8s 🔴 POOR (target: <2.5s)
- **CLS (Cumulative Layout Shift):** 0.15 🟡 NEEDS IMPROVEMENT (target: <0.1)
- **FID (First Input Delay):** 180ms 🟡 NEEDS IMPROVEMENT (target: <100ms)

### Bottleneck Analysis (Performance Engineer)

**1. Blocking Scripts (2.1s wasted)**
From network waterfall:
```
analytics.js      1.2s (blocking, 450KB)
chat-widget.js    0.9s (blocking, 380KB)
```

**Fix:**
```html
<!-- Defer non-critical scripts -->
<script src="analytics.js" defer></script>
<script src="chat-widget.js" async></script>
```

**Expected improvement:** LCP 3.8s → 2.6s (30% faster) ✅

**2. Layout Shift (CLS: 0.15)**
From accessibility snapshot:
- Login form shifts down 45px when error message appears
- "Forgot password" link shifts when loaded

**Fix:**
```css
/* Reserve space for error message */
.error-message {
  min-height: 24px;  /* Prevent shift */
}

/* Reserve space for forgot password link */
.login-form {
  min-height: 320px;
}
```

**Expected improvement:** CLS 0.15 → 0.05 (GOOD) ✅

### Implementation Priority
1. **Week 1:** Defer analytics.js + chat-widget.js (2 hours)
2. **Week 1:** Fix layout shifts with min-height (1 hour)
3. **Week 2:** Re-test with Playwright, validate improvements
```

---

## 🔥 Example Workflows

### Workflow 1: Performance Debugging

**Scenario:** Checkout page feels slow

```
You: "Diagnose performance issues on /checkout"

Sensei + Playwright workflow:
1. Sensei suggests: [performance-engineer, frontend-ux-specialist]
2. Playwright traces:
   - Navigate to /checkout
   - Start performance trace with page reload
   - Capture Core Web Vitals
   - Get network waterfall
3. Claude synthesizes: Real metrics + performance recommendations
```

**Sample Output:**
```markdown
## Checkout Performance Report

### Metrics (Playwright Trace)
| Metric | Value | Grade | Target |
|--------|-------|-------|--------|
| LCP | 4.2s | 🔴 POOR | <2.5s |
| FID | 45ms | 🟢 GOOD | <100ms |
| CLS | 0.02 | 🟢 GOOD | <0.1 |
| TTFB | 1.8s | 🔴 POOR | <800ms |

### Root Causes

**1. Slow API Response (1.8s TTFB)**
```
GET /api/cart?user_id=123
Response time: 1,823ms
```
**Diagnosis (Performance Engineer):**
- Backend DB query not indexed
- N+1 query for cart items

**Fix:**
```sql
-- Add index on cart_items.user_id
CREATE INDEX idx_cart_user ON cart_items(user_id);

-- Use JOIN instead of N+1
SELECT * FROM carts
JOIN cart_items ON carts.id = cart_items.cart_id
WHERE carts.user_id = ?;
```

**Expected:** TTFB 1.8s → 400ms ✅

**2. Large JavaScript Bundle (LCP 4.2s)**
From network waterfall:
```
checkout.bundle.js: 2.8MB (uncompressed)
Load time: 2.4s
```

**Fix:**
- Enable Brotli compression: 2.8MB → 420KB
- Code splitting: Split vendor bundle
- Lazy load payment providers

**Expected:** LCP 4.2s → 2.1s ✅
```

---

### Workflow 2: UI/UX Inspection

**Scenario:** Verify UI matches design specs

```
You: "Take a screenshot of /checkout and compare to Figma design"

Sensei + Playwright workflow:
1. Sensei suggests: [frontend-ux-specialist, visual-design-specialist]
2. Playwright captures:
   - Navigate to /checkout
   - Take full-page screenshot
   - Capture accessibility snapshot (text hierarchy)
3. Claude analyzes: Visual comparison + UX recommendations
```

**Sample Output:**
```markdown
## Checkout UI Review

### Screenshot Analysis (Frontend UX Specialist)

**❌ Discrepancies from Design:**

1. **Button Color** (Screenshot shows #3366FF, Figma shows #0052CC)
   ```css
   /* Current */
   .checkout-button { background: #3366FF; }

   /* Should be */
   .checkout-button { background: #0052CC; }
   ```

2. **Font Size** (Screenshot shows 14px, Figma shows 16px)
   - Body text too small for accessibility
   - WCAG AA requires 16px minimum for body text

3. **Spacing** (16px gap, should be 24px)
   - Cards too cramped
   - Reduces scanability

### Accessibility Issues (from snapshot)

**⚠️ Medium Priority:**
- "Place Order" button: No aria-label when loading
- Credit card input: Missing autocomplete="cc-number"
- Error messages: Not announced to screen readers

**Fixes:**
```html
<!-- Add loading state accessibility -->
<button
  aria-label="Place Order"
  aria-busy="true"
  disabled
>
  Processing...
</button>

<!-- Add credit card autocomplete -->
<input
  type="text"
  autocomplete="cc-number"
  aria-label="Credit card number"
/>
```
```

---

### Workflow 3: Security Analysis

**Scenario:** Audit network traffic for security issues

```
You: "Check /login for security issues"

Sensei + Playwright workflow:
1. Sensei suggests: [security-sentinel, privacy-engineer]
2. Playwright inspects:
   - Navigate to /login
   - Capture network requests (headers, cookies)
   - Take snapshot of form fields
3. Claude analyzes: Security posture + compliance
```

**Sample Output:**
```markdown
## Login Security Audit

### Network Traffic Analysis (Playwright)

**🔴 Critical Issues:**

1. **No HTTPS** (Security Sentinel)
   ```
   URL: http://app.example.com/login  ← Insecure!
   Status: 200 OK
   ```
   **Risk:** Credentials transmitted in plaintext
   **Fix:** Enforce HTTPS redirect

2. **Missing Security Headers**
   From network response:
   ```
   ✅ X-Frame-Options: DENY
   ❌ Content-Security-Policy: (missing)
   ❌ Strict-Transport-Security: (missing)
   ✅ X-Content-Type-Options: nosniff
   ```

   **Add missing headers:**
   ```nginx
   # Nginx config
   add_header Content-Security-Policy "default-src 'self'; script-src 'self'";
   add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
   ```

3. **Session Cookie Not Secure** (Privacy Engineer)
   ```
   Set-Cookie: session_id=abc123; Path=/; HttpOnly
   Missing: Secure, SameSite=Strict
   ```

   **Fix:**
   ```
   Set-Cookie: session_id=abc123; Path=/; HttpOnly; Secure; SameSite=Strict
   ```

### Form Analysis (from snapshot)

**⚠️ Medium Priority:**
- Password field allows paste (good for password managers) ✅
- No rate limiting visible (test with 10 rapid login attempts)
- "Remember me" checkbox defaults to unchecked ✅ (GDPR compliant)
```

---

### Workflow 4: Accessibility Audit

**Scenario:** WCAG compliance check

```
You: "Run accessibility audit on /checkout"

Sensei + Playwright workflow:
1. Sensei suggests: [accessibility-specialist, frontend-ux-specialist]
2. Playwright tests:
   - Navigate to /checkout
   - Take accessibility snapshot
   - Test keyboard navigation (Tab, Enter, Escape)
3. Claude analyzes: WCAG violations + fixes
```

**Sample Output:**
```markdown
## WCAG Accessibility Audit

### Automated Checks (Playwright Snapshot)

**🔴 WCAG AA Violations (Must Fix):**

1. **Missing Form Labels**
   ```html
   <!-- Current (BAD) -->
   <input type="text" placeholder="Card number" />

   <!-- Fixed (GOOD) -->
   <label for="card-number">Card number</label>
   <input
     id="card-number"
     type="text"
     placeholder="1234 5678 9012 3456"
     aria-required="true"
   />
   ```

2. **Insufficient Color Contrast**
   - Error text: #FF6B6B on #FFFFFF = 3.1:1 (fails WCAG AA 4.5:1)
   - Fix: Use #CC0000 (5.2:1 contrast) ✅

3. **No Skip Link**
   - Screen reader users must tab through entire nav
   - Add skip link to main content:
   ```html
   <a href="#main-content" class="skip-link">
     Skip to checkout
   </a>
   ```

### Keyboard Navigation Test

**✅ Passed:**
- Tab order is logical (form → button → links)
- Escape closes modal dialogs

**❌ Failed:**
- Date picker not keyboard accessible (requires mouse)
- "Place Order" button not focusable when loading

**Fixes:**
```javascript
// Make date picker keyboard accessible
<input
  type="date"  // Native date picker (fully accessible)
  aria-label="Delivery date"
/>

// Ensure button stays focusable when disabled
<button
  aria-busy="true"
  aria-disabled="true"  // Don't use disabled attribute
  tabindex="0"
>
  Processing...
</button>
```

### Screen Reader Test (Manual Required)
- [ ] Test with NVDA (Windows)
- [ ] Test with JAWS (Windows)
- [ ] Test with VoiceOver (macOS/iOS)
```

---

## 🔍 Playwright MCP Tools Reference

### Core Navigation

**`browser_navigate(url)`**
```javascript
browser_navigate({ url: "https://example.com" })
```

**`browser_navigate_back()`**
```javascript
browser_navigate_back()
```

### Content Inspection

**`browser_snapshot()`**
Captures accessibility tree (text-based, fast):
```javascript
browser_snapshot()
// Returns: Hierarchical text representation of page
```

**`browser_take_screenshot()`**
Captures visual screenshot:
```javascript
browser_take_screenshot({
  filename: "checkout-page.png",
  fullPage: true  // Full page scroll
})
```

### Performance Analysis

**`browser_performance_start_trace()`**
```javascript
performance_start_trace({
  reload: true,  // Reload page to get full trace
  autoStop: true  // Stop after page load
})
```

**`browser_performance_stop_trace()`**
```javascript
performance_stop_trace()
// Returns: Core Web Vitals, insights, recommendations
```

**`browser_performance_analyze_insight()`**
```javascript
performance_analyze_insight({
  insightSetId: "trace_1",
  insightName: "LCPBreakdown"  // Get detailed LCP analysis
})
```

### Network Analysis

**`browser_network_requests()`**
```javascript
browser_network_requests()
// Returns: All network requests since page load
// (URL, method, status, size, timing)
```

**`browser_get_network_request(reqid)`**
```javascript
get_network_request({ reqid: 5 })
// Returns: Full details (headers, body, cookies)
```

### Interaction

**`browser_click(element)`**
```javascript
browser_click({
  element: "Submit button",
  ref: "button[type=submit]"
})
```

**`browser_type(element, text)`**
```javascript
browser_type({
  element: "Email input",
  ref: "input[name=email]",
  text: "user@example.com"
})
```

**`browser_fill_form(fields)`**
```javascript
browser_fill_form({
  fields: [
    { name: "email", value: "user@example.com", ref: "input[name=email]" },
    { name: "password", value: "secret", ref: "input[name=password]" }
  ]
})
```

### Console & Logs

**`browser_console_messages()`**
```javascript
browser_console_messages({ onlyErrors: true })
// Returns: Console errors and warnings
```

---

## 💡 Best Practices

### 1. Start with Snapshot, Not Screenshot

**❌ Inefficient:**
```
1. Take screenshot (slow, large file)
2. Analyze visually
```

**✅ Efficient:**
```
1. Take snapshot (fast, text-based)
2. Analyze structure, accessibility
3. Take screenshot only if visual issues found
```

### 2. Use Performance Traces Strategically

Traces are expensive (3-5 seconds):

**When to trace:**
- ✅ Performance complaints (slow page load)
- ✅ Verifying optimizations worked
- ✅ Baseline measurements

**When NOT to trace:**
- ❌ Simple UI inspections
- ❌ Every consultation (cache results)

### 3. Combine with Context7 for Best Practices

**Pattern:**
1. Playwright: Measure current performance (LCP: 4.2s)
2. Context7: Fetch latest performance best practices
3. Sensei: Synthesize (Performance Engineer recommends fixes)

### 4. Test in Multiple Environments

```javascript
// Test in different viewport sizes
browser_resize({ width: 375, height: 812 })  // iPhone X
browser_snapshot()

browser_resize({ width: 1920, height: 1080 })  // Desktop
browser_snapshot()
```

### 5. Respect Privacy in Screenshots

**⚠️ Screenshots may contain:**
- User PII (names, emails, addresses)
- Session tokens in URLs
- Sensitive business data

**Before sharing:**
```javascript
// Navigate to demo account or sanitized environment
browser_navigate("https://staging.example.com?demo=true")
```

---

## 🐛 Troubleshooting

### Issue: "Playwright not installed"

**Cause:** Browser binaries missing

**Solution:**
```bash
npx playwright install chromium
```

---

### Issue: "Navigation timeout"

**Cause:** Page took >30s to load

**Solution:**
```javascript
// Increase timeout for slow pages
browser_navigate({
  url: "https://slow-site.com",
  timeout: 60000  // 60 seconds
})
```

---

### Issue: "Element not found"

**Cause:** Selector doesn't match any element

**Solution:**
1. Take snapshot first to see available elements:
   ```javascript
   browser_snapshot()
   // Returns: All interactive elements with refs
   ```

2. Use exact `ref` from snapshot:
   ```javascript
   browser_click({
     element: "Submit button",
     ref: "button[data-testid='submit']"  // From snapshot
   })
   ```

---

### Issue: "Screenshot is blank"

**Cause:** Page hasn't loaded yet

**Solution:**
```javascript
// Wait for specific element before screenshot
browser_wait_for({ text: "Checkout" })
browser_take_screenshot()
```

---

### Issue: "Performance trace failed"

**Cause:** Page crashed or trace interrupted

**Solution:**
```javascript
// Stop any running trace first
performance_stop_trace()

// Start fresh trace
performance_start_trace({ reload: true })
```

---

## 🎯 Success Metrics

Track Playwright effectiveness:

```python
get_session_insights(session_id="my-project")

# Good indicators:
{
  "mcp_usage": {
    "playwright": {
      "total_sessions": 34,
      "avg_load_time": "3.2s",
      "insights_generated": 127
    }
  },
  "performance_improvements": {
    "lcp_avg_before": "4.8s",
    "lcp_avg_after": "2.1s",  # 56% improvement ✅
    "cls_avg_before": "0.18",
    "cls_avg_after": "0.05"  # 72% improvement ✅
  }
}
```

---

## 📖 Related Resources

- [Playwright Docs](https://playwright.dev/)
- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Chrome DevTools MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/chrome-devtools)
- [Sensei MCP Integration Architecture](../MCP_INTEGRATION_ARCHITECTURE.md)
- [Context7 Integration Guide](./CONTEXT7.md)
- [Tavily Integration Guide](./TAVILY.md)

---

## 🤝 Contributing

Found a great Playwright + Sensei workflow? Share it!

1. Open issue: https://github.com/amarodeabreu/sensei-mcp/issues
2. Add your workflow to this doc via PR
3. Tag with `integration-example`

---

**Made with 🥋 by the Sensei MCP community**

*See the real system. Fix the real problems.*
