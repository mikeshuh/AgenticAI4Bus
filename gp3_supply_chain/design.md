# Inventory Replenishment Agent - Design Document

## Agent Role & Objectives

**Role:** Expert supply chain manager that analyzes inventory levels, demand forecasts, and cost parameters to make optimal replenishment decisions.

**Core Objective:** Minimize total cost (holding + stockout) while maintaining target service levels for each SKU.

**Secondary Goals:** (1) Reduce stockouts and maintain high fill rates, (2) Balance proactive ordering vs. wait-and-see strategies, (3) Adapt to different demand patterns (stable, trending, volatile), (4) Provide transparent, explainable decisions.

---

## Inputs & Outputs

**Inputs:**
- Current inventory state: stock level, pending orders
- Demand forecast: EWMA-based average daily demand, forecast error std dev
- SKU parameters: unit cost, holding cost, stockout cost, lead time, min order qty, service level
- Recent demand history: last 7 days for context
- Calculated metrics: safety stock, reorder point, projected inventory position

**Outputs:**
- Order decision: "order" or "wait"
- Order quantity: integer (0 if wait, ≥ min_order_qty if order)
- Reasoning: data-driven rationale explaining decision and trade-offs
- Risk assessment: Low/Medium/High stockout risk if we wait
- Confidence: Low/Medium/High decision confidence
- Decision metadata: timestamp, tokens used, inventory state snapshot

---

## Rules & Guardrails

### Inventory Constraints

1. **Minimum Order Quantity**
   - Respect supplier MOQ (SKU-A: 100, SKU-B: 50, SKU-C: 30)
   - Prevents economically inefficient small orders
   - Reflects real-world supplier contracts

2. **Service Level Targets**
   - SKU-A: 98% (high-priority, stable demand)
   - SKU-B: 95% (standard, trending demand)
   - SKU-C: 90% (acceptable stockouts due to volatility)
   - Safety stock calculated to meet these targets

3. **Lead Time Awareness**
   - Must account for replenishment delay (3-7 days)
   - Consider pending orders (already placed but not yet arrived)
   - Project inventory position over lead time + review period

**Decision Framework:**
- If `projected_stock < safety_stock` → STRONG SIGNAL to order (high stockout risk)
- If `current_stock < reorder_point` and no pending orders → CONSIDER ordering
- If `projected_stock > safety_stock` → MAY WAIT to reduce holding costs
- Balance trade-off: order now (higher holding cost) vs. wait (stockout risk)

### Cost Trade-offs

**Holding Cost vs. Stockout Cost:**
- Holding: $0.08-0.15/unit/day (warehouse storage)
- Stockout: $45-90/unit (3× unit cost, represents lost profit + customer dissatisfaction)
- Agent must balance: over-ordering (wastes cash in inventory) vs. under-ordering (loses sales)

**Service Level Differentiation:**
- High-priority SKUs (SKU-A: 98%) → higher safety stock, more proactive ordering
- Low-priority SKUs (SKU-C: 90%) → accept some stockouts to reduce inventory carrying costs

### Privacy & Trust

- **No Customer PII:** Only aggregate SKU-level demand, no order identifiers or customer data
- **Human-in-the-Loop:** Agent recommends, humans approve and execute orders
- **Transparency:** All decisions logged with complete reasoning and inventory state
- **Audit Trail:** Immutable decision logs with timestamps for compliance

---

## Evaluation Metrics

**Primary Metric:** Total cost (holding + stockout) over test period (days 31-60)
- Agent must beat baseline reorder point policy by ≥10% to demonstrate value

**Secondary Metrics:**
- Total stockouts: Should be ≤ baseline
- Fill rate: Should be ≥90% overall (≥95% for high-priority SKUs)
- Order frequency: Too many orders = inefficient, too few = risk of stockouts
- Reasoning quality: Manual review of decision rationale for data-driven logic

**Baseline Strategy:** Traditional reorder point policy
- Rule: Order min_order_qty when `(current_stock + pending) < reorder_point`
- No LLM, no optimization - just deterministic threshold

**Comparison Method:**
- Train forecast models on days 1-30 (EWMA, calculate safety stock, reorder point)
- Test period days 31-60 (30-day evaluation): Both agents make decisions, simulate actual outcomes
- Compare cumulative costs, stockouts, and fill rates using same demand data
- Note: Data generated for 90 days total, but evaluation uses only first 60 days

