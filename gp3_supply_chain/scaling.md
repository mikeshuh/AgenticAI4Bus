# Scaling Plan: Production Deployment

## Cloud Architecture (GCP)

**Data Pipeline:**
- **Cloud Function** (daily @ 6 AM): Fetch demand data from ERP/WMS systems (SAP, Oracle, NetSuite)
- **Cloud Storage (GCS)**: Store raw demand data, inventory snapshots, and decision logs for audit
- **BigQuery**: Structured warehouse for historical demand, inventory states, decisions, and outcomes

**Optimization Service:**
- **Cloud Run** (daily @ 8 AM): Containerized agent service with Gemini API integration
- **Cloud Scheduler**: Trigger daily replenishment reviews for all SKUs
- **Secret Manager**: Secure storage for API keys (Gemini, ERP/WMS credentials)

**Execution:**
- **Cloud Function**: Human approval workflow → execute orders via ERP API (create purchase orders)
- **Pub/Sub**: Event-driven architecture for approval notifications and order confirmations
- **Email/Slack Integration**: Notify procurement team of recommendations, await approval

---

## Observability

**Logging:**
- Structured JSON logs in Cloud Logging: decision reasoning, inventory states, costs, risk assessments
- 30-day retention for queries, 1-year in BigQuery for analytics and compliance
- Fields: timestamp, SKU, decision, order_qty, current_stock, pending_orders, projected_stock, reasoning

**Monitoring:**
- Custom metrics: daily stockouts by SKU, fill rates, total costs, order frequency, API latency
- Dashboard: Real-time inventory levels, pending orders, safety stock thresholds, cost trends
- Forecast accuracy tracking: Compare EWMA predictions vs. actual demand, adjust alpha if drift detected

**Alerting:**
- **Critical** (PagerDuty/Slack): Agent failure, API quota exceeded, ERP integration failure, stockout on high-priority SKU
- **Warning** (Email): Fill rate drops below 90%, holding costs spike >20%, forecast error increases >30%
- **Info**: Daily summary report with recommendations, cost savings, order confirmations

---

## Reliability & Cost Controls

**Error Handling:**
- Exponential backoff retry (3 attempts) for Gemini API calls
- Circuit breaker: Disable agent after 3 consecutive failures, fallback to baseline reorder point policy
- Fallback strategy hierarchy:
  1. LLM decision (primary)
  2. Simple reorder point logic (if LLM errors)
  3. Conservative safety stock maintenance (if all else fails)
- Health checks: Validate ERP connectivity, Gemini API availability, data freshness before each run

**Rate Limiting:**
- Built-in 3-second delays between API calls (respect 30 RPM Gemini free tier limit)
- Request queue to prevent concurrent optimization runs for same SKU
- Exponential backoff if 429 rate limit errors occur

**Cost Management:**
- **Gemini API**: ~$0.15/month for 3 SKUs (90 calls × ~765 tokens avg × $0.075/1M input tokens)
  - Based on actual results: 68,867 tokens for 90 decisions = ~765 tokens/call
  - Gemini 2.0 Flash-Lite: $0.075/1M input, $0.30/1M output tokens
- **GCP Infrastructure**: ~$15/month (BigQuery, Cloud Run, Cloud Functions, Logging, Monitoring)
- **Total**: <$20/month (~0.01% of typical $200K annual inventory carrying costs)
- **Alerts**: Notify if monthly API costs exceed $50 budget
- **Auto-scaling**: Cloud Run scales to 0 when not in use, only pay for active processing time

**Data Validation:**
- Schema checks on all CSV inputs (demand, inventory, params)
- Sanity checks: demand ≥ 0, stock ≥ 0, lead_time > 0, min_order_qty > 0
- Anomaly detection: Flag unusual demand spikes (>3 std dev) for manual review

---

## Security & Compliance

- **API Keys**: Stored in Secret Manager, rotated every 90 days, never hardcoded or logged
- **IAM Roles**: Least-privilege access (service accounts for BigQuery read/write, ERP API calls)
- **Audit Logs**: All decisions logged immutably in BigQuery (7-year retention for regulatory compliance)
- **Privacy**: Zero PII collection; GDPR/CCPA compliant (aggregate SKU metrics only)
- **Encryption**: Data encrypted at rest (GCS, BigQuery) and in transit (TLS 1.3)
- **Access Control**: Role-based access for procurement (view recommendations), finance (view costs), ops (approve orders)

---

## Deployment Strategy

1. **Week 1-2**: Shadow mode (agent proposes, baseline executes) to validate decision quality
   - Compare agent recommendations vs. what would have been ordered under baseline
   - Review reasoning logs with procurement team for business logic alignment
   - Tune forecast alpha, safety stock buffers if needed

2. **Week 3-4**: Pilot with low-priority SKU (SKU-C)
   - Agent executes orders for SKU-C only, baseline for SKU-A/B
   - Monitor fill rate, costs, and procurement team feedback
   - Validate ERP integration, order placement, and approval workflow

3. **Week 5-6**: Expand to medium-priority SKU (SKU-B)
   - Agent manages SKU-B and SKU-C, baseline for SKU-A
   - Track cost savings, stockout reduction, and operational efficiency

4. **Week 7+**: Full rollout to all SKUs if performance meets criteria
   - ≥10% cost reduction maintained over pilot period
   - Fill rate ≥90% (≥95% for high-priority SKUs)
   - No critical failures or manual overrides >20% of time

**Rollback Triggers:**
- Fill rate drops below 85% for 3 consecutive days
- Total costs increase >15% vs. baseline for 5 consecutive days
- Circuit breaker opens >2x per week
- Procurement team reports >30% manual override rate

---

## Future Enhancements

- **Multi-echelon inventory**: Optimize across distribution centers, regional warehouses, retail stores
- **Demand sensing**: Incorporate external signals (weather, holidays, promotions, social media trends)
- **Advanced forecasting**: Replace EWMA with ML models (LSTM, Prophet) for seasonality and external factors
- **Dynamic safety stock**: Adjust service levels based on actual stockout costs, customer churn rates
- **Supplier reliability**: Model lead time variability, incorporate supplier performance scores
- **Bulk discounts**: Optimize order quantities considering volume pricing tiers
- **Multi-objective optimization**: Balance cost, service level, cash flow, and warehouse capacity simultaneously
- **Real-time adjustments**: Intra-day replenishment reviews if demand spikes detected
- **Automated retraining**: Weekly forecast model updates, drift detection, and alpha tuning
- **Expanded SKU coverage**: Scale from 3 SKUs to 100+ with automated segmentation (ABC analysis)

**Estimated Deployment Effort:** 8-10 weeks with 2-3 engineers (1 backend, 1 data, 1 DevOps)

**Expected ROI:**
- Prototype shows ~10-20% cost reduction potential
- For $200K annual inventory carrying cost → $20-40K savings/year
- Implementation cost: ~$80K (labor) + $240/year (infrastructure)
- Payback period: <6 months
