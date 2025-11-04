# Ad Optimization Agent - Design Document

## Agent Role & Objectives

**Role:** Expert digital marketing strategist that analyzes multi-channel advertising performance and allocates daily budgets to maximize conversions.

**Core Objective:** Maximize total conversions within a fixed daily budget ($1000) by intelligently distributing spend across three channels: Search, Social, and Display.

**Secondary Goals:** (1) Maintain multi-channel brand presence, (2) Minimize cost per acquisition (CPA), (3) Adapt to performance trends, (4) Provide transparent, explainable decisions.

---

## Inputs & Outputs

**Inputs:**
- Historical performance CSV: `date`, `channel`, `spend`, `impressions`, `clicks`, `conversions` (14-30 days)
- Daily budget: $1000 fixed allocation
- Lookback window: 7 days for trend analysis
- Previous allocation: For enforcing shift limits

**Outputs:**
- Budget allocation per channel (e.g., Search: $550, Social: $300, Display: $150)
- Reasoning: Data-driven rationale explaining decision and trade-offs
- Expected conversions: Projected outcomes per channel
- Decision metadata: Timestamp, tokens used, constraint violations

---

## Rules & Guardrails

### Budget Constraints

1. **Minimum Allocation: 15% per channel**
   - Ensures multi-channel brand presence
   - Prevents over-concentration in single platform
   - Diversifies risk against platform-specific issues

2. **Maximum Allocation: 60% per channel**
   - Allows strong preference but prevents total dominance
   - Maintains strategic flexibility
   - Guards against performance shifts

3. **Daily Shift Limit: ±25%**
   - Prevents volatile, erratic changes day-to-day
   - Enables gradual adaptation to trends
   - Maintains predictability for marketing teams

**Exception:** First optimization run has no shift limit (no previous allocation exists).

### Privacy & Trust

- **No PII:** Only aggregate channel-level metrics, no user data
- **Human-in-the-Loop:** Agent proposes, humans approve and execute
- **Transparency:** All decisions logged with complete reasoning
- **Audit Trail:** Immutable decision logs with timestamps and data snapshots

---

## Evaluation Metrics

**Primary Metric:** Total conversions (days 15-30)
- Agent must beat baseline by ≥10% to demonstrate value

**Secondary Metrics:**
- Average CPA: Should be ≤ baseline (more cost-efficient)
- Allocation stability: Std dev <12% per channel (not thrashing)
- Reasoning quality: Manual review of decision rationale

**Baseline Strategy:** Equal allocation (33.3% per channel, no optimization)

**Comparison Method:**
- Train performance model on days 1-14 (calculate CVR, CTR, CPA per channel)
- Test period days 15-30: Agent proposes allocations, simulate outcomes using model
- Compare cumulative conversions and CPA vs. baseline using same simulation model

---

## System Prompt Structure

The LLM receives:
1. **Performance data:** Recent 7-day metrics (CPA, CVR, CTR, trends) per channel
2. **Constraints:** Budget limits, min/max bounds, shift limits, previous allocation
3. **Task:** Propose optimal allocation as JSON with reasoning
4. **Examples:** 2-3 few-shot demonstrations of good allocations

The LLM returns:
```json
{
  "allocations": {"Search": 550, "Social": 300, "Display": 150},
  "reasoning": "Search has lowest CPA ($8.50) and stable performance, allocated 55%. Social shows improving trend (+0.8% CVR) despite higher CPA, warranting 30% to capitalize on momentum. Display has highest CPA ($35) and declining trend, minimized to 15% floor.",
  "expected_conversions": {"Search": 60, "Social": 26, "Display": 5},
  "confidence": "High"
}
```

---

## Performance Modeling

**Challenge:** How to evaluate counterfactual allocations (what if we allocated differently)?

**Solution:** Build performance model from training data (days 1-14):
- Calculate base conversion rate, CTR, CPM per channel
- Identify trends (improving/declining/stable)
- Measure volatility (daily variance)

**Simulation:** For any proposed allocation:
1. Estimate impressions: `budget / CPM × 1000`
2. Estimate clicks: `impressions × CTR`
3. Estimate conversions: `clicks × (CVR + trend × day_number)`
4. Add realistic noise based on historical volatility

**Key Assumptions:**
- Channel performance remains relatively stable over 30 days
- No cross-channel effects (independence)
- Linear scaling (no diminishing returns)
- No external factors (seasonality, competitors)

**Limitations:** Real ad platforms have auction dynamics, attribution complexity, and external factors not modeled here. This is a prototype suitable for demonstrating the approach; production requires real A/B testing.

---

## Ethics & Trust Considerations

**Transparency:** Every allocation includes reasoning; decisions are auditable and explainable to stakeholders.

**Fairness:** No inherent platform bias; purely data-driven. Equal minimum (15%) ensures all channels get opportunity to perform.

**Accountability:** Agent recommends, humans decide. Marketing teams retain final authority and can override for strategic reasons.

**Privacy:** Zero PII collection. Only aggregate channel metrics (no user IDs, cookies, or personal identifiers). GDPR/CCPA compliant.

**Safety:** Guardrails prevent catastrophic errors (e.g., allocating $0 to a channel). Fallback strategies ensure service continuity if agent fails.

**Long-term Trust:** Built through consistent performance, explainable reasoning, and alignment with business values.

---

## Success Criteria

**Quantitative:**
- ≥10% more conversions than baseline (primary)
- CPA ≤ baseline CPA (efficiency)
- <12% allocation volatility (stability)
- All constraint violations automatically corrected (validation system)

**Qualitative:**
- Clear, data-driven reasoning in decision logs
- Correct identification of channel trends
- Appropriate trade-off articulation (proven performers vs. emerging opportunities)

**Rubric Alignment:**
- Design clarity: Clear role, guardrails linked to ethics & trust
- Functionality: Reads data, proposes allocations, logs reasoning
- Evaluation: Computes outcomes, compares to baseline, reflects on trade-offs
- Scaling: See scaling.md for cloud deployment plan
