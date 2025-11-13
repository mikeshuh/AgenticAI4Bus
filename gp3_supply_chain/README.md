# Inventory Replenishment Agent

An intelligent agent that optimizes inventory replenishment decisions using LLM-powered reasoning to minimize costs while maintaining service levels across multiple SKUs.

---

## How to Run

### 1. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn scipy python-dotenv google-generativeai
```

### 2. Set Up API Key
Get a free Gemini API key at https://ai.google.dev/ and create a `.env` file:
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 3. Run the Notebook
```bash
jupyter notebook inventory_replenishment_agent.ipynb
# Then: Kernel → Restart & Run All
```

**Expected Runtime:** ~4.5 minutes (includes 90 API calls with 3-second delays for 3 SKUs over 30 test days)

---

## Results Snapshot

Evaluation over days 31-60 (30-day test period) for 3 SKUs:

| Strategy | Total Cost | Total Stockouts | Overall Fill Rate | API Cost |
|----------|------------|-----------------|-------------------|----------|
| **Optimization Agent** | $18,251.75 | 201 units | 92.4% | $0.0083 |
| **Baseline (Reorder Point)** | $22,195.22 | 290 units | 89.1% | $0 |

**Key Metrics:**
- **17.8% cost improvement** vs baseline ($3,943 savings)
- **89 unit stockout reduction** (31% fewer stockouts)
- **92.4% fill rate achieved** (exceeds 90% target)
- **477,184x ROI** ($3,943 savings / $0.0083 API cost)

**Performance by SKU:**
- **SKU-A (Stable)**: 92.8% cost reduction, 100% fill rate (outstanding)
- **SKU-B (Trending)**: 3.2% cost reduction, 79.6% fill rate (modest)
- **SKU-C (Volatile)**: -3.9% cost increase, 90.6% fill rate (slight regression)

---

## Key Assumptions

### Demand Model
1. **EWMA Forecasting** - Exponentially weighted moving average with alpha=0.3 captures demand trends
2. **Training Period** - Days 1-30 used to build forecast models, days 31-60 for evaluation (30-day test period)
3. **Demand Patterns**:
   - SKU-A: Stable, high-volume (~50 units/day, low variance)
   - SKU-B: Trending, medium-volume (20→35 units/day, medium variance)
   - SKU-C: Volatile, low-volume (~10 units/day, high variance with spikes)

### Cost Structure
- **Unit Costs**: SKU-A: $15, SKU-B: $30, SKU-C: $25
- **Holding Cost**: ~0.5% of unit cost per day (warehouse storage)
- **Stockout Cost**: 3× unit cost (lost profit + customer dissatisfaction)
- **No Order Costs**: Assumes fixed logistics arrangements (could add $50/order in production)

### Inventory Policy
- **Service Levels**: SKU-A: 98%, SKU-B: 95%, SKU-C: 90% (reflects product priority)
- **Lead Times**: SKU-A: 3 days, SKU-B: 7 days, SKU-C: 5 days (different suppliers)
- **Minimum Order Quantities**: SKU-A: 100, SKU-B: 50, SKU-C: 30 units
- **Safety Stock**: Calculated as `z_score(service_level) × forecast_error_std × sqrt(lead_time)`
- **Reorder Point**: `(avg_demand × lead_time) + safety_stock`

### Operational Assumptions
1. **Instant order placement** - Orders placed on day N arrive on day N + lead_time
2. **No supply disruptions** - Lead times are deterministic, no supplier failures
3. **No capacity constraints** - Can always fulfill orders up to stock level
4. **Linear costs** - No bulk discounts, volume breaks, or expediting fees
5. **Independent SKUs** - No substitution effects or cross-selling impacts

### Evaluation Method
- **Training period**: Days 1-30 (build forecast models)
- **Test period**: Days 31-60 (30-day evaluation)
- **Baseline strategy**: Simple reorder point policy (no LLM optimization)
- **Simulation**: Both strategies operate on same actual demand data
- **Success criteria**: Lower total cost, fewer stockouts, maintain fill rate ≥90%

---

## Files

- `sales.csv` - 90 days of demand data for 3 SKUs (270 rows)
- `inventory.csv` - Opening stock levels per SKU (3 rows)
- `params.csv` - Cost and policy parameters per SKU (3 rows)
- `inventory_replenishment_agent.ipynb` - Main implementation notebook
- `agent_decision_log.json` - Full decision log with reasoning (generated after notebook run)
- `evaluation_results.png` - Visualization charts (generated after notebook run)
- `design.md` - Design document (agent role, guardrails, evaluation)
- `scaling.md` - Production deployment plan (cloud architecture, costs)
- `README.md` - This file
- `generate_data.py` - Script to regenerate CSV files

---

## Notes

**Limitations:**
- Simplified cost model (no order placement costs, no bulk discounts)
- Deterministic lead times (real supply chains have variability)
- Short 30-day evaluation period
- No external factors (seasonality, promotions, competitor actions)

**Ethics & Trust:**
- No customer PII (only aggregate SKU-level demand)
- Human-in-the-loop (agent recommends, humans approve orders)
- Transparent reasoning (all decisions logged with rationale)
- Audit trail (complete decision history with timestamps)
- Cost controls (API budget limits, fallback to simple rules if LLM fails)

See `design.md` for detailed architecture and `scaling.md` for production deployment plan.
