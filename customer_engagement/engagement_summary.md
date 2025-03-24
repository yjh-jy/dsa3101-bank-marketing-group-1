# Detailed Engagement Analysis Report

This report summarizes findings from separate exploratory analyses at the campaign and customer levels, based on the use of `campaign_engagement.ipynb` and `customer_engagement.ipynb`. The goal is to identify which variables are most associated with user engagement in the bank’s marketing efforts.

---
## 1. Campaign-Level Analysis

This section uses `campaign_engagement.ipynb`, which performs aggregation at the `campaign_id` level. The key engagement variable is `engagement_rate`, which is derived from dividing `num_engaged` by `num_targeted`.

### A. Derived Metrics

| Feature | Description |
|--------|-------------|
| `quarter` | Mapping of months to the four quarters in a year |
| `engagement_rate` | Proportion of targeted users who engaged |
| `click_through_rate` | Clicks divided by impressions |
| `impressions_per_day` | Mean impressions normalized by campaign duration |
| `targets_per_day` | Number of targets per day |
| `clicks_per_day` | Number of clicks per day |

### B. Barplots (Categorical Features by Engagement Rate)

| Feature | Insight |
|--------|---------|
| **channel_used** | Channels like TikTok and Instagram are associated with significantly higher engagement rates. |
| **campaign_type** | Affliate Marketing shows much stronger performance than other types, about 10 percentage points more than Display Advertising, which comes in second at about one-third more than Email Marketing, and Search Engine Optimisation and Telemarketing bringing up the rear. |
| **campaign_language** | Variation observed across languages; French and English appear to yield better engagement in some cases. |
| **target_audience** | Engagement varies by audience; certain age segments show higher responsiveness. |
| **quarter** | Seasonal effects are visible; quarters Q3 and Q1 show better engagement outcomes than Q2 and Q4, the latter of which showing the lowest engagement. |
| **campaign_duration** | Engagement rate peaks at 30 days, but trends downwards as campaign duration increases thereafter |

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
| **click_through_rate**| Higher CTR values are very visibly linked to higher engagement tiers. |
| **clicks_per_day**    | High engagement campaigns sustain stronger daily click performance. |
| **impressions_per_day** | Campaigns with higher daily impression rates often yield better engagement. |
| **targets_per_day**   | Targeting intensity has a modest but visible impact on engagement outcomes. |
|###### **campaign_duration** | Very long campaigns trend toward lower engagement; short to medium durations perform better. |

### E. Correlation Matrix

Pairwise Pearson correlations among continuous campaign metrics are shown.

- `clicks`, `clicks_per_day`, and `click_through_rate` are strongly correlated with `engagement_rate`.
- `targets_per_day` has a weak negative correlation with `engagement_rate`.
- `impressions` and `impressions_per_day` are weakly positively associated with engagement.
- Interestingly, `targets_per_day`has a strong positive correlation with `impressions_per_day` but weka negative correlation with `impressions`.

### F. Chi-Square Tests (Categorical Features vs Engagement Bin)

| Feature           | P-Value | Interpretation |
|------------------|---------|----------------|
| **channel_used**     | < 0.001 | Strongly associated with engagement level |
| **campaign_type**    | < 0.001 | Strongly associated with engagement level |
| **campaign_duration**| < 0.001 | Strongly associated with engagement level |
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
| **days_since_web_use**   | No strong pattern. |
| **days_since_mobile_use**   | No strong pattern. |
| **debt**                 | No strong pattern. |
| **avg_web_time**         | Slightly higher in engaged group. |
| **total_logins_per_week**        | Slightly higher for engaged users. |
| **avg_total_time_per_session**      | Slightly higher for engaged users. |
| **income**               | No meaningful difference. |
| **customer_lifetime_value** | Slight trend toward higher values among engaged users. |
| **nps**                  | No strong visual trend. |
| **balance**              | Largely overlapping distributions. |

### T-Test (Continuous Variables by Engagement)

| Feature                     | P-Value | Insight |
|-----------------------------|---------|---------|
| **income**                  | 0.189  | Statistically higher among engaged users. |
| **transaction_count**       | 0.225  | Not significant. |
| **transaction_frequency**   | 0.293  | No meaningful difference. |
| **debt**                    | 0.616  | No clear separation. |
| **nps**                     | 0.744  | Minimal difference between groups. |
| **days_since_web_use**      | 0.757  | Weak pattern. |
| **total_logins_per_week**   | 0.770  | Weak pattern. |
| **customer_lifetime_value** | 0.778  | Overlaps in distribution. |
| **age**                     | 0.829  | Minimal difference between groups. |

### C. Chi-Square Tests (Categorical & Binary Variables)

| Feature              | P-Value | Interpretation |
|----------------------|--------|----------------|
| **job**              | < 0.065 | Statistically meaningful |
| **dependents**       | 0.171   | Not statistically significant. |
| **education**        | 0.200   | Not statistically significant. |
| **marital**          | 0.250   | Weak association. |
| **default**          | 0.321   | Weak but statistically meaningful. |
| **num_products_owned**| 0.410   | Weak but statistically meaningful. |
| **has_web_account**   | 0.464   | Weak signal. |
| **is_high_value_user**| 0.495   | Not statistically significant. |
| has_credit_card, has_mobile_app | 1.0 | Not statistically significant. |

### D. Proportion Table (Categorical Features by Engagement)

These show the proportion of customers who engaged (`has_engaged = 1`) within each category group.

