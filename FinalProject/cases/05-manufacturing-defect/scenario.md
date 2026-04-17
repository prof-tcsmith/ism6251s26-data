# Scenario 05: Manufacturing Defect Detection

## Business Context

PrecisionTech Electronics is a mid-tier manufacturer of printed circuit boards (PCBs) serving the automotive, medical device, and consumer electronics industries. The company operates three production lines running 24/7 across three operator shifts, processing approximately 8,000 boards per day. Current defect rates hover around 5%, which is above the 2% target set by the company's largest automotive OEM customer. Boards that pass initial quality control but fail in the field result in warranty claims, potential recalls, and significant brand damage.

The VP of Manufacturing has partnered with the data science team to develop a predictive model that identifies boards likely to be defective before they leave the factory floor. The model will use process parameters (temperatures, speeds, durations), environmental conditions (humidity, ambient temperature), and inspection metrics collected during production. Boards flagged as high-risk will be routed to a secondary manual inspection station where a trained technician performs a detailed visual and functional test. This re-inspection process costs approximately $750 per board in labor and production throughput loss.

The cost of a missed defect is severe. When a defective board reaches a customer, the average cost including warranty replacement, field service, logistics, and contractual penalties is approximately $10,000. For boards that end up in medical devices or automotive safety systems, the liability exposure can be substantially higher, though the $10,000 figure represents the blended average across all customers. The quality assurance team has compiled a dataset of boards with known outcomes (passed final QC vs. confirmed defective through customer returns or secondary inspection catch).

PrecisionTech's CEO has communicated to the board that reducing the escaped defect rate is an existential priority: the company's largest customer has threatened to move 40% of its orders to a competitor if quality metrics do not improve within two quarters.

## Key Stakeholders

- **VP of Manufacturing:** Owns the production process; needs to balance quality improvement with throughput targets.
- **Quality Assurance Director:** Manages the inspection team; needs a manageable number of flagged boards (re-inspection capacity is limited to ~400 boards/day).
- **Customer Quality Engineers:** Interface with OEM customers on defect reports; need to demonstrate continuous improvement.
- **Finance:** Tracks cost of quality (internal failures + external failures + prevention costs); needs to justify the investment in the ML system.
- **Operations Managers (per shift):** Responsible for their shift's defect rates; interested in understanding which process parameters they can control.

## Cost Structure

| Prediction | Actual | Outcome | Cost |
|---|---|---|---|
| Good (0) | Good (0) | True Negative | $0 |
| Defective (1) | Defective (1) | True Positive | $750 (re-inspection catches defect, prevents field failure) |
| Defective (1) | Good (0) | **False Positive** | **$750** (unnecessary re-inspection of a good board) |
| Good (0) | Defective (1) | **False Negative** | **$10,000** (defective board reaches customer) |

## Special Considerations

- The FN/FP cost ratio is 300:1. This is among the most extreme asymmetries in the scenario set. Missing a defect is catastrophically more expensive than a false alarm.
- The class imbalance is moderate (~5% defect rate) but combined with the extreme cost asymmetry, threshold selection is critical.
- Temperature features exhibit important interactions: the solder temperature's effect on defects depends on ambient temperature conditions. High ambient temperature narrows the acceptable solder temperature window.
- Production speed interacts with board complexity (component count): fast production is fine for simple boards but dangerous for complex ones.
- Time since maintenance has a threshold effect rather than a linear one: defect rates spike noticeably after ~500 hours since last maintenance, with another jump around 800 hours.
- The three reflow zone temperatures are highly correlated with each other (multicollinearity), and what matters most is the delta between zones rather than absolute values.
- Operator shift effects are subtle and interact with board complexity: the night shift (shift 2) shows slightly elevated defect rates, but only on complex boards.
- Machine ID captures equipment-specific effects: certain machines have persistent calibration issues that produce more defects regardless of other settings.


---

*Note: Costs rebalanced: re-inspection triggers full machine stop + operator time + production line slowdown.*
