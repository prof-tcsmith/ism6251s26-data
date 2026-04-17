# Scenario 02: Employee Attrition Prediction

## Business Context

TechVantage Solutions is a mid-size technology company with approximately 5,000 employees spread across seven departments including Engineering, Product, Sales, Marketing, Operations, HR, and Finance. Over the past two years, the company has experienced a voluntary attrition rate of roughly 20%, which is significantly above the industry average of 13%. The cost of replacing a departing employee -- factoring in recruiting fees, onboarding time, lost institutional knowledge, and reduced team productivity during the transition -- averages $45,000 per departure.

The VP of People Operations has partnered with the analytics team to build a predictive model that identifies employees at high risk of leaving within the next 12 months. The plan is to use model predictions to proactively offer targeted retention interventions: additional compensation, role changes, mentorship programs, or flexible work arrangements. These retention packages cost approximately $5,000 per employee, so offering them to employees who were never going to leave represents a real but manageable waste.

The HR analytics team has compiled a dataset from the HRIS (Human Resource Information System) combining compensation data, performance reviews, engagement surveys, organizational tenure information, and demographic attributes. All data has been pre-encoded numerically. The satisfaction_score comes from the most recent annual engagement survey and ranges from 1 to 10, while manager_rating and performance_rating come from the formal review cycle.

A key concern raised by the CHRO is that the model must not become a self-fulfilling prophecy. If high-risk employees are treated differently in ways they perceive negatively (such as being excluded from stretch assignments because leadership assumes they are leaving), the intervention could backfire. The model should therefore be used only to trigger positive retention efforts, and its predictions should not be shared with line managers directly.

## Key Stakeholders

- **VP of People Operations:** Owns the retention program; needs to allocate limited retention budget to highest-risk employees.
- **Department Heads:** Want early warning about potential departures so they can begin succession planning without demoralizing teams.
- **Finance:** Tracks cost of attrition and ROI on retention spending; needs justification that model-driven interventions save money.
- **Legal/Ethics:** Concerned about potential bias in predictions (e.g., if the model disproportionately flags employees of certain ages or departments).

## Cost Structure

| Prediction | Actual | Outcome | Cost |
|---|---|---|---|
| Stays (0) | Stays (0) | True Negative | $0 |
| Leaves (1) | Leaves (1) | True Positive | $5,000 (retention offer, potentially prevents the departure) |
| Leaves (1) | Stays (0) | **False Positive** | **$5,000** (unnecessary retention offer to employee who was staying) |
| Stays (0) | Leaves (1) | **False Negative** | **$45,000** (employee departs, full replacement cost) |

## Special Considerations

- The FN/FP cost ratio is 9:1. Missing a departure is much more expensive than an unnecessary retention offer, but the FP cost is not negligible.
- Salary has a non-linear effect on attrition: very high salaries reduce attrition significantly, but mid-range salaries do not provide much protection.
- There is a critical interaction between tenure and promotion history: long-tenured employees who have not been promoted recently are at elevated risk, especially if they are also high performers.
- Satisfaction scores below 3 are a strong signal, but the relationship is not purely linear across the full range.
- The department feature is encoded 0-6 but acts mostly as a noise/confounding variable in this dataset; attrition patterns are driven more by individual-level factors.
- Ethical review of the model's predictions across demographic groups (age, in particular) is strongly recommended before deployment.