---

## Forecasting Methodology

**EWMA (Exponentially Weighted Moving Average):**
- Formula: `forecast[t] = α × actual[t-1] + (1-α) × forecast[t-1]`
- Alpha = 0.3 (balances responsiveness to recent changes vs. stability)
- Advantages: Captures trends, simple, computationally efficient
- Limitation: Lags sudden shifts, no seasonality modeling

**Safety Stock Calculation:**
- Formula: `safety_stock = z_score(service_level) × σ_forecast_error × √(lead_time)`
- Z-scores: 98%→2.05, 95%→1.65, 90%→1.28
- Accounts for forecast uncertainty and lead time duration
- Higher service level → higher safety stock → lower stockout risk but higher holding cost

**Reorder Point:**
- Formula: `reorder_point = (avg_demand × lead_time) + safety_stock`
- Triggers replenishment when inventory position falls below this threshold
- Baseline agent uses this deterministically; optimization agent uses it as guidance

---

## System Prompt Structure

The LLM receives:
1. **SKU parameters:** costs, lead time, min order qty, service level
2. **Inventory state:** current stock, pending orders (with arrival days)
3. **Demand forecast:** avg daily demand, forecast error, recent 7-day history
4. **Policy metrics:** safety stock, reorder point, projected stock over lead time
5. **Decision framework:** guidelines for when to order vs. wait

The LLM returns:
```json
{
  "decision": "order" or "wait",
  "order_qty": 100,
  "reasoning": "Projected stock of 45 units falls below safety stock of 60, creating high stockout risk. Recent demand stable around 50 units/day. Ordering 100 units (min qty) will replenish to safe levels.",
  "risk_assessment": "High",
  "confidence": "High"
}
```

---

## Key Assumptions (Documented)

### Demand Patterns
- **Data Generation**: 90 days of synthetic demand data created; evaluation uses days 1-60
- **SKU-A (Stable)**: ~50 units/day, low variance (±5), predictable
- **SKU-B (Trending)**: Starts at ~20, grows to ~35 by day 90, medium variance
- **SKU-C (Volatile)**: ~10 units/day, high variance (±5-8), random spikes

### Cost Structure
- **Unit Costs**: Realistic wholesale prices ($15-30)
- **Holding Cost**: ~0.5% of unit cost per day (industry standard for warehouse storage)
- **Stockout Cost**: 3× unit cost (represents lost profit + customer goodwill damage)
- **No Order Placement Cost**: Assumes existing logistics contracts (could add $50/order in production)

### Lead Times
- **SKU-A**: 3 days (domestic supplier, fast turnaround)
- **SKU-B**: 7 days (regional supplier, longer logistics)
- **SKU-C**: 5 days (mixed sourcing)
- **Deterministic**: No lead time variability (real-world has uncertainty)

### Service Levels
- **Tiered by Priority**: 98% (critical), 95% (standard), 90% (acceptable stockouts)
- **Safety Stock Calculated**: Based on forecast error and lead time
- **Trade-off**: Higher service level = more inventory = higher holding cost

### Operational
1. **Instant order placement** - Orders placed today arrive exactly on day + lead_time
2. **No supply disruptions** - Suppliers always fulfill, no delays or shortages
3. **No capacity constraints** - Unlimited warehouse space, unlimited cash
4. **Linear costs** - No bulk discounts, expediting fees, or storage capacity limits
5. **Independent SKUs** - No substitution, no bundling, no cross-selling effects
6. **Perfect information** - Demand is known after it occurs, no cancellations or returns

### Limitations
- Short 30-day evaluation period (days 31-60); longer timeframes needed for seasonality and trend validation
- Real supply chains have lead time variability, supplier reliability issues, demand forecast uncertainty
- This is a prototype demonstrating the approach; production requires A/B testing and continuous monitoring

---

## Ethics & Trust Considerations

**Transparency:** Every order decision includes reasoning; decisions are auditable and explainable to procurement teams and finance stakeholders.

**Cost Control:** Agent balances holding costs (cash tied up in inventory) vs. stockout costs (lost revenue), aligning with business financial goals.

