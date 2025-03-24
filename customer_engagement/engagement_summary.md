# Detailed Engagement Analysis Report

This report summarizes findings from separate exploratory analyses at the campaign and customer levels, based on the use of `campaign_engagement.ipynb` and `customer_engagement.ipynb`. The goal is to identify which variables are most associated with user engagement in the bank’s marketing efforts.

---
## 1. Campaign-Level Analysis

This section uses `campaign_engagement.ipynb`, which performs aggregation at the `campaign_id` level. The key engagement variable is `engagement_rate`, which is derived from dividing `num_engaged` by `num_targeted`.

### A. Derived Metrics

| Feature | Description |
|--------|-------------|
| `engagement_rate` | Proportion of targeted users who engaged |
| `click_through_rate` | Clicks divided by impressions |
| `impressions_per_day` | Mean impressions normalized by campaign duration |
| `targets_per_day` | Number of targets per day |
| `clicks_per_day` | Number of clicks per day |

### B. Barplots (Categorical Features by Engagement Rate)

| Feature | Insight |
|--------|---------|
| **channel_used** | Channels like Google Ads and Instagram are associated with higher engagement rates. |
| **campaign_type** | Display Advertising shows stronger performance than other types. |
| **campaign_language** | Slight variation observed across languages; French and English appear to yield better engagement in some cases. |
| **target_audience** | Engagement varies by audience; certain age segments show higher responsiveness. |
| **quarter** | Seasonal effects are visible; some quarters show better engagement outcomes. |

### C. Boxplots (Continuous Features by Engagement Rate)

| Feature | Insight |
|--------|---------|
| **clicks** | Higher click averages are associated with higher engagement rates. |
| **impressions** | Campaigns with more impressions tend to perform better, though effect may be nonlinear. |
| **campaign_duration** | Medium-length campaigns show higher engagement; very long campaigns drop off. |
| **click_through_rate** | Strongly differentiates campaigns; higher CTR correlates with high engagement. |
| **clicks_per_day** | Daily click volume is an effective signal of engagement success. |
| **impressions_per_day** | Effective for evaluating campaign pacing; higher values generally support engagement. |
| **targets_per_day** | Moderate signal; reflects campaign intensity. |

### D. Violin Plots (Continuous Features by Engagement Bin)

The violin plots visualize how the distribution of key campaign metrics varies across low, medium, and high engagement tiers.

| Feature               | Insight |
|-----------------------|---------|
| **clicks**            | Distributions for high engagement campaigns show higher median and upper range of click counts. |
| **impressions**       | Higher impression volumes are associated with higher engagement, with some spread across tiers. |
| **click_through_rate**| Higher CTR values are clearly linked to higher engagement tiers. |
| **clicks_per_day**    | High engagement campaigns sustain stronger daily click performance. |
| **impressions_per_day** | Campaigns with higher daily impression rates often yield better engagement. |
| **targets_per_day**   | Targeting intensity has a modest but visible impact on engagement outcomes. |
| **campaign_duration** | Very long campaigns trend toward lower engagement; short to medium durations perform better. |

### E. Correlation Matrix

Pairwise Pearson correlations among continuous campaign metrics are shown.

- `clicks`, `clicks_per_day`, and `click_through_rate` are strongly correlated with `engagement_rate`.
- `campaign_duration` and `target_per_day` has a weak negative correlation with most metrics, including `engagement_rate`.
- `impressions` and `impressions_per_day` are weakly positively associated with engagement.

### F. Chi-Square Tests (Categorical Features vs Engagement Bin)

| Feature           | P-Value | Interpretation |
|------------------|---------|----------------|
| **channel_used**     | < 0.001 | Strongly associated with engagement level |
| **campaign_type**    | < 0.001 | Strongly associated with engagement level |
| campaign_language | 0.20    | No significant association |
| target_audience   | 0.29    | No significant association |
| quarter           | 0.62    | No significant association |

---
## 2. Customer-Level Analysis

This section uses `customer_engagement.ipynb`, which aggregates user data to customer level. The key variable is `has_engaged` (1 if the customer engaged in any campaign).

### A. Boxplots (Continuous Variables by Engagement)

| Feature                  | Insight |
|--------------------------|---------|
| **age**                  | No clear separation between groups. Age has limited predictive value. |
| **tenure**               | Slightly lower median for engaged users, but not strongly differentiated. |
| **mobile_logins_wk**     | Modestly higher for engaged users; digital activity may be informative. |
| **days_since_web_use**   | Engaged users tended to use web more recently. |
| **debt**                 | No strong pattern. |
| **avg_web_time**         | Slightly higher in engaged group. |
| **web_logins_wk**        | Slightly higher for engaged users. |
| **avg_mobile_time**      | Minimal difference between groups. |
| **income**               | No meaningful difference. |
| **days_since_mobile_use**| Weak pattern, but engaged users may use mobile more frequently. |
| **customer_lifetime_value** | Slight trend toward higher values among engaged users. |
| **nps**                  | No strong visual trend. |
| **balance**              | Largely overlapping distributions. |

### T-Test (Continuous Variables by Engagement)

