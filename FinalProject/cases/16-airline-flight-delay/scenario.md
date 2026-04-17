# Scenario 16: Airline Flight Delay Prediction

## Company Background

**SkyBridge Airlines** is a mid-size domestic carrier operating approximately 800 daily flights across 95 destinations. The airline operates from two primary hubs and serves a mix of business and leisure travelers. SkyBridge has a fleet of 120 aircraft (primarily Boeing 737 and Airbus A320 variants) and employs 15,000 people including 2,400 pilots and 3,800 flight attendants.

## Business Problem

In 2025, 23% of SkyBridge flights experienced delays exceeding 60 minutes. These delays cost the airline an estimated $180 million in passenger compensation, rebooking costs, crew overtime, and missed connection handling. Beyond direct costs, delays erode customer satisfaction and drive travelers to competitors — SkyBridge's Net Promoter Score has dropped 12 points over two years.

The Operations Control Center (OCC) makes real-time decisions about flight scheduling, crew assignments, and gate management. Currently, these decisions are reactive: the OCC scrambles to respond after delays occur. SkyBridge wants a model that can predict delays **3-6 hours before departure**, giving the OCC time to:

- Proactively rebook passengers on alternative flights
- Pre-position backup crews at hub airports
- Adjust gate assignments to minimize connection disruptions
- Communicate delay expectations to passengers before they arrive at the airport

## Stakeholders

- **SVP of Operations** — Responsible for on-time performance (OTP) metrics reported to the DOT. OTP is a key metric in analyst reports and affects the airline's stock price.
- **Director of Customer Experience** — Wants to transform delay response from reactive to proactive. Studies show passengers are 40% more satisfied when notified of delays before arriving at the airport.
- **Crew Scheduling Manager** — FAA regulations limit crew duty hours. A late-day delay can "time out" a crew, cascading into cancellations for the next day's flights.
- **CFO** — Wants to quantify the ROI of predictive delay management. Currently skeptical that the investment will pay off.

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Preemptive action** (Predict 1) | **Flight delayed >60 min** (Actually 1) | True Positive | **Saves ~$25,000** ($30K delay cost reduced to $5K via proactive management) |
| **Preemptive action** (Predict 1) | **Flight on time** (Actually 0) | False Positive | **-$5,000** (unnecessary rebooking prep, crew repositioning, passenger notifications for on-time flight) |
| **No preemptive action** (Predict 0) | **Flight on time** (Actually 0) | True Negative | **$0** (normal operations) |
| **No preemptive action** (Predict 0) | **Flight delayed >60 min** (Actually 1) | False Negative | **-$30,000** (reactive response: stranded passengers, compensation, missed connections, crew overtime) |

**Key asymmetry:** An unprepared-for delay ($30,000) costs **6x** unnecessary preemptive action ($5,000). However, the relatively high base rate of delays (~22%) means the total cost of false positives can be substantial.

## Target Variable

- `target = 1`: Flight is delayed by more than 60 minutes from scheduled departure
- `target = 0`: Flight departs on time or with a delay of 60 minutes or less

**Class balance:** Approximately 22% of flights are significantly delayed.

## Features

| Feature | Description |
|---------|-------------|
| `scheduled_departure_hour` | Scheduled departure time (hour, 5-23) |
| `day_of_week` | Day of the week (0 = Monday, 6 = Sunday) |
| `month` | Month of the year (1-12) |
| `origin_airport_congestion` | Current congestion level at origin airport (0-10) |
| `dest_airport_congestion` | Current congestion level at destination airport (0-10) |
| `aircraft_age_years` | Age of the assigned aircraft in years |
| `aircraft_utilization_hours_today` | Hours the aircraft has been in service today |
| `crew_hours_on_duty` | Hours the assigned crew has been on duty today |
| `weather_severity_origin` | Weather severity at origin (0 = clear, 4 = severe) |
| `weather_severity_dest` | Weather severity at destination (0 = clear, 4 = severe) |
| `num_prior_flights_today` | Number of flights this aircraft has completed today |
| `previous_flight_delay_minutes` | Delay of this aircraft's immediately preceding flight (minutes) |
| `gate_turnaround_time_planned` | Planned time for deplaning, cleaning, boarding (minutes) |
| `passenger_load_factor` | Percentage of seats sold for this flight |
| `is_holiday_period` | 1 = departure during a holiday travel period, 0 = normal period |
| `route_distance_miles` | Great-circle distance of the route (miles) |
| `is_hub_origin` | 1 = departing from a hub airport, 0 = spoke |
| `is_hub_destination` | 1 = arriving at a hub airport, 0 = spoke |
| `maintenance_flag` | 1 = aircraft has an open (deferred) maintenance item, 0 = clean |
| `connecting_pax_pct` | Percentage of passengers connecting from other flights |

## What Makes This Problem Interesting

1. **Cascading Delays:** The single strongest predictor of a flight delay is whether the aircraft's previous flight was delayed. Delays propagate through the network — a morning delay in Chicago can cause an evening delay in Miami if the same aircraft is used.

2. **Non-Linear Time Patterns:** Delays are not uniformly distributed throughout the day. They build through the afternoon as cascading effects accumulate, then partially reset overnight. The relationship between departure time and delay probability is non-linear.

3. **Weather Interactions:** Bad weather at an airport is dangerous on its own, but bad weather combined with high airport congestion is much worse than either alone — congested airports have no buffer to absorb weather-related slowdowns.

4. **Crew Duty Limits:** FAA regulations limit pilots to specific duty hours. When crew hours approach the limit (>10 hours), the risk of a "crew timeout" cancellation increases sharply — this is a threshold effect, not a gradual one.

5. **Relatively Balanced Classes:** Unlike many other scenarios, the positive class here is ~22%, making accuracy a somewhat reasonable (though still imperfect) metric. The challenge is more about capturing the complex feature interactions than handling extreme imbalance.

## Evaluation Considerations

The OCC processes 800 flights daily. If your model flags 200+ flights for preemptive action, the operations team cannot handle the workload. Consider the trade-off between catching more delays (higher recall) and operational feasibility (higher precision). A model that catches 70% of delays while only flagging 25% of all flights may be more useful than one that catches 90% of delays but flags 50% of flights.

---

*Dataset contains 20 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and test.csv (~1,000 rows).*
