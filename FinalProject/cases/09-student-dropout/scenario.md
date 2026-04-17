# Scenario 09: University Student Dropout Prediction

## Business Context

Lakewood State University is a public four-year institution with approximately 15,000 undergraduate students. Over the past five years, the university's six-year graduation rate has stagnated at 58%, well below the institutional target of 68% and the peer-group average of 63%. The 22% first-to-second-year dropout rate is the primary driver of this gap. Each student who drops out represents not only a personal loss for the individual but also a financial loss for the institution: foregone tuition revenue over the remaining years of enrollment averages $35,000, and high dropout rates negatively impact the university's rankings, accreditation standing, and ability to attract future students.

The Provost has launched the "Student Success Initiative," a data-driven early warning system that identifies students at high risk of dropping out so that targeted interventions can be deployed. These interventions include mandatory academic advising sessions, peer tutoring, emergency financial assistance, and mental health referrals. The average cost of a full intervention package is approximately $2,000 per student per semester. When applied to students who were not actually at risk of dropping out, this investment is wasted -- though the advising and tutoring may still provide marginal benefit, the core cost is considered sunk.

The institutional research office has compiled a dataset linking admissions records (high school GPA, SAT scores), enrollment data (course load, withdrawals, major declaration), engagement metrics (library usage, advisor meetings, extracurricular participation), financial data (aid, unmet need), and academic performance (semester GPAs) with the ultimate outcome: whether the student completed their degree or dropped out. The dataset includes only students who have either graduated or formally withdrawn; currently enrolled students are excluded.

The Dean of Students has raised an important concern: the model should be used to provide additional support, never to discourage or exclude students. A student identified as high-risk should receive more resources, not fewer opportunities. The university's commitment to access and equity means that first-generation and Pell-eligible students, who are overrepresented in the at-risk population, should receive culturally sensitive interventions.

## Key Stakeholders

- **Provost:** Champions the initiative and is accountable to the Board of Trustees for graduation rate improvement.
- **Dean of Students:** Oversees student support services; manages the intervention budget and staff capacity.
- **Academic Advisors:** Will use the model's risk scores to prioritize outreach; need to understand why specific students are flagged.
- **Financial Aid Office:** Can deploy emergency grants to students with unmet financial need who are at risk of dropping out.
- **Institutional Research:** Maintains the data infrastructure and is responsible for model validation and bias auditing.
- **Enrollment Management:** Concerned about both retention (keeping current students) and reputation (graduation rates affect future enrollment).

## Cost Structure

| Prediction | Actual | Outcome | Cost |
|---|---|---|---|
| Persists (0) | Persists (0) | True Negative | $0 |
| Drops Out (1) | Drops Out (1) | True Positive | $2,000 (intervention deployed; may prevent dropout, saving $35,000) |
| Drops Out (1) | Persists (0) | **False Positive** | **$2,000** (unnecessary intervention for student who would have stayed) |
| Persists (0) | Drops Out (1) | **False Negative** | **$35,000** (student drops out without receiving support) |

## Special Considerations

- The FN/FP cost ratio is 17.5:1. Missing an at-risk student is far more costly than providing unnecessary support.
- GPA trajectory matters more than the absolute GPA level. A student whose GPA is declining from 3.5 to 2.8 may be at higher risk than a student with a stable 2.5, because the decline signals a developing problem.
- Financial need interacts with first-generation status: first-generation students with high unmet financial need face compounding barriers that are more than additive.
- Being undeclared in a major is a risk factor on its own, but it becomes much more dangerous when combined with low campus engagement (zero extracurriculars).
- Part-time work hours have a non-linear relationship with dropout: moderate work (10-15 hours/week) is actually slightly protective (financial stability, time management skills), but excessive work (20+ hours/week) significantly increases dropout risk.
- Several features are correlated: SAT score and high school GPA are positively correlated; is_pell_eligible and is_first_generation overlap substantially; credit_hours_completed and credit_hours_attempted are highly correlated by construction.
- The high_school_gpa and sat_score features capture pre-college preparation but become less predictive once college GPA data is available, testing whether models appropriately weight current vs. historical performance.
