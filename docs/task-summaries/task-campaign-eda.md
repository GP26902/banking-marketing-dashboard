# Task Summary: Exploratory Data Analysis on Campaign Characteristics

**Project:** Banking Marketing Campaign Analytics Dashboard
**Deliverable:** New **📞 Campaign Characteristics (EDA)** tab in `app.py`
**Dataset:** UCI Bank Marketing dataset (`data/train.csv`), 45,211 customers

## 1. Objective

Analyze campaign-specific characteristics (contact method, campaign frequency, and previous campaign outcome) to understand campaign dynamics and which of them relate to term-deposit subscriptions.

## 2. Acceptance Criteria

| Criterion | Status | Where |
|---|---|---|
| Descriptive statistics for key campaign characteristics | ✅ Done | Contact method table, previous outcome table, numeric summary (`campaign`, `previous`, `pdays`) |
| Initial visualizations for at least 3 campaign characteristics | ✅ Done (4 charts) | Conversion by contact method, conversion by previous outcome, box plot of contact attempts, conversion by number of attempts |
| Notable patterns or outliers identified | ✅ Done | Notable Patterns & Outliers section (generated automatically from the data) |

All results respond to the existing five sidebar filters (job, age group, education, contact method, previous outcome). The figures below are for the full dataset with no filters applied.

## 3. Descriptive Statistics

**Overall:** 45,211 customers, 11.70% overall conversion rate, $1,362.27 average account balance.

### Contact Method

| Contact | Contacts | % of Contacts | Conversions | Conversion Rate |
|---|---:|---:|---:|---:|
| cellular | 29,285 | 64.77% | 4,369 | 14.92% |
| unknown | 13,020 | 28.80% | 530 | 4.07% |
| telephone | 2,906 | 6.43% | 390 | 13.42% |

### Previous Campaign Outcome

| Previous Outcome | Contacts | % of Contacts | Conversions | Conversion Rate |
|---|---:|---:|---:|---:|
| unknown | 36,959 | 81.75% | 3,386 | 9.16% |
| failure | 4,901 | 10.84% | 618 | 12.61% |
| other | 1,840 | 4.07% | 307 | 16.68% |
| success | 1,511 | 3.34% | 978 | 64.73% |

### Campaign Frequency & Prior Contact

| Variable | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| campaign | 2.76 | 3.10 | 1 | 1 | 2 | 3 | 63 |
| previous | 0.58 | 2.30 | 0 | 0 | 0 | 0 | 275 |
| pdays | 40.20 | 100.13 | -1 | -1 | -1 | -1 | 871 |

`pdays = -1` means the client was not previously contacted. Since the 75th percentile is -1, most clients had no earlier contact.

## 4. Visualizations

1. **Conversion Rate by Contact Method** (bar chart): compares conversion across cellular, telephone, and unknown contacts.
2. **Impact of Previous Campaign Outcome** (bar chart): compares conversion by the result of the earlier campaign.
3. **Campaign Frequency vs. Subscription** (box plot): distribution of contact attempts for clients who did and did not subscribe.
4. **Conversion Rate by Number of Contact Attempts** (line chart): conversion across 1, 2, 3, 4, 5-10, and 11+ attempts.

![Campaign EDA tab](screenshots/campaign-eda-tab.png)

## 5. Key Findings

- **Cellular is the main channel.** It covers 64.8% of contacts and has the highest conversion rate at 14.92%. Telephone converts at a similar 13.42%, but on only 6.43% of contacts.
- **Contacts with an unknown channel convert poorly.** The `unknown` group is 28.8% of contacts but converts at only 4.07%.
- **Past success is the strongest signal.** Clients with a previously successful campaign convert at 64.73%, compared with 9.86% for all other clients.
- **Most conversions happen early.** 92.6% of all subscriptions occurred within the first 4 contact attempts.
- **Repeated contact shows diminishing returns.** Conversion falls steadily as attempts increase. Clients contacted more than 10 times convert at 3.93%, versus 12.53% for clients contacted 1-4 times.

## 6. Outliers

- Using the IQR rule, any client contacted **more than 6 times** is an outlier. That is **3,064 clients (6.78%)**.
- The maximum is **63 attempts** for a single client. The box plot shows extreme values in both groups, with the highest attempt counts in the non-subscribers.
- `previous` (max 275) and `pdays` (max 871) also contain extreme values worth reviewing if they are used in later modeling.

## 7. Notes & Limitations

- These are descriptive patterns, not proof of cause. For example, a high conversion rate after a previous success shows association, not that the earlier campaign caused it.
- 81.75% of clients have an `unknown` previous outcome, so the previous-outcome comparison rests on small groups (1,511 successes, 1,840 "other").
- The `unknown` contact method is a large share of the data and may hide a mix of channels.

## 8. Next Steps (Suggested)

- Test whether channel and number of attempts still matter after controlling for client characteristics such as age, job, and balance.
- Investigate the `unknown` contact group to see if it can be recovered or explained.
- Consider contact-frequency caps as a hypothesis to evaluate with the marketing team.
