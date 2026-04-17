# Scenario 18: Medical Appointment No-Show Prediction

## Company Background

**CarePoint Medical Group** is a multi-specialty outpatient clinic network with 8 locations across a mid-size metropolitan area. The group employs 50 physicians across primary care, cardiology, orthopedics, dermatology, and other specialties. CarePoint handles approximately 15,000 appointments per month and serves a diverse patient population spanning privately insured, Medicare, Medicaid, and uninsured patients.

## Business Problem

CarePoint's no-show rate is approximately **28%** — meaning more than one in four scheduled appointments result in the patient failing to appear without canceling in advance. This is a significant operational and financial problem:

- **Revenue Loss:** An empty appointment slot represents $250 in lost revenue on average (consultation fee plus ancillary services). With 15,000 monthly appointments, a 28% no-show rate means ~4,200 wasted slots, or roughly **$1.05 million per month** in unrealized revenue.
- **Access Delays:** Patients needing appointments wait 2-4 weeks because slots are "reserved" by patients who never show up. This is particularly harmful for patients with urgent needs.
- **Physician Productivity:** Doctors sitting idle during no-show slots could be seeing other patients, performing procedures, or catching up on documentation.

CarePoint wants a model to predict which patients are likely to no-show so the scheduling team can take targeted action: extra reminder calls, overbooking strategies for high-risk time slots, or offering standby patients the opportunity to fill likely-empty slots.

## Stakeholders

- **Chief Medical Officer** — Wants to improve patient access and reduce wait times. Believes better scheduling could improve health outcomes by ensuring patients are seen on time.
- **Practice Manager** — Responsible for clinic operations and physician utilization. Currently uses overbooking based on gut feel — sometimes too aggressive (patients waiting hours) and sometimes too conservative (empty slots).
- **Scheduling Coordinator** — Has capacity to make approximately 200 extra reminder calls per week across all locations. Needs to know which patients to prioritize.
- **Patient Experience Director** — Concerned that overbooking could lead to long wait times for patients who DO show up, damaging patient satisfaction.

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Extra reminder** (Predict 1) | **Would have no-showed** (Actually 1) | True Positive | **Saves up to $250** (reminder reduces no-show probability; or slot is overbooked with standby patient) |
| **Extra reminder** (Predict 1) | **Would have attended** (Actually 0) | False Positive | **-$20** (staff time for unnecessary reminder call/text) |
| **No extra action** (Predict 0) | **Attends appointment** (Actually 0) | True Negative | **$0** (normal appointment proceeds) |
| **No extra action** (Predict 0) | **No-shows** (Actually 1) | False Negative | **-$250** (lost revenue from empty slot that could have been filled) |

**Key asymmetry:** A missed no-show ($250) costs about **12.5x** an unnecessary reminder ($20). However, the high base rate (~28%) means many patients are at risk, and the intervention (a reminder call) is cheap enough to use broadly.

## Target Variable

- `target = 1`: Patient does not attend the scheduled appointment (no-show)
- `target = 0`: Patient attends the scheduled appointment

**Class balance:** Approximately 28% no-show rate.

## Features

| Feature | Description |
|---------|-------------|
| `lead_time_days` | Days between when the appointment was scheduled and the appointment date |
| `age` | Patient age in years |
| `num_previous_appointments` | Total number of prior appointments at CarePoint |
| `num_previous_no_shows` | Number of prior no-shows at CarePoint |
| `no_show_rate_historical` | Patient's historical no-show rate (no-shows / appointments) |
| `appointment_hour` | Hour of the scheduled appointment (7-18) |
| `day_of_week` | Day of the week (0 = Monday, 4 = Friday) |
| `is_new_patient` | 1 = first appointment at CarePoint, 0 = returning patient |
| `specialty` | Medical specialty (encoded 0-8) |
| `insurance_type` | Insurance category (encoded 0-4: private, Medicare, Medicaid, self-pay, other) |
| `distance_to_clinic_miles` | Distance from patient's home to the clinic location |
| `reminder_sent` | 1 = automated reminder was sent, 0 = no reminder |
| `num_reminders_sent` | Number of reminders sent (0-5) |
| `rescheduled_count` | Number of times this appointment was rescheduled |
| `weather_forecast_severity` | Weather severity for the appointment day (0 = clear, 3 = severe) |
| `has_chronic_condition` | 1 = patient has a chronic condition requiring regular care, 0 = no |
| `num_medications` | Number of active prescriptions |
| `copay_amount` | Expected copay for this visit ($) |
| `wait_time_last_visit_minutes` | How long the patient waited past appointment time at their last visit |
| `online_portal_active` | 1 = patient uses the online patient portal, 0 = does not |

## What Makes This Problem Interesting

1. **Lead Time is Key:** The further out an appointment is scheduled, the more likely the patient is to no-show. An appointment booked 6 weeks in advance has a dramatically different no-show probability than one booked 2 days ahead. This is the single most powerful predictor.

2. **Historical No-Show Behavior:** A patient's past no-show rate is highly predictive of future behavior — but this feature is partially circular (patients labeled as "no-show risks" may receive different treatment). New patients have no history, creating a cold-start problem.

3. **U-Shaped Age Effect:** Very young patients (whose parents schedule for them) and elderly patients (who may have transportation difficulties or forget) show different patterns than middle-aged adults. The relationship between age and no-show risk is not linear.

4. **Copay as Barrier:** For patients with good private insurance, a high copay might not matter. For patients on Medicaid or self-pay, a $60 copay could be the difference between showing up and not — the copay-insurance interaction is important.

5. **Reminders Help But Don't Solve:** Sending a reminder reduces no-show probability, but doesn't eliminate it. The model needs to work alongside the reminder system, not be confounded by it. Patients who received reminders but still no-showed are the hardest cases.

6. **High Base Rate:** With ~28% no-shows, this is a relatively balanced problem. The challenge is less about detecting rare events and more about distinguishing between the 28% who won't show and the 72% who will — a subtler discrimination task.

## Evaluation Considerations

Given the cheap cost of reminders ($20 per call), the optimal strategy might be to cast a wide net. If the model identifies patients with >35% no-show probability and the scheduling team sends extra reminders to all of them, what's the expected ROI? Consider also the overbooking application: if the model says a time slot has 3 patients with >50% no-show probability, the clinic might book a 4th patient for that slot. Calibrated probabilities matter more than binary classifications here.

---

*Dataset contains 20 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and holdout.csv (~1,000 rows).*