| Feature               | P-Value | Insight |
|------------------------|--------|---------|
| **income**             | 0.001  | Statistically higher among engaged users. |
| **loan_id**            | 0.216  | Not significant. |
| **loan_amount**        | 0.275  | No clear separation. |
| **balance**            | 0.389  | No meaningful difference. |
| **total_spent**        | 0.396  | Slightly lower for engaged users, but not significant. |
| **age**                | 0.401  | No clear difference. |
| **nps**                | 0.414  | Largely overlapping distributions. |
| **avg_mobile_time**    | 0.479  | Minimal difference between groups. |
| **debt**               | 0.548  | Weak pattern. |
| **txn_count**          | 0.563  | Overlaps in distribution. |

### C. Chi-Square Tests (Categorical & Binary Variables)

| Feature              | P-Value | Interpretation |
|----------------------|--------|----------------|
| **job**              | < 0.001 | Strong association with engagement. |
| **dependents**       | 0.002   | Moderate association. |
| **education**        | 0.004   | Significant association. |
| **default**          | 0.014   | Weak but statistically meaningful. |
| **has_fixed_deposit**| 0.016   | Weak but statistically meaningful. |
| **marital**          | 0.033   | Weak association. |
| **has_insurance**    | 0.034   | Weak signal. |
| **has_personal_loan**| 0.042   | Weak signal. |
| has_credit_card, has_mobile_app | > 0.1 | Not statistically significant. |

### D. Proportion Table (Categorical Features by Engagement)

These show the proportion of customers who engaged (`has_engaged = 1`) within each category group.

| Feature               | Highest Engaging Group | Engagement Rate |
|------------------------|------------------------|------------------|
| **job**               | unemployed             | 0.688            |
| **loan_purpose**      | medical                | 0.678            |
| **dependents**        | 0                      | 0.633            |
| **default**           | 1                      | 0.618            |
| **education**         | primary                | 0.618            |
| **has_fixed_deposit** | 1                      | 0.614            |
| **has_personal_loan** | 1                      | 0.603            |
| **marital**           | single                 | 0.603            |
| **has_mobile_app**    | 0                      | 0.599            |
| **has_investment_product** | 1                | 0.598            |

### E. Barplots (Categorical Features by Engagement Rate)

Barplots visually depict the proportion of engaged customers across different category levels.

| Feature               | Insight |
|------------------------|---------|
| **job**               | Unemployed and students show highest engagement rates. |
| **loan_purpose**      | Medical and personal-related loans correspond with higher engagement. |
| **dependents**        | Customers without dependents are more likely to engage. |
| **default**           | Surprisingly, customers who defaulted previously show higher engagement. |
| **education**         | Primary-educated users engage more often; tertiary users show lower rates. |
| **has_fixed_deposit** | Customers with fixed deposits have higher engagement. |
| **has_personal_loan** | Users with personal loans are more engaged. |
| **marital**           | Single customers are more likely to engage. |
| **has_mobile_app**    | Engagement is slightly higher among non-users, possibly due to targeting. |
| **has_investment_product** | Product owners tend to engage more. |

## 3. Actionable Insights for Stakeholders

### A. Campaign Optimization
- Platforms like Google Ads or Instagram drive significantly more engagement. Consider allocating more budget and attention to these high-performing channels over lower-performing channels like email or telemarketing.
- Display advertising outperform others in driving engagement, as supported by both barplot and chi-square analyses.
- Short to medium-length campaigns perform better. Very long campaigns trend toward lower engagement, as shown in both boxplots and violin plots.
- CTR is one of the strongest differentiators of engagement. Design creatives and call-to-actions that improve CTR.
- `targets_per_day` shows only modest positive association, and excessive daily reach may not yield proportional returns.

### B. Targeting Strategy
- **Digital Activity**:
  - Engaged customers tend to have more recent web use, more mobile/web logins, and slightly higher `avg_web_time`.
  - Having the app, however, does not strongly correlate with engagement; usage patterns are more important than access.
  - High click and impression counts are strong indicators of potential engagement.
- **Demographics**:
  - Age, job type, and marital status show moderate to weak influence but may still support segmentation.
  - Unemployed individuals, students and singles show the highest engagement rates. Tailor messaging and offers for these groups.
  - Customers with primary education levels engage more frequently than those with tertiary education. Avoid over-segmenting based on assumed affluence.
  - Customers without dependents engage more, possibly due to more flexible financial or lifestyle priorities.
  - Counterintuitively, those with prior defaults show higher engagement. As such, these users may be more receptive to new offers.
  - Features like `has_home_loan`, `has_credit_card`, and `has_insurance` offer limited predictive power individually but could help in profiling.
  - Ownership of fixed deposits, personal loans, and investment products correlate positively with engagement. These customers may be more attentive to financial communication and offers.
---

## 4. Suggestions for Modeling

| Task | Recommendation |
|------|----------------|
| **Feature Selection** | Include campaign-level metrics like `clicks`, `click_through_rate`, `clicks_per_day`, `channel_used`, `campaign_type`. On the customer side, include `job`, `education`, and digital activity indicators (`days_since_web_use`, `avg_web_time`). |
| **Preprocessing** | One-hot encode categorical variables such as `channel_used`, `campaign_type`, `job`, `education`, `marital`. |
| **Remove Low-impact Features** | Consider removing `has_insurance`, `has_home_loan`, and `has_credit_card` if they degrade model performance. |

---

## Visual Aids

Figures used in this analysis are saved under:
- `figures/boxplots/` for continuous variable distributions
- `figures/barplots/` for engagement rates across categories