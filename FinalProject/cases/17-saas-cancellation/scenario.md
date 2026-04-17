# Scenario 17: SaaS Subscription Cancellation Prediction

## Company Background

**CloudMetrics Pro** is a B2B analytics SaaS company founded in 2018. The platform helps small and mid-size businesses track marketing performance, website analytics, and customer engagement metrics through a unified dashboard. The company has grown to 8,500 active subscribers, with three plan tiers:

- **Starter** ($49/month): Basic analytics, 3 users
- **Professional** ($99/month): Advanced analytics, 10 users, integrations
- **Enterprise** ($249/month): Full suite, unlimited users, custom reports, API access

The average customer pays $99/month (Professional tier), and the blended monthly churn rate is approximately 3% (meaning ~18% of customers cancel within any given 60-day window). Customer acquisition cost (CAC) is approximately $600, so losing a customer before they've been active for 6+ months means losing money on the relationship.

## Business Problem

CloudMetrics Pro's retention team has capacity to proactively reach out to approximately 200 at-risk accounts per month with retention interventions: personalized onboarding sessions, usage optimization consultations, temporary discounts, or feature training. These interventions cost approximately $100 per account (staff time + any discount offered) but have a 35% success rate at preventing cancellation.

The challenge is identifying **which** 200 accounts to target. Currently, the retention team uses simple heuristics (e.g., "hasn't logged in for 2 weeks" or "submitted a support ticket mentioning a competitor"). These heuristics catch only the most obvious cases and miss many customers who silently disengage before canceling.

The CEO wants a model that identifies customers likely to cancel within the next 60 days, so the retention team can intervene before the customer has mentally "checked out."

## Stakeholders

- **VP of Customer Success** — Measured on net revenue retention (NRR). Currently at 92%; board target is 97%. Needs to reduce churn by at least 30%.
- **Retention Team Lead** — Has a team of 5 CSMs (Customer Success Managers). Each can handle approximately 40 at-risk accounts per month with meaningful interventions.
- **Head of Product** — Wants to understand WHY customers churn, not just who will churn. Feature importance insights can drive product roadmap decisions.
- **CFO** — Wants clear ROI justification. The retention program costs ~$240K/year ($100/account x 200 accounts x 12 months). Is the investment worth it?

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Intervene** (Predict 1) | **Would have canceled** (Actually 1) | True Positive | **Net +$320** (35% chance of saving $1,200 annual revenue = $420 expected value, minus $100 intervention cost) |
| **Intervene** (Predict 1) | **Would have stayed** (Actually 0) | False Positive | **-$100** (unnecessary retention discount/effort for a loyal customer) |
| **No action** (Predict 0) | **Stays** (Actually 0) | True Negative | **$0** (normal subscription continues) |
| **No action** (Predict 0) | **Cancels** (Actually 1) | False Negative | **-$1,200** (lost annual subscription revenue; may also lose expansion revenue) |

**Key asymmetry:** A lost customer ($1,200) costs **12x** an unnecessary retention effort ($100). This heavily favors recall — it's much better to intervene with a happy customer (minor waste) than to miss a customer about to cancel.

## Target Variable

- `target = 1`: Customer cancels their subscription within the next 60 days
- `target = 0`: Customer renews/remains active beyond 60 days

**Class balance:** Approximately 18% cancellation rate.

## Features

| Feature | Description |
|---------|-------------|
| `account_age_months` | Months since the account was created |
| `monthly_active_users` | Number of unique users who logged in this month |
| `daily_active_users_avg` | Average number of unique users per day this month |
| `feature_adoption_score` | Percentage of available features used at least once (0-100) |
| `num_support_tickets_last_month` | Support tickets submitted in the past 30 days |
| `avg_session_duration_minutes` | Average session length in minutes |
| `login_frequency_weekly` | Average number of login sessions per week |
| `num_integrations_enabled` | Number of third-party integrations connected |
| `contract_type` | 0 = monthly billing, 1 = annual billing |
| `plan_tier` | Current plan (0 = Starter, 1 = Professional, 2 = Enterprise) |
| `num_admin_users` | Number of admin-level users on the account |
| `data_storage_used_pct` | Percentage of storage quota used |
| `num_reports_created_last_month` | Reports/dashboards created in the past 30 days |
| `last_login_days_ago` | Days since any user on the account last logged in |
| `nps_score` | Most recent Net Promoter Score response (0-10) |
| `onboarding_completed` | 1 = completed guided onboarding, 0 = skipped/incomplete |
| `training_sessions_attended` | Number of training webinars/sessions attended |
| `billing_issues_count` | Number of billing-related issues (failed payments, disputes) |
| `competitor_mention_in_tickets` | 1 = support tickets mention a competitor product, 0 = no mention |
| `expansion_revenue_pct` | Percentage of revenue from upsells/add-ons |

## What Makes This Problem Interesting

1. **Usage Trajectories:** It's not just the current level of usage that matters, but the trend. A customer logging in 5 times per week is healthy — but a customer who used to log in 15 times per week and has dropped to 5 is showing a warning sign. The model must infer trajectory from static features (e.g., `last_login_days_ago` captures recent disengagement).

2. **Contract Type as Moderator:** Annual contracts dramatically reduce churn because of the commitment and switching cost. But an annual customer showing deep disengagement signals is at severe risk when renewal time comes. The interaction between contract type and engagement metrics is crucial.

3. **Onboarding Impact:** Customers who complete onboarding AND adopt many features are very sticky. But onboarding alone without follow-through adoption is less protective. This is a classic interaction effect.

4. **Billing as Amplifier:** Billing issues (failed payments, disputes) alone might not cause churn, but combined with other dissatisfaction signals (many support tickets, low NPS), they can be the final straw.

5. **Competitor Mentions:** A customer mentioning a competitor in a support ticket is a very strong signal — but it's rare (~5%). The model must handle this high-signal, low-frequency feature appropriately.

## Evaluation Considerations

Given the retention team's capacity of 200 accounts/month, the operationally relevant question is: of the top 200 accounts your model flags, how many are genuine churn risks? This is a precision-at-K problem. Also consider: if the model identifies 300 at-risk accounts but the team can only contact 200, how should they be prioritized? Well-calibrated probability scores enable this ranking.

---

*Dataset contains 20 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and test.csv (~1,000 rows).*
