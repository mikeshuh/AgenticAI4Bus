# Scaling Plan: Production Deployment

## Cloud Architecture (GCP)

**Data Pipeline:**
- **Cloud Function** (daily @ 2 AM): Fetch performance data from ad platform APIs (Google Ads, Facebook, etc.)
- **Cloud Storage (GCS)**: Store raw CSV files for audit trail
- **BigQuery**: Structured warehouse for performance history and decision logs

**Optimization Service:**
- **Cloud Run** (daily @ 8 AM): Containerized agent service with Gemini API integration
- **Cloud Scheduler**: Trigger daily optimization runs
- **Secret Manager**: Secure API key storage (Gemini, ad platforms)

**Execution (Optional):**
- **Cloud Function**: Await human approval → execute allocations via platform APIs
- **Pub/Sub**: Event-driven approval workflow

---

## Observability

**Logging:**
- Structured JSON logs in Cloud Logging (decision reasoning, metrics, violations)
- 30-day retention for queries, 1-year in BigQuery for analytics

**Monitoring:**
- Custom metrics: daily conversions, CPA by channel, allocation drift, API costs
- Dashboard: Real-time allocation view, conversion trends, system health

**Alerting:**
- **Critical** (PagerDuty): Agent failure, API quota exceeded, data ingestion failure
- **Warning** (Slack): CPA spike >30%, conversions drop >20%, high constraint violations

---

## Reliability & Cost Controls

**Error Handling:**
- Exponential backoff retry (3 attempts) for Gemini API calls
- Circuit breaker: Disable agent after 3 consecutive failures
- Fallback strategy: Previous allocation → rolling average → CPA-based → equal split

**Rate Limiting:**
- Built-in 2-second delays between API calls (respect 30 RPM Gemini limit)
- Request queue to prevent concurrent optimization runs

**Cost Management:**
- **Gemini API**: ~$0.003/month (30 calls × ~800 tokens × $0.075/1M tokens)
- **GCP Infrastructure**: ~$13.50/month (BigQuery, Cloud Run, Logging, Monitoring)
- **Total**: <$15/month (~0.05% of $30K monthly ad spend)
- **Alerts**: Notify if monthly costs exceed $50 budget

---

## Security & Compliance

- **API Keys**: Stored in Secret Manager, never hardcoded
- **IAM Roles**: Least-privilege access (service accounts for BigQuery read/write, logging)
- **Audit Logs**: All decisions logged immutably in BigQuery (7-year retention)
- **Privacy**: Zero PII collection; GDPR/CCPA compliant (aggregate metrics only)

---

## Deployment Strategy

1. **Week 1-2**: Shadow mode (agent proposes, baseline executes) to validate decision quality
2. **Week 3**: 25% rollout (agent executes Monday/Wednesday, baseline other days)
3. **Week 4-5**: Gradual increase to 50%, then 75%
4. **Week 6+**: Full rollout if performance meets criteria (≥10% conversion improvement, stable CPA)

**Rollback Triggers:**
- Conversions drop >15% for 3 consecutive days
- CPA increases >20% for 5 consecutive days
- Circuit breaker opens >1x per week

---

## Future Enhancements

- **Multi-objective optimization**: Balance conversions + brand awareness + CLV
- **Advanced modeling**: Diminishing returns curves, multi-touch attribution, seasonality
- **Real-time adjustments**: Intra-day budget pacing based on hourly performance
- **Automated retraining**: Weekly performance model updates, drift detection
- **Expanded channels**: Support 10+ channels with dynamic selection

**Estimated Deployment Effort:** 6-8 weeks with 1-2 engineers
