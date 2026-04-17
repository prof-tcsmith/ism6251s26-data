# Scenario 08: Email Spam Classification

## Business Context

MailGuard Pro is an enterprise email security provider serving over 2,000 corporate clients, filtering approximately 50 million emails per day. The company's spam detection system is the first line of defense for its clients' inboxes, and its performance directly impacts client retention and reputation. Currently, the system uses a combination of blacklists, heuristic rules, and an aging Bayesian classifier that was last retrained eighteen months ago. Spam volumes have increased by 30% in that period, and the nature of spam has evolved considerably, with sophisticated phishing campaigns now accounting for a growing share.

The Director of Engineering has tasked the data science team with building a next-generation classification model. The critical performance requirement is that the model must have an extremely low false positive rate -- legitimate emails incorrectly classified as spam. When a legitimate business email is sent to the spam folder, the consequences can be severe: missed contract deadlines, lost sales opportunities, failed regulatory communications, and erosion of trust in the email platform. The average cost of a false positive is estimated at $50, accounting for the probability and severity of various business impacts.

The cost of a false negative (spam reaching the inbox) is comparatively low in most cases: roughly $0.10 in user annoyance and lost productivity from deleting unwanted email. However, approximately 0.5% of spam emails are sophisticated phishing attacks that, if clicked, can lead to credential compromise costing an average of $100,000. The probability-weighted cost of a false negative is therefore approximately $2 when averaged across all spam types. This creates an unusual cost structure where **false positives are far more costly than false negatives** -- the reverse of most classification scenarios.

MailGuard Pro's clients have been vocal in feedback surveys: they would rather see ten spam emails in their inbox than have one legitimate email buried in spam. The product team has translated this into the mandate that precision (for the spam class) must be prioritized over recall.

## Key Stakeholders

- **Director of Engineering:** Owns the filtering pipeline; needs a model that can score emails in under 50ms.
- **Client Success Team:** Handles complaints about misclassified emails; false positives generate 10x more support tickets than false negatives.
- **Security Operations:** Monitors phishing threats; wants the model to be particularly sensitive to phishing indicators, but not at the expense of blocking legitimate emails.
- **Product Management:** Balances user experience against security; has set the strategic direction that false positives are the primary metric to minimize.
- **Sales:** Competes against rivals on filtering accuracy; a publicized incident of blocking important client emails could be devastating.

## Cost Structure

| Prediction | Actual | Outcome | Cost |
|---|---|---|---|
| Legitimate (0) | Legitimate (0) | True Negative | $0 |
| Spam (1) | Spam (1) | True Positive | $0 (spam correctly filtered) |
| Spam (1) | Legitimate (0) | **False Positive** | **$50** (legitimate email lost in spam folder) |
| Legitimate (0) | Spam (1) | **False Negative** | **$2** (spam reaches inbox; probability-weighted including phishing risk) |

## Special Considerations

- **THIS SCENARIO HAS REVERSED COST ASYMMETRY.** Unlike most other scenarios, false positives ($50) are far more costly than false negatives ($2). The FP/FN cost ratio is 25:1. Students must recognize this and adjust their threshold accordingly -- a higher classification threshold (requiring greater confidence before labeling spam) is appropriate.
- A naive approach that optimizes recall will perform terribly here. The model should be tuned for high precision on the spam class.
- Sender reputation and header authenticity are strong baseline features, but they interact with content features: a high-reputation sender with urgency words and financial language might indicate a compromised account.
- The sender_in_contacts feature is extremely protective: emails from known contacts should almost never be classified as spam. However, it is not perfectly reliable (compromised contact accounts can send spam).
- The num_images and body_length features are near-noise; they have minimal relationship with spam status in this dataset.
- The time_sent_hour feature is also mostly noise, testing whether students recognize uninformative features.
- The class balance (~30% spam) is the most balanced in the scenario set, but the cost structure still demands careful threshold management.
