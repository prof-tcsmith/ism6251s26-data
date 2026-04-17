# Scenario 23: Job Posting Salary Prediction

## Business Context

TalentScope Analytics is an HR data platform that serves approximately 1,500 corporate clients — primarily talent acquisition teams, compensation analysts, and HR business partners — across the United States. The platform aggregates job postings from major job boards, company career pages, and recruitment APIs, enriching them with metadata about company size, location cost-of-living indices, and industry classification. TalentScope's core product is a salary benchmarking tool that helps companies set competitive compensation for open roles.

A persistent challenge for TalentScope's clients is that the majority of job postings do not include explicit salary information. Depending on the industry, only 20-40% of postings list a salary range. This forces compensation analysts to rely on survey data (expensive, often stale) or ad hoc market research (time-consuming, inconsistent). TalentScope's product team believes that the *text of a job description* — combined with structured posting metadata — contains enough signal to estimate the salary midpoint with useful accuracy, even when no salary is listed.

The Chief Product Officer has commissioned the development of a salary prediction model that will power a new "Estimated Salary" feature in the platform. When a client searches for comparable roles, TalentScope will display the predicted salary alongside actual posted salaries, clearly labeled as an estimate. The model must be accurate enough that clients trust it for budgeting and offer decisions, but not so overconfident that it creates legal liability if a predicted salary is wildly wrong.

Key stakeholders include the Chief Product Officer (owns the feature roadmap), the Data Science team (responsible for model development and monitoring), Enterprise Sales (the feature is a key differentiator in competitive deals), and the Legal/Compliance team (concerned about pay equity implications if the model systematically under- or over-predicts for certain demographics or industries).

## The Problem

Predict the salary midpoint (annual compensation in US dollars, ranging from $30,000 to $250,000) for a job posting based on the job description text and structured posting metadata. This is a **regression** problem with a continuous target.

## Evaluation Criteria

The primary evaluation metric is **Root Mean Squared Error (RMSE)**, which penalizes large prediction errors more heavily than small ones — appropriate because a $50K error on a single posting is far more damaging to client trust than ten $5K errors.

Secondary metrics to consider:
- **Mean Absolute Error (MAE):** More interpretable ("on average, predictions are off by $X").
- **R-squared:** What proportion of salary variance does the model explain?
- **Mean Absolute Percentage Error (MAPE):** Important because a $10K error on a $40K job is much worse than a $10K error on a $200K job. Clients care about relative accuracy.
- **Error distribution by salary range:** Does the model perform equally well across entry-level ($30-50K), mid-range ($70-120K), and executive ($150K+) positions? Systematic under-prediction at the high end (or over-prediction at the low end) could create pay equity concerns.

## Data Description

| Feature | Type | Description |
|---------|------|-------------|
| `job_description` | text | Job posting description text (60-150 words) |
| `years_experience_required` | int | Minimum years of experience listed |
| `education_level` | int (0-4) | 0=High School, 1=Associate, 2=Bachelor, 3=Master, 4=PhD |
| `industry_sector` | int (0-9) | Encoded industry sector |
| `company_size_employees` | int | Number of employees at the company |
| `is_remote` | binary | Whether the position is listed as remote (0/1) |
| `city_cost_of_living_index` | float | Cost-of-living index for the posting location (national avg=100) |
| `num_skills_required` | int | Number of distinct skills listed in requirements |
| `is_senior_title` | binary | Whether the job title contains senior/lead/principal (0/1) |
| `is_management` | binary | Whether the job title indicates management (0/1) |
| `required_clearance` | binary | Whether security clearance is required (0/1) |
| `benefits_score` | int (1-5) | Composite score of benefits package quality |
| `company_age_years` | int | Age of the company in years |
| **`salary_midpoint`** | **int** | **Target: annual salary midpoint in dollars** |

## Text Field Details

The `job_description` column contains 60-150 words of job posting text. The vocabulary and tone of the text carry strong salary signals:

- **Low salary ($30-55K):** Entry-level language — "assist," "support," "coordinate," "data entry," "customer service," "filing," "basic," "follow procedures." Titles like Associate, Coordinator, Clerk.
- **Mid salary ($55-140K):** Professional language — "manage," "lead," "analyze," "develop," "implement," "strategy," "cross-functional," "optimize." Titles like Manager, Analyst, Engineer.
- **High salary ($140K+):** Executive language — "transform," "architect," "envision," "P&L," "enterprise strategy," "board," "global operations." Titles like Director, VP, Principal, Chief.
- **Technical vocabulary boosts salary:** Mentions of "machine learning," "cloud architecture," "distributed systems," "cybersecurity" correlate with higher compensation regardless of seniority level.

The text provides salary signal that is complementary to (but not redundant with) structured features. For example, two jobs both requiring 5 years of experience and a Bachelor's degree may have very different salaries depending on whether the description uses "coordinate team schedules" versus "architect distributed systems."

## Special Considerations

- **Continuous target with skewed distribution:** Salaries are right-skewed. Consider whether log-transforming the target improves model performance.
- **Text vocabulary correlates with structured features but is not redundant:** Senior titles appear in both text and the `is_senior_title` flag, but text captures nuances (e.g., "entry-level manager" vs. "strategic VP") that the binary flag misses. Ablation studies should reveal incremental value of text features.
- **Industry effects in text:** Technology and finance job descriptions use different vocabulary even at similar seniority levels. Industry is encoded in `industry_sector`, but the text may capture sub-industry distinctions not reflected in the 10-category encoding.
- **Non-linear interactions:** The salary premium for a PhD varies dramatically by industry (huge in biotech, modest in retail). Tree-based models may capture these interactions more naturally than linear models.
- **Holdout drift:** The holdout period reflects cost-of-living inflation (higher COL indices), slightly smaller companies (reflecting a startup boom), and marginally higher experience requirements — simulating a labor market shift.
- **Fairness consideration:** If the model learns salary patterns that reflect existing pay inequities, it could perpetuate them. Consider whether certain text features (e.g., gendered language) introduce bias.

## Error Impact Table

| Error Magnitude | Client Impact | Severity |
|----------------|---------------|----------|
| Within $5,000 of true salary | Excellent: client can use estimate for budgeting directly | Acceptable |
| $5,000 - $15,000 off | Moderate: useful as a range anchor but needs human review | Tolerable |
| $15,000 - $30,000 off | Poor: client may set non-competitive offers or over-budget significantly | Concerning |
| $30,000+ off | Unacceptable: destroys trust in the tool; potential legal exposure if used for pay decisions | Critical |
| Systematic under-prediction for high-salary roles | Legal risk: could contribute to lowball offers for senior positions | High |
| Systematic over-prediction for low-salary roles | Budget risk: companies over-allocate compensation budgets | Medium |