| Feature               | Highest Engaging Group | Engagement Rate |
|------------------------|------------------------|------------------|
| **job**               | unemployed             | 0.691            |
| **dependents**        | 0                      | 0.635            |
| **education**         | primary                | 0.619            |
| **num_products_owned**| 4                      | 0.608            |
| **default**           | 1                      | 0.604            |
| **is_high_value_user** | 1                      | 0.602            |
| **marital**           | single                 | 0.599            |
| **has_web_account**   | 1                      | 0.588            |
| **has_mobile_app**    | 1                      | 0.585            |

### E. Barplots (Categorical Features by Engagement Rate)

Barplots visually depict the proportion of engaged customers across different category levels.

| Feature               | Insight |
|------------------------|---------|
| **job**               | Unemployed and students show highest engagement rates. |
| **dependents**        | Customers without dependents are more likely to engage. |
| **education**         | Primary-educated users engage more often; tertiary users show lower rates. |
| **num_products_owned**| Customers with higher number of products they already own have higher engagement. |
| **default**           | Surprisingly, customers who defaulted previously show higher engagement. |
| **is_high_value_user** | Users with higher than medians logins per week and total transaction amounts show higher engagement.
| **marital**           | Single customers are more likely to engage. |
| **has_web_account**   | Engagement is slightly higher among users.
| **has_mobile_app**    | Engagement is slightly higher among users. |

## 3. Actionable Insights for Stakeholders

### A. Campaign Optimization
- Affliate marketing is the top-performing campaign type, outperforming others in engagement by a significant margin.
- TikTok and Instagram are the most effective channels. These findings, reinforced by chi-square tests and barplots, support increased budget allocation toward affiliate campaigns run on social platforms.
- Campaigns lasting around 30 days yield the highest engagement. Longer campaigns tend to suffer diminishing returns.
- Seasonal patterns suggest Q1 and Q3 as the most effective quarters for campaign deployment.
- CTR is one of the strongest differentiators of engagement. Design creatives and call-to-actions that improve CTR.
- Daily metrics such as `clicks_per_day` and `impressions_per_day` provide more granular insights into pacing and momentum.
- Targets per day, however, suggests diminishing returns at high outreach volumes.

### B. Targeting Strategy
- **Digital Activity**:
  - More frequent web and mobile interactions, as well as higher average time per session, are moderately predictive of engagement.
  - App ownership by itself does not strongly correlate with engagement; active usage is more important than access.
  - High click and impression counts are strong indicators of potential engagement.
- **Demographics**:
  - Age, job type, and marital status show moderate to weak influence but may still support segmentation.
  - Unemployed individuals, students and singles show the highest engagement rates. These could represent underutilised high-potential segments.
  - Primary-educated users engage more than tertiary-educated ones, possibly due to differing content or financial needs. Avoid over-segmenting based on assumed affluence.
  - Customers without dependents engage more, possibly due to more flexible financial or lifestyle priorities. 
  - Counterintuitively, those with prior defaults show higher engagement. As such, these users may be seeking support or new financial solutions, and thus be more receptive to new offers.
  - Customers with more financial products (e.g., loans, investments) tend to engage more. They may already be more involved or attentive to financial updates.
  - Features overall offer limited predictive power individually but could help in profiling.
  - Note that high-value users (based on transactions and logins) do not always engage more, reinforcing the need for behaviour-based segmentation instead of purely financial metrics.
---

## 4. Suggestions for Modelling

| Task | Recommendation |
|------|----------------|
| **Feature Selection** | Include more campaign-level metrics like `clicks`, `click_through_rate`, `clicks_per_day`, `channel_used`, `campaign_type`. On the customer side, can consider including `job`, `education`, `dependents` and `num_products_owned`. |
| **Preprocessing** | One-hot encode categorical variables such as `channel_used`, `campaign_type`, `job`, `education`, `marital`. |
| **Feature Pruning** | Consider removing `nps`, `age`, and `customer_lifetime_value` if they degrade model performance. |

---

## Visual Aids

Figures used in this EDA are saved under:
- `figures/boxplots/` for continuous variable distributions
- `figures/barplots/` for engagement rates across categories
- `figures/violinplots/` for spread and density of features across engagement tiers
- `figures/histograms/` for overall distributions of numeric features

---

## Expected Outcome: Key Metrics for Tracking Customer Engagement
Based on the updated campaign-level and customer-level analyses, the following metrics are recommended for tracking customer engagement over time. These are grounded in both statistical significance and consistent visual patterns observed during exploratory analysis:

- Engagement rate: The primary metric for measuring campaign performance, defined as the proportion of engaged users over those targeted. This should be tracked consistently across time and campaign segments.

- Click-through rate: One of the strongest indicators of engagement. Campaigns with higher CTRs consistently exhibit better overall engagement outcomes.

- Clicks per day: Reflects daily interaction momentum. Higher values are associated with campaigns in the high engagement tier.

- Impressions per day: A pacing metric that correlates positively with engagement. Useful for monitoring how exposure volume influences responsiveness.

- Campaign type and channel used: Certain campaign types (e.g., affiliate marketing) and channels (e.g., TikTok, Instagram) have statistically significant associations with engagement. These categorical features can guide future campaign design and targeting strategy.

- Campaign duration: Engagement tends to peak for campaigns lasting around 30 days, with diminishing returns observed for longer durations.

These metrics provide a focused and evidence-based foundation for tracking engagement performance over time and supporting campaign decision-making.