# Scenario 12: Power Plant Equipment Failure Prediction

## Company Background

**GridPoint Energy** is a regional power utility serving 1.8 million customers across three states. The company operates a fleet of natural gas and combined-cycle power plants with a combined generating capacity of 8,500 MW. Their equipment includes turbines, generators, transformers, and auxiliary systems, many of which are aging and require careful maintenance scheduling.

## Business Problem

GridPoint's operations team currently relies on time-based preventive maintenance schedules (e.g., inspect every 6 months regardless of equipment condition). This approach is costly and often results in either unnecessary maintenance shutdowns or, worse, unexpected equipment failures between scheduled inspections.

An unplanned equipment failure can cause a cascading outage affecting thousands of customers, trigger regulatory investigations, and cost hundreds of thousands of dollars in emergency repairs and lost generation revenue. GridPoint wants to move from time-based to **condition-based predictive maintenance** — using sensor data and equipment history to predict failures before they happen.

The goal is to identify equipment likely to fail within the next **30 days**, allowing planned shutdowns during low-demand periods rather than emergency outages during peak usage.

## Stakeholders

- **VP of Plant Operations** — Responsible for fleet reliability metrics (target: 99.5% availability). Needs to balance maintenance costs against outage risk.
- **Maintenance Planning Manager** — Schedules maintenance crews and procures parts. Needs 2-4 weeks of lead time to plan a preventive shutdown.
- **Chief Risk Officer** — Concerned about regulatory exposure. State regulators levy fines for unplanned outages exceeding 4 hours.
- **CFO** — Maintenance budget is $45M/year. Wants evidence that predictive maintenance will reduce total cost of ownership.

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Schedule maintenance** (Predict 1) | **Would have failed** (Actually 1) | True Positive | **Saves ~$195,000** ($200K failure cost avoided, minus $5K planned maintenance) |
| **Schedule maintenance** (Predict 1) | **Would NOT have failed** (Actually 0) | False Positive | **-$5,000** (unnecessary preventive maintenance shutdown) |
| **No action** (Predict 0) | **Does NOT fail** (Actually 0) | True Negative | **$0** (normal operations continue) |
| **No action** (Predict 0) | **Fails unexpectedly** (Actually 1) | False Negative | **-$200,000** (emergency repair + lost revenue + regulatory fine) |

**Key asymmetry:** A missed failure ($200,000) costs **40x** an unnecessary maintenance event ($5,000). This extreme asymmetry means the model should strongly favor recall over precision — missing a real failure is catastrophic.

## Target Variable

- `target = 1`: Equipment experiences a failure requiring unplanned repair within 30 days
- `target = 0`: Equipment operates normally for the next 30 days

**Class balance:** Approximately 6% failure rate (most equipment is healthy at any given time).

## Features

| Feature | Description |
|---------|-------------|
| `equipment_age_years` | Age of the equipment in years |
| `operating_hours_total` | Cumulative operating hours since installation |
| `hours_since_last_maintenance` | Hours of operation since last maintenance event |
| `vibration_level_mm_s` | Current vibration measurement (mm/s) from sensors |
| `temperature_bearing_celsius` | Bearing temperature reading (Celsius) |
| `oil_pressure_psi` | Lubricating oil pressure (PSI) |
| `coolant_flow_rate` | Coolant flow rate (liters/minute) |
| `power_output_mw` | Current power output (megawatts) |
| `load_factor_pct` | Current load as percentage of rated capacity |
| `ambient_temperature` | Ambient temperature at plant location (Celsius) |
| `num_previous_failures` | Count of historical failures for this equipment |
| `manufacturer` | Equipment manufacturer (encoded 0-4) |
| `equipment_type` | Type of equipment (encoded 0-3) |
| `last_maintenance_type` | Type of last maintenance performed (encoded 0-2) |
| `humidity_pct` | Ambient humidity percentage |
| `startup_count_last_month` | Number of start/stop cycles in the last month |
| `operating_mode` | Current operating mode (encoded 0-2) |
| `alarm_count_last_week` | Number of minor alarms triggered in the past week |
| `efficiency_rating` | Current thermal efficiency rating (%) |
| `thermal_image_anomaly_score` | Anomaly score from thermal imaging inspections |

## What Makes This Problem Interesting

1. **Sensor Interactions:** Individual sensor readings may look normal, but combinations can signal trouble. For example, high vibration combined with elevated bearing temperature is far more alarming than either alone.

2. **Threshold Effects:** Some features have critical thresholds — equipment that hasn't been maintained in over 2,000 operating hours enters a danger zone, even if other indicators look fine.

3. **Equipment Heterogeneity:** Different manufacturers' equipment may age differently. A 15-year-old unit from one manufacturer might be more reliable than a 10-year-old unit from another.

4. **Extreme Cost Asymmetry:** The 40:1 FN-to-FP cost ratio should dramatically influence your threshold selection. A model with 95% precision but only 50% recall would miss half the failures — costing GridPoint millions.

5. **Rare Events:** With only ~6% failure rate, the model must handle significant class imbalance without simply predicting "no failure" for everything.

## Evaluation Considerations

Given the extreme cost asymmetry, recall on the positive class is critical — but not at the expense of flagging so many false alarms that the maintenance team ignores the model. Consider whether a cost-sensitive metric (expected total cost) is more appropriate than standard classification metrics. The maintenance planning team has capacity for approximately 15-20 preventive shutdowns per month — flagging more than that will overwhelm their scheduling capacity.

---

*Dataset contains 20 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and holdout.csv (~1,000 rows).*
