# Detailed Engagement Analysis Report

This report summarizes findings from separate exploratory analyses at the campaign and customer levels, based on the use of `campaign_engagement.ipynb` and `customer_engagement.ipynb`. The goal is to identify which variables are most associated with user engagement in the bank’s marketing efforts.

---
# Campaign-Level Analysis

This section uses `campaign_engagement.ipynb`, which performs aggregation at the `campaign_id` level. The key engagement variable is `engagement_rate`, which is derived from dividing `num_engaged` by `num_targeted` to get the proportion of users who engaged among those targeted by a campaign.

## 1. Summary of Derived Metrics

| Feature | Description |
|--------|-------------|
| `quarter` | Calendar quarter derived from campaign month |
| `engagement_rate` | Proportion of targeted users who engaged |
| `click_through_rate` | Clicks divided by impressions |
| `impressions_per_day` | Average impressions per day based on campaign duration |
| `targets_per_day` | Number of targets per day |
| `clicks_per_day` | Number of clicks per day |

## 2. Key Insights by Plot Type

### A. Barplots (Categorical Features by Engagement Rate)

| Feature | Insight |
|--------|---------|
| **channel_used** | Channels like TikTok and Instagram are associated with significantly higher engagement rates. |
| **campaign_type** | Affliate Marketing shows much stronger performance than other types, about 10 percentage points more than Display Advertising, which comes in second at about one-third more than Email Marketing, and Search Engine Optimisation and Telemarketing bringing up the rear. |
| **campaign_language** | English and French campaigns often perform better; Mandarin and Spanish show more variable outcomes. |
| **target_audience** |  Certain age segments (e.g., 25-34) exhibit higher responsiveness. |
| **quarter** | Seasonal effects are visible; quarters Q3 and Q1 show better engagement outcomes than Q2 and Q4, the latter of which showing the lowest engagement. |
| **campaign_duration** | Engagement rate peaks at 30-day durations, but trends downwards as campaign duration increases thereafter. |

### B. Boxplots (Continuous Features by Engagement Rate)

| Feature               | Insight |
|-----------------------|---------|
| **clicks**            | High engagement campaigns have higher medians and broader upper tails. |
| **impressions**       | Higher distributions align with high engagement, though some outliers persist. |
| **click_through_rate**| Most visibly separates high vs low engagement tiers. |
| **clicks_per_day**    | Consistently stronger in high engagement tier. |
| **impressions_per_day** | High values correspond with better outcomes. |
| **targets_per_day**   | Higher bins show modest improvements. |
| **campaign_duration** | Short to medium durations dominate higher engagement bins. |

### C. Violin Plots (Continuous Features by Engagement Bin)

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

### D. Correlation Matrix

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
# 2. Customer-Level Analysis

This section uses `customer_engagement.ipynb`, which aggregates user data to customer level. The key variable is `has_engaged`, a binary variable indicating whether a customer responded to any campaign.

## 1. Summary of Derived Features

| Feature | Description |
|--------|-------------|
| `is_high_value_user` | Binary flag for users with above-median login activity and transaction volume |
| `is_recently_active` | Indicates if the user used web/mobile or transacted in past 30 days |
| `is_multichannel_user` | True if both mobile and web channels were used |
| `transaction_frequency` | Transactions normalized by tenure |
| `num_products_owned` | Count of financial products held by the user |
| `days_since_mobile_use` / `days_since_web_use` | Recency of last digital interaction |
| `avg_total_time_per_session` | Combined average time per digital session |
| `total_logins_per_week` | Weekly digital login volume |
| `total_transaction_amt` / `transaction_count` | Overall transaction activity metrics |

## 2. Key Insights by Plot Type

### A. Boxplots (Continuous Features by Engagement)

| Feature                  | Insight |
|--------------------------|---------|
| **total_logins_per_week** | Strong separation between engaged and non-engaged customers; frequent login behavior is a key indicator. |
| **transaction_count** | Higher transaction counts correlate with engagement. |
| **transaction_frequency** | Higher normalized transaction activity is seen among engaged users. |
| **avg_total_time_per_session** | Engaged customers tend to spend more time per session. |
| **days_since_mobile_use** | Recency of mobile use is lower (i.e., more recent) among engaged users. |
| **days_since_web_use** | Same trend as mobile use but slightly weaker. |
| **total_transaction_amt** | Spending volume is generally higher for engaged customers. |
| **tenure** | Slight trend toward shorter tenure among engaged customers, suggesting newer users might be more responsive. |
| **customer_lifetime_value**, **nps**, **income**, **debt**, **balance**, **age** | No strong separation between engagement groups observed. |

### B. T-Test (Continuous Variables by Engagement)

None of the numerical features showed statistically significant differences (p < 0.05). All p-values were greater than 0.24.

