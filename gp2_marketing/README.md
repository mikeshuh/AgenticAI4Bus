# Ad Optimization Agent

An intelligent agent that allocates daily advertising budgets across multiple channels to maximize conversions using LLM-powered reasoning and iterative learning.

---

## How to Run

### 1. Install Dependencies
```bash
pip install requirements.txt
```

### 2. Set Up API Key
Get a free Gemini API key at https://ai.google.dev/ and create a `.env` file:
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 3. Run the Notebook
```bash
jupyter notebook ad_optimization_agent.ipynb
# Then: Kernel → Restart & Run All
```

**Expected Runtime:** 2-3 minutes (includes 16 API calls with 2-second delays)

---

## Results Snapshot

Evaluation over days 15-30 (16-day test period):

| Strategy | Total Conversions | Total Spend | Avg CPA | API Cost |
|----------|-------------------|-------------|---------|----------|
| **Optimization Agent** | 1,329 | $16,000 | $12.04 | $0.001 |
| **Baseline (Equal Split)** | 1,116 | $16,000 | $14.34 | $0 |

**Key Metrics:**
- **+19.1% improvement** in total conversions vs baseline
- **-16.0% reduction** in average cost per acquisition (CPA)
- **3.69% allocation volatility** per channel (stable, predictable strategy)
- **15,595 tokens** used across 16 API calls

**Typical Allocation Strategy:**
- Search: 50-55% (best performer, stable, lowest CPA ~$9)
- Social: 30-35% (improving trend, medium CPA ~$15)
- Display: 15-20% (minimum to maintain presence, highest CPA ~$35)

---

## Key Assumptions

### Performance Model
1. **Past performance predicts future** - Channel conversion rates remain relatively stable over 30 days
2. **Channel independence** - No cross-channel attribution effects
3. **Linear scaling** - Doubling budget doubles conversions (no diminishing returns)
4. **No external factors** - No seasonality, competitor changes, or creative fatigue

### Business Constraints
- **Fixed daily budget:** $1000 total allocation
- **Min/max bounds:** Each channel receives 15-60% of budget
- **Daily shift limit:** ±25% maximum change from previous day
- **Multi-channel presence:** All three channels receive budget every day

### Data
- **Training period:** Days 1-14 (build performance model)
- **Test period:** Days 15-30 (optimization vs baseline)
- **Channels:** Search (high-intent), Social (brand awareness), Display (reach)
- **Metrics:** Spend, impressions, clicks, conversions per channel per day

### Evaluation Method
- **Baseline strategy:** Equal 33.3% split across all channels (no optimization)
- **Simulation:** Both strategies use same performance model for fair comparison
- **Noise:** Realistic variance added based on historical volatility
- **Success criteria:** ≥10% conversion improvement, CPA ≤ baseline, <12% volatility

---

## Files

- `ad_performance_data.csv` - 30 days of mock ad performance data (3 channels)
- `ad_optimization_agent.ipynb` - Main implementation notebook
- `design.md` - Design document (agent role, guardrails, evaluation)
- `scaling.md` - Production deployment plan (cloud architecture, costs)
- `README.md` - This file

---

## Notes

**Limitations:**
- Simplified performance model (no auction dynamics, no attribution complexity)
- Short 16-day evaluation period
- Simulated outcomes (not tested on real ad platforms)

**Ethics & Privacy:**
- No PII collection (aggregate channel metrics only)
- Human-in-the-loop (agent recommends, humans approve)
- Transparent reasoning (all decisions logged with rationale)
- Audit trail (complete decision history with timestamps)

See `design.md` for detailed architecture and `scaling.md` for production deployment plan.
