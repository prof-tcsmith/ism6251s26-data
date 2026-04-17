# Scenario 06: Hospital Readmission Risk Prediction

## Business Context

MercyFirst Health System is a regional hospital network comprising four acute care hospitals and twelve outpatient clinics, serving a mixed urban-suburban population of approximately 800,000 people. The system discharges roughly 45,000 inpatients per year, with an overall 30-day readmission rate of approximately 18%. Under the CMS Hospital Readmissions Reduction Program (HRRP), MercyFirst has been penalized $3.2 million in the current fiscal year for excess readmissions in targeted conditions including heart failure, pneumonia, and COPD.

The Chief Medical Officer has launched a "Transition of Care" initiative that uses predictive analytics to identify patients at high risk of readmission at the time of discharge. High-risk patients receive an enhanced post-discharge care bundle: a follow-up phone call within 48 hours, a home health visit within one week, medication reconciliation by a clinical pharmacist, and priority scheduling for a follow-up appointment. This care bundle costs approximately $500 per patient in direct expenses. When applied to patients who would not have been readmitted anyway, it represents a well-intentioned but unnecessary expenditure.

The cost of a missed readmission is substantial. The direct cost of an unplanned readmission averages $12,000 in hospital charges, but the total impact including CMS penalties (which are calculated at the hospital level, not per-patient), lost patient satisfaction scores, and downstream reputation effects is estimated at $25,000 per avoidable readmission. The analytics team has assembled a retrospective dataset linking discharge records with 30-day readmission outcomes, combining clinical features (lab values, diagnoses, procedures), utilization features (prior admissions, ER visits), and social determinant proxies (insurance type, discharge disposition).

The CMO has emphasized that the model is intended as a safety net, not a replacement for clinical judgment. Physicians will always have the final say on discharge planning, but the model's risk score will be displayed in the electronic health record to inform their decisions.

## Key Stakeholders

- **Chief Medical Officer (CMO):** Champions the initiative; accountable for quality metrics and CMS penalties.
- **Hospitalists/Discharge Planners:** Make discharge decisions; need actionable risk scores at the point of care, not post hoc analysis.
- **Care Coordination Team:** Executes the enhanced post-discharge bundle; limited to approximately 300 interventions per month across the system.
- **Finance/Revenue Cycle:** Tracks CMS penalty exposure and the ROI of readmission prevention efforts.
- **Patient Experience:** Monitors HCAHPS scores; readmissions negatively impact patient satisfaction ratings.

## Cost Structure

| Prediction | Actual | Outcome | Cost |
|---|---|---|---|
| No Readmit (0) | No Readmit (0) | True Negative | $0 |
| Readmit (1) | Readmit (1) | True Positive | $500 (enhanced care bundle; potentially prevents readmission) |
| Readmit (1) | No Readmit (0) | **False Positive** | **$500** (unnecessary enhanced care for patient who was fine) |
| No Readmit (0) | Readmit (1) | **False Negative** | **$25,000** (unplanned readmission + CMS penalty exposure) |

## Special Considerations

- The FN/FP cost ratio is 50:1. Missing a readmission is far more costly, but the $500 per FP is not trivial at scale.
- Age interacts with clinical complexity: elderly patients with many diagnoses are at dramatically higher risk than either factor alone would suggest.
- Length of stay has a U-shaped relationship with readmission: very short stays (premature discharge) and very long stays (severely ill) both predict readmission, while moderate stays do not.
- Lab value interactions are clinically meaningful: low hemoglobin combined with elevated creatinine indicates simultaneous anemia and kidney dysfunction, which is a much stronger risk factor than either alone.
- Several features serve as proxies for social determinants of health: insurance type, discharge disposition, and number of ER visits capture socioeconomic factors that influence post-discharge outcomes.
- The num_procedures and num_lab_tests features are somewhat noisy -- higher values can indicate either sicker patients (more risk) or more thorough care (potentially less risk).
- The primary_diagnosis_category is encoded 0-8 but different categories carry very different baseline readmission risks, which may require the model to learn category-specific patterns.
