# Scenario 14: Supply Chain Disruption Risk Prediction

## Company Background

**NovaParts Manufacturing** is a Tier-1 automotive parts supplier headquartered in Detroit, supplying brake systems, suspension components, and powertrain parts to three major automakers. The company manages a network of 180 suppliers across 22 countries, processing approximately 12,000 purchase orders per month. NovaParts operates on a just-in-time (JIT) manufacturing model, meaning even a small supply delay can cascade into production line shutdowns.

## Business Problem

In 2025, NovaParts experienced 47 significant supply disruptions (deliveries more than 5 days late), resulting in an estimated $8.2 million in direct costs from production delays, emergency procurement, and contractual penalties. The supply chain team currently relies on manual risk assessment and periodic supplier audits to manage risk — a process that is slow, subjective, and often reactive.

NovaParts wants a predictive model that can flag incoming purchase orders at high risk of disruption **at the time of order placement**, giving the procurement team 2-4 weeks to arrange backup suppliers or increase safety stock before the disruption materializes.

## Stakeholders

- **VP of Supply Chain** — Accountable for on-time delivery metrics (target: 98% OTD). Needs to reduce disruptions without dramatically increasing inventory carrying costs.
- **Procurement Director** — Manages supplier relationships. Wants to know which suppliers to pressure or replace, and which orders need expediting.
- **Plant Manager** — When a disruption causes a line shutdown, the plant manager faces immediate pressure from automaker customers who charge $50,000/hour in penalties.
- **CFO** — Carrying emergency safety stock ties up working capital. Wants the model to be precise enough that safety stock orders are targeted, not blanket.

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Order safety stock** (Predict 1) | **Disruption occurs** (Actually 1) | True Positive | **Saves ~$140,000** ($150K disruption cost avoided, minus $10K safety stock) |
| **Order safety stock** (Predict 1) | **No disruption** (Actually 0) | False Positive | **-$10,000** (unnecessary safety stock: procurement + storage + capital cost) |
| **No action** (Predict 0) | **No disruption** (Actually 0) | True Negative | **$0** (normal JIT operations) |
| **No action** (Predict 0) | **Disruption occurs** (Actually 1) | False Negative | **-$150,000** (production line shutdown + emergency procurement + penalties) |

**Key asymmetry:** A missed disruption ($150,000) costs **15x** unnecessary safety stock ($10,000). This strongly favors high recall, but the CFO wants to avoid tying up millions in unnecessary inventory.

## Target Variable

- `target = 1`: The supplier delivery is disrupted (arrives more than 5 days late)
- `target = 0`: The supplier delivers on time (within 5 days of promised date)

**Class balance:** Approximately 8% disruption rate.

## Features

| Feature | Description |
|---------|-------------|
| `supplier_reliability_score` | Historical on-time delivery score (0-100) |
| `lead_time_days` | Promised lead time in days for this order |
| `order_quantity` | Number of units in the purchase order |
| `supplier_country_risk` | Country risk index (0 = low, 4 = very high) |
| `transportation_mode` | Shipping method (0 = truck, 1 = rail, 2 = ocean, 3 = air) |
| `days_since_last_disruption` | Days since this supplier's last delivery disruption |
| `num_disruptions_last_year` | Number of disruptions from this supplier in the past year |
| `supplier_financial_health_score` | Financial stability score (0-100, from Dun & Bradstreet-style rating) |
| `commodity_price_volatility` | Price volatility index for the raw material in this order |
| `weather_risk_index` | Weather disruption risk for the shipping route (0-10) |
| `geopolitical_risk_score` | Geopolitical instability index for supplier region (0-10) |
| `port_congestion_index` | Port/logistics hub congestion level (0-10) |
| `num_alternative_suppliers` | Number of qualified alternative suppliers for this part |
| `contract_type` | Type of contract (0 = spot, 1 = short-term, 2 = long-term) |
| `order_complexity_score` | Complexity/customization level of the order (0-10) |
| `seasonal_demand_index` | Seasonal demand factor (0-1) |
| `supplier_capacity_utilization` | Supplier's current capacity utilization (%) |
| `distance_km` | Shipping distance in kilometers |
| `customs_complexity_score` | Customs/regulatory complexity for this shipment (0-10) |

## What Makes This Problem Interesting

1. **Risk Amplification:** Lead time acts as a risk amplifier — all other risk factors become more dangerous as lead time increases, because there is less time to react.

2. **Capacity Threshold:** Suppliers operating above ~90% capacity utilization become dramatically more likely to miss delivery targets, as they have no buffer for unexpected issues.

3. **Geopolitical Interactions:** Country risk and geopolitical risk interact — a supplier in a high-country-risk location during a period of elevated geopolitical tension is at much greater risk than either factor alone would suggest.

4. **Transportation Vulnerability:** Weather risk matters much more for ocean and air shipments than for truck or rail — a tropical storm can delay an ocean shipment by weeks but barely affects ground transport.

5. **Rare but Costly:** With only ~8% disruption rate, a naive model that predicts "no disruption" for everything would be 92% accurate but completely useless. The value of the model is entirely in catching that 8%.

## Evaluation Considerations

The procurement team can realistically act on 15-25 high-risk orders per month (ordering safety stock, contacting backup suppliers). If your model flags significantly more than that, the team will start ignoring alerts. Consider how precision at realistic operating thresholds compares across your models — it's not just about overall AUC.

---

*Dataset contains 19 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and test.csv (~1,000 rows).*
