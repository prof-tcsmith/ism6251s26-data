# Scenario 25: Patient Triage Priority Classification

## Business Context

EmergoCare Health Network operates 14 emergency departments across a large metropolitan area, treating approximately 850,000 patients annually. The emergency departments range from Level I trauma centers to community hospital ERs, and they collectively employ over 200 triage nurses who perform the critical function of assessing each arriving patient and assigning a triage level that determines how quickly the patient is seen by a physician.

EmergoCare currently uses the Emergency Severity Index (ESI), a five-level system where Level 1 (Immediate) patients are seen within minutes and Level 5 (Non-Urgent) patients may wait several hours. In practice, EmergoCare has consolidated this into four operational levels: Immediate (1), Emergent (2), Urgent (3), and Non-Urgent (4). Triage accuracy is literally a life-or-death decision: an Immediate patient mistakenly classified as Urgent could wait 30-60 minutes for physician contact, potentially resulting in irreversible harm or death. Conversely, over-triaging Non-Urgent patients as Emergent clogs the fast-track system and delays care for genuinely sick patients.

The Chief Medical Officer and the Director of Emergency Services have initiated a pilot program to develop an AI-assisted triage tool. The tool would analyze the triage nurse's free-text chief complaint notes alongside objective vital signs and patient metadata to suggest a triage level. **The tool is explicitly designed as a decision-support aid, not an autonomous classifier** — the triage nurse always makes the final decision. However, the system should flag cases where the suggested triage level differs from what the nurse entered, prompting a second look. In particular, the system should be biased toward higher acuity: it is far better to over-triage (err toward more urgent) than under-triage (err toward less urgent).

Key stakeholders include the Chief Medical Officer (accountable for patient safety outcomes), the Director of Emergency Services (manages staffing and flow), Triage Nurses (primary users who must trust the tool), the Quality Assurance team (monitors triage accuracy and adverse events), and Risk Management/Legal (concerned about liability if the tool contributes to under-triage of a critical patient).

## The Problem

Predict the triage level (1=Immediate, 2=Emergent, 3=Urgent, 4=Non-Urgent) for an emergency department patient based on the triage nurse's chief complaint notes and objective clinical measurements. This is a **multi-class classification** problem with 4 ordered classes, where misclassification costs are highly asymmetric.

## Evaluation Criteria

This is a **safety-critical application** where standard aggregate metrics are insufficient. The evaluation framework must prioritize patient safety:

- **Primary metric: Weighted F1 score** for overall performance tracking.
- **Critical safety metric: Recall for Immediate (Level 1) and Emergent (Level 2) classes.** Missing a truly Immediate patient (classifying as Urgent or Non-Urgent) is the worst possible error. Recall for Level 1 should exceed 95%; recall for Level 2 should exceed 85%.
- **Under-triage rate:** The percentage of patients assigned a *less* urgent level than their true level. This must be minimized, especially for Levels 1 and 2.
- **Over-triage rate:** The percentage of patients assigned a *more* urgent level than their true level. Some over-triage is acceptable and even desirable — it is the safer error direction.

A model that achieves 90% overall accuracy but only 70% recall for Immediate patients is **unacceptable** and dangerous. A model that achieves 80% overall accuracy with 98% recall for Immediate patients and moderate over-triage is **preferred**.

## Data Description

| Feature | Type | Description |
|---------|------|-------------|
| `chief_complaint_notes` | text | Triage nurse's free-text notes (20-80 words) |
| `age` | int | Patient age in years |
| `heart_rate` | int | Heart rate (beats per minute) |
| `blood_pressure_systolic` | int | Systolic blood pressure (mmHg) |
| `blood_pressure_diastolic` | int | Diastolic blood pressure (mmHg) |
| `temperature_f` | float | Body temperature in Fahrenheit |
| `respiratory_rate` | int | Respiratory rate (breaths per minute) |
| `oxygen_saturation` | float | Blood oxygen saturation percentage (SpO2) |
| `pain_score` | int (0-10) | Patient-reported pain score |
| `arrival_mode` | int (0-2) | 0=Walk-in, 1=Ambulance, 2=Transfer from another facility |
| `time_of_arrival_hour` | int (0-23) | Hour of arrival at the ED |
| `is_weekend` | binary | Whether arrival is on a weekend (0/1) |
| `num_previous_er_visits` | int | Number of previous ER visits in the past year |
| `has_chronic_condition` | binary | Whether patient has a documented chronic condition (0/1) |
| `currently_on_medications` | binary | Whether patient is currently on medications (0/1) |
| `allergies_count` | int | Number of documented allergies |
| `bmi` | float | Body mass index |
| **`triage_level`** | **string** | **Target: triage priority level — one of `Immediate`, `Emergent`, `Urgent`, `Non-Urgent` (ordinal from highest to lowest severity). Encode with `LabelEncoder` or an explicit ordinal mapping before fitting models that require integer targets (e.g. XGBoost).** |