| Feature | P-Value |
|--------|---------|
| `transaction_frequency`, `total_transaction_amt`, `transaction_count` | > 0.24 |
| `income`, `tenure`, `debt`, `customer_lifetime_value`, `balance`, `age` | > 0.5 |
| `total_logins_per_week`, `avg_total_time_per_session`, `days_since_mobile_use`, `days_since_web_use` | > 0.63 |
| `nps` | ~0.63 |

These results confirm weak individual predictive power for engagement based solely on continuous variables.

### C. Barplots & Proportion Tables (Categorical Features)

Engagement rates were compared across different category levels:

- Users with more products owned (3 or more) showed slightly higher engagement rates.
- Users flagged as recently active or high-value had marginally better engagement, though not statistically significant.
- Job, education, marital status, default status showed weak patterns visually.

### C. Chi-Square Tests (Categorical & Binary Variables)

No categorical feature showed a significant association with engagement (p < 0.05), but some showed weak-to-moderate trends:

| Feature | P-Value |
|--------|---------|
| `dependents` | 0.13 |
| `is_recently_active` | 0.20 |
| `default`, `education`, `is_high_value_user` | 0.32 – 0.42 |

## 3. Actionable Insights for Stakeholders

### A. Campaign Optimization

- Click-through rate (CTR) remains the most effective indicator of engagement. Campaigns with higher CTRs consistently outperform others.
- Clicks per day and impressions per day are strong pacing metrics. These features help identify high-momentum campaigns that sustain engagement over time.
- Campaign type and channel show significant associations:
  - Affiliate marketing and social media platforms (e.g., TikTok, Instagram) continue to yield higher engagement.
  - These findings are visually supported by barplots and statistically reinforced by chi-square results.
- Campaign duration shows an optimal range around 30 days. Campaigns longer than this tend to experience diminishing engagement returns.
- Seasonal trends (e.g., Q1 and Q3) showed no statistically significant effect in updated data, suggesting prior assumptions of seasonal impact may be overstated.
- Targets per day appears to be a weaker or even slightly negative signal, suggesting that oversaturation may reduce effectiveness.

### B. Targeting Strategy

- Digital Activity:
  - Contrary to initial assumptions, metrics such as logins, session time, and days since digital use did not show statistically significant separation between engaged and non-engaged groups.
  - App and web account ownership alone is not predictive — actual behavioral usage matters more than access.
- Financial Behavior:
  - Transaction volume and frequency, while higher on average for engaged customers, were not statistically significant.
  - Number of products owned shows more promise: users with more bundled products tend to engage more frequently.
- Demographics:
  - Features like age, income, education, and marital status were not meaningfully associated with engagement.
  - Contrary to earlier assumptions, job type and dependents showed weak or non-significant associations.
- Behavioral Segments:
  - Flags like `is_high_value_user`, `is_recently_active`, and `is_multichannel_user` provide practical segment definitions but were not statistically strong on their own.
  - This reinforces the need for interaction-based modeling rather than relying on individual variables.

---

## 4. Suggestions for Modelling

| Task | Updated Recommendation |
|------|-------------------------|
| **Feature Selection** | Prioritize campaign-level metrics like `click_through_rate`, `clicks_per_day`, `channel_used`, and `campaign_type`. On the customer side, include `num_products_owned`, `is_recently_active`, and possibly interaction terms involving digital usage. |
| **Preprocessing** | One-hot encode categorical variables such as `channel_used`, `campaign_type`, `job`, `education`, `marital`. Consider binning continuous variables with weak trends. |
| **Feature Pruning** | Features like `nps`, `age`, `income`, and `customer_lifetime_value` did not show meaningful association and may be excluded if they reduce model clarity or performance. |

---

## Visual Aids

Figures used in this EDA are stored under:

- `figures/boxplots/`: continuous variable distributions by engagement
- `figures/barplots/`: category-level engagement patterns
- `figures/violinplots/`: campaign features split across engagement tiers
- `figures/histograms/`: baseline distributions

---

## Expected Outcome: Key Metrics for Tracking Customer Engagement

Based on current analysis, the following metrics are most useful for monitoring campaign and customer responsiveness:

- Engagement rate: The primary outcome metric for campaigns.
- Click-through rate (CTR): The most reliable campaign-level predictor of engagement.
- Clicks per day and Impressions per day: Effective pacing metrics to assess campaign momentum.
- Campaign duration: Track engagement decay beyond the 30-day mark.
- Campaign type and channel used: These remain important categorical drivers with actionable insight.
- Product bundling: Monitor `num_products_owned` as a proxy for engagement readiness on the customer side.

These metrics can support real-time performance monitoring, segmentation logic, and more accurate forecasting of future campaign outcomes.