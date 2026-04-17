# Scenario 22: Support Ticket Department Routing

## Business Context

TechNova Software is a mid-market B2B SaaS platform serving over 3,000 enterprise clients across industries including financial services, healthcare, logistics, and retail. The platform provides a suite of tools for project management, data analytics, team collaboration, and workflow automation. TechNova's customer support operation handles an average of 1,200 tickets per day across six specialized departments: Billing, Technical, Account Management, Security, Onboarding, and Feature Requests.

Currently, incoming tickets are triaged manually by a small frontline team that reads each ticket description and routes it to the appropriate department. This process wastes roughly 40% of support staff time on rerouting misclassified tickets — a Technical issue sent to Billing, a Security concern misrouted to Account Management, and so on. The average time-to-resolution for correctly routed tickets is 4.2 hours; for misrouted tickets, it balloons to 14.8 hours due to the handoff delay. Customer satisfaction scores drop by an average of 22 points (on a 100-point scale) when a ticket is rerouted even once.

The VP of Customer Success has championed the development of an automated routing system that reads the ticket description alongside customer account metadata to predict the correct department. The system does not need to be perfect — even 85% first-contact routing accuracy would cut rerouting volume in half and save an estimated $1.2 million annually in labor costs. The Security team, however, has insisted that Security-related tickets must have near-perfect recall: a missed security incident routed to Billing could delay response to an active data breach by hours.

Key stakeholders include the VP of Customer Success (owns support metrics), Department Leads (each department wants accurate routing to avoid being overwhelmed with irrelevant tickets), the Security team (zero tolerance for missed security issues), and the Onboarding team (new customers with routing delays during their first weeks are 3x more likely to churn).

## The Problem

Predict which of 6 departments (Billing, Technical, Account, Security, Onboarding, Feature_Request) a support ticket should be routed to, based on the ticket description text and customer account metadata. This is a **multi-class classification** problem with 6 classes.

## Evaluation Criteria

The primary metric is **weighted F1 score**, reflecting overall routing accuracy weighted by class frequency. However, several class-specific considerations override a pure aggregate metric:

- **Security recall must be very high (>90%):** Missing a security incident is the highest-cost error. A Security ticket misrouted to any other department introduces dangerous delay.
- **Onboarding precision matters:** New customers misrouted out of Onboarding have poor first experiences. False positives (non-Onboarding tickets sent to Onboarding) waste the specialized onboarding team's time.
- **Technical vs. Account confusion is expected:** "I can't log in" could be a Technical issue (system bug) or an Account issue (wrong credentials). The model should handle this gracefully, and some misclassification between these two is tolerable.

Consider examining the **confusion matrix** carefully to identify which department pairs are most often confused and whether those confusions align with genuinely ambiguous tickets.

## Data Description

| Feature | Type | Description |
|---------|------|-------------|
| `ticket_description` | text | Customer's support ticket text (30-100 words) |
| `customer_tier` | int (0-3) | Customer tier: 0=Free, 1=Starter, 2=Professional, 3=Enterprise |
| `account_age_months` | int | Months since account creation |
| `num_open_tickets` | int | Number of currently open tickets for this customer |
| `priority_level` | int (1-3) | Ticket priority: 1=High, 2=Medium, 3=Low |
| `submission_hour` | int (0-23) | Hour of day the ticket was submitted |
| `is_weekend` | binary | Whether submitted on a weekend (0/1) |
| `num_users_on_account` | int | Number of user seats on the customer account |
| `monthly_spend` | float | Customer's monthly subscription spend in dollars |
| `product_module` | int (0-5) | Encoded product module the ticket relates to |
| `days_since_last_ticket` | int | Days since the customer's previous ticket |
| `escalation_history_count` | int | Number of previous ticket escalations for this customer |
| **`department`** | **categorical** | **Target: routing department (6 classes)** |

## Text Field Details

The `ticket_description` column contains customer-written support ticket text, typically 30-100 words. Each department has a characteristic vocabulary:

- **Billing:** invoice, charge, payment, refund, credit, subscription, renewal, pricing
- **Technical:** error, crash, bug, loading, timeout, API, integration, database, performance
- **Account:** password, login, access, permission, user, role, admin, SSO, authentication
- **Security:** breach, unauthorized, suspicious, vulnerability, compliance, audit, encryption
- **Onboarding:** setup, getting started, tutorial, configuration, migration, training, guide
- **Feature_Request:** feature, capability, enhancement, improvement, functionality, suggest

Approximately 8% of tickets contain language from multiple department vocabularies, creating genuine ambiguity. For example, "I can't access my account after the system update" could reasonably be Technical or Account. These ambiguous tickets are where structured features (like `account_age_months` for Onboarding, or `priority_level` for Security) provide the most incremental value.

## Special Considerations

- **Uneven class sizes:** Technical (30%) and Billing (25%) dominate, while Security (8%) and Feature_Request (10%) are minority classes. Class weighting or stratified approaches may be important.
- **Safety-critical minority class:** Security tickets are rare but high-impact. Standard accuracy optimization may sacrifice Security recall in favor of majority-class performance.
- **Structured features complement text:** Account age strongly predicts Onboarding tickets (new customers). Priority level correlates with Security and Technical. Monthly spend correlates with Billing complexity. These signals help disambiguate when text alone is insufficient.
- **Cross-department ambiguity:** Some tickets genuinely span departments. The model should be evaluated not just on hard accuracy but on whether its confusions are reasonable (Technical-Account confusion is forgivable; Security-Feature_Request confusion is not).
- **Evaluation drift:** The test period reflects higher customer spending (price increases), slightly older accounts, and more open tickets per customer — simulating platform growth.

## Cost/Impact Table

| Misrouting Error | Business Impact | Severity |
|-----------------|-----------------|----------|
| Security to any other dept | Delayed response to potential data breach; regulatory and reputational risk | **Critical** |
| Any dept to Security | Security team investigates non-issue; wastes scarce security analyst time | High |
| Onboarding to Technical | New customer gets technical support instead of guided onboarding; poor first experience, churn risk | High |
| Technical to Account | Customer with a system bug is told to reset password; frustration and delay | Medium |
| Account to Technical | Customer with login issue enters technical queue; slower resolution but eventually rerouted | Medium |
| Billing to Feature_Request | Invoice dispute sits unresolved; customer payment delays | Medium |
| Feature_Request to Billing | Feature suggestion treated as billing inquiry; minor annoyance | Low |
| Any misroute (general) | Average 10.6 hours added to resolution time; 22-point CSAT drop | Medium |