## Text Field Details

The `chief_complaint_notes` column contains the triage nurse's free-text documentation, typically 20-80 words. The language is clinical shorthand mixed with narrative descriptions:

- **Immediate (Level 1):** "crushing chest pain," "unresponsive," "severe bleeding," "seizure activity," "cardiac arrest," "respiratory failure," "anaphylaxis," "stroke symptoms." Notes mention critical interventions needed.
- **Emergent (Level 2):** "difficulty breathing," "severe abdominal pain," "head injury," "high fever with confusion," "vomiting blood," "diabetic emergency." Notes describe acute but not immediately life-threatening presentations.
- **Urgent (Level 3):** "moderate pain," "sprained ankle," "laceration needing stitches," "persistent cough," "urinary symptoms," "back pain." Notes describe conditions requiring timely but not immediate care.
- **Non-Urgent (Level 4):** "sore throat," "runny nose," "minor rash," "prescription refill," "mild headache," "follow-up visit," "insect bite." Notes describe minor complaints with no red flags.

Critically, approximately 8% of cases involve **discrepancy between text and vitals**. A patient may report "mild headache" (text suggests Non-Urgent) but have dangerously elevated blood pressure (vitals suggest Emergent). These cases are where the model must learn to weight vital signs appropriately and not rely solely on the chief complaint text. This mirrors real clinical practice where patients frequently minimize or are unable to articulate the severity of their condition.

## Special Considerations

- **Safety-critical application:** Under-triage of Immediate patients is the most dangerous error in all of medicine. The model must be evaluated with this asymmetry front and center.
- **Class imbalance:** Immediate patients are only 8% of presentations. Standard accuracy optimization will sacrifice recall for this critical minority class. Consider class weighting, oversampling, or threshold adjustment.
- **Vital signs provide objective severity signal:** Unlike many text classification problems, the structured features here are not just contextual — they directly measure physiological severity. Abnormal vitals (heart rate, oxygen saturation, blood pressure, temperature) override text in clinical importance. The model must learn this hierarchy.
- **Text-vital discordance cases:** Approximately 8% of cases have mild text but severe vitals (or vice versa). These are the cases where combining text and structured features matters most — and where a text-only model would be dangerous.
- **Ordinal target:** Triage levels have a natural order. Predicting Level 3 for a true Level 2 patient (one level off toward less urgent) is a safety concern; predicting Level 1 for a true Level 2 patient (one level off toward more urgent) is an acceptable over-triage. Consider whether ordinal approaches or asymmetric loss functions improve safety metrics.
- **Evaluation drift:** The test period reflects a slightly older patient population, marginally elevated heart rates, and lower oxygen saturation levels — simulating a seasonal respiratory illness surge. Models must be robust to this population shift.

## Cost/Impact Table

| True Level | Predicted Level | Clinical Impact | Severity |
|-----------|----------------|-----------------|----------|
| 1 (Immediate) | 1 (Immediate) | Correct: patient seen within minutes | Safe |
| 1 (Immediate) | 2 (Emergent) | **Under-triage:** 15-30 min delay; potential for irreversible harm | **Critical** |
| 1 (Immediate) | 3 or 4 | **Severe under-triage:** 1-4 hour delay; potential death or permanent disability | **Life-threatening** |
| 2 (Emergent) | 1 (Immediate) | Over-triage: uses critical bay unnecessarily; safe for this patient but displaces resources | Low |
| 2 (Emergent) | 3 (Urgent) | **Under-triage:** 30-60 min added delay; risk of clinical deterioration | **High** |
| 2 (Emergent) | 4 (Non-Urgent) | **Severe under-triage:** hours of delay for an acutely ill patient | **Critical** |
| 3 (Urgent) | 1 or 2 | Over-triage: occupies higher-acuity resources; safe but inefficient | Low |
| 3 (Urgent) | 4 (Non-Urgent) | Minor under-triage: additional 1-2 hour wait; generally safe but uncomfortable | Medium |
| 4 (Non-Urgent) | 1 or 2 | Over-triage: significant resource waste; patient seen faster than needed | Low |
| 4 (Non-Urgent) | 3 (Urgent) | Slight over-triage: minor resource misallocation; patient is safe | Negligible |