**Accountability:** Agent recommends, humans decide. Procurement teams retain final authority and can override for strategic reasons (e.g., anticipated demand spike, supplier negotiations).

**Privacy:** Zero customer PII collection. Only aggregate SKU-level demand data (no order IDs, customer names, or addresses). GDPR/CCPA compliant.

**Bias Mitigation:** Service levels are explicitly set by business policy (98%/95%/90%), not learned by model. Prevents implicit discrimination in prioritization.

**Safety:** Guardrails prevent catastrophic errors (e.g., ordering 0 units when critically low stock). Fallback to simple reorder point logic if LLM fails.

**Long-term Trust:** Built through consistent performance, explainable reasoning, cost effectiveness, and alignment with business values.

---

## Success Criteria

**Quantitative:**
- ≥10% total cost reduction vs. baseline (primary)
- Total stockouts ≤ baseline (maintain service)
- Fill rate ≥90% overall (≥95% for SKU-A)
- Order frequency reasonable (not thrashing with daily orders)

**Qualitative:**
- Clear, data-driven reasoning in decision logs
- Correct identification of stockout risk levels
- Appropriate trade-off articulation (cost vs. service)
- Adapts to different demand patterns (stable/trending/volatile)

**Rubric Alignment:**
- Design clarity: Clear role, guardrails linked to ethics & trust
- Functionality: Reads data, makes decisions, logs reasoning, respects constraints
- Evaluation: Computes costs, compares to baseline, reflects on trade-offs
- Scaling: See scaling.md for cloud deployment plan

---

## Actual Results & Insights

**Overall Performance (30-day test period, days 31-60):**
- ✅ **17.8% total cost reduction** (exceeded 10% target)
- ✅ **92.4% fill rate** (exceeded 90% target)
- ✅ **89 fewer stockouts** vs baseline (31% reduction)
- ✅ **$3,943 savings** for $0.0083 API cost (477,184x ROI)

### Performance by SKU Type

**SKU-A (Stable, CV=0.09):** ⭐ **Outstanding**
- 92.8% cost reduction ($3,827 → $276)
- 100% fill rate (exceeded 98% target)
- 83 fewer stockouts
- **Insight:** Agent excels when demand is predictable; traded 3x higher holding costs for zero stockout costs

**SKU-B (Trending, CV=0.23):** ⚠️ **Modest**
- 3.2% cost reduction ($15,670 → $15,173)
- 79.6% fill rate (missed 95% target)
- 6 fewer stockouts
- **Insight:** 7-day lead time limited both strategies; long lead times constrain optimization potential

**SKU-C (Volatile, CV=0.67):** ❌ **Regression**
- -3.9% cost increase ($2,699 → $2,803)
- 90.6% fill rate (met 90% target)
- No stockout reduction (both had 34)
- **Insight:** High volatility defeats forecast-based optimization; agent over-ordered without benefit

### Key Learnings

1. **Demand Predictability Matters Most**
   - Agent performance correlates inversely with coefficient of variation
   - Stable demand (CV=0.09) → 92.8% improvement
   - Volatile demand (CV=0.67) → -3.9% degradation

2. **Lead Time Limits Responsiveness**
   - Short lead time (3 days, SKU-A) → exceptional results
   - Long lead time (7 days, SKU-B) → modest improvement
   - Lead time reduction may yield more value than optimization sophistication

3. **Service Level Trade-offs**
   - High-priority SKU (98% target) achieved 100% fill rate at 3x holding cost
   - Medium-priority SKU (95% target) missed target despite agent's efforts
   - Low-priority SKU (90% target) met target but at unnecessary cost

4. **Decision Quality**
   - All 90 decisions referenced specific metrics (projected stock, safety stock)
   - Risk assessments aligned with actual inventory positions
   - Agent correctly identified when to order 2x minimum quantity

### Recommendations

1. **Hybrid Strategy:** Use LLM for stable/trending SKUs (high ROI), simple rules for volatile SKUs
2. **Lead Time Focus:** Prioritize operational improvements on long lead time items
3. **Dynamic Calibration:** Adjust safety stock based on recent forecast error, not just historical
4. **Multi-Objective:** Explicitly penalize excess holding costs in volatile scenarios
5. **Extended Testing:** 90-180 day evaluation for seasonal pattern validation
