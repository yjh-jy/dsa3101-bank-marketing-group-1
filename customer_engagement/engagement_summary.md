# Detailed Engagement Analysis Report

This report summarises findings from separate exploratory analyses at the campaign and customer levels, based on the use of `campaign_engagement.ipynb` and `customer_engagement.ipynb`. The goal is to identify which variables are most associated with user engagement in the bank’s marketing efforts.

---

# Customer-Level Analysis

This section uses `customer_engagement.ipynb`, which aggregates user data to customer level. The key variable is `has_engaged`, a binary variable indicating whether a customer responded to any campaign.

## 1. Summary of Derived Features

| Feature | Description |
|--------|-------------|
| `is_high_value_user` | Binary flag for users with above-median login activity and transaction volume |
| `is_recently_active` | Indicates if the user used web/mobile or transacted in past 30 days |
| `is_multichannel_user` | True if both mobile and web channels were used |
| `transaction_frequency` | Transactions normalised by tenure |
| `num_products_owned` | Count of financial products held by the user |
| `days_since_mobile_use` / `days_since_web_use` | Recency of last digital interaction |
| `avg_total_time_per_session` | Combined average time per digital session |
| `total_logins_per_week` | Weekly digital login volume |
| `total_transaction_amt` / `transaction_count` | Overall transaction activity metrics |

## 2. Key Insights by Plot Type

### A. Boxplots (Continuous Features by Engagement)

| Feature                  | Insight |
|--------------------------|---------|
| **total_logins_per_week** | Strong separation between engaged and non-engaged customers; frequent login behaviour is a key indicator. |
| **transaction_count** | Higher transaction counts correlate with engagement. |
| **transaction_frequency** | Higher normalised transaction activity is seen among engaged users. |
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

These results suggest that individual continuous variables do not strongly predict engagement on their own. However, several behavioural metrics such as `total_logins_per_week`, `avg_total_time_per_session`, and `transaction_frequency` may still carry practical relevance when considered together. Their combined patterns can signal digital engagement readiness, which can be operationalised for segmentation or campaign timing.

### C. Barplots & Proportion Tables (Categorical Features)

Engagement rates were compared across different category levels:

- Users with more products owned (3 or more) showed slightly higher engagement rates. This suggests that product bundling may be a useful proxy for engagement readiness.
- While is_recently_active and is_high_value_user did not show statistical significance on their own, these flags may serve as practical operational segments. They can help prioritise customers who are more primed to respond, especially when paired with real-time behavioural triggers.
- Job, education, marital status, and default status showed weak visual patterns. Although not individually predictive, they may still contribute value for tailoring messaging or creative direction.

### D. Chi-Square Tests (Categorical & Binary Variables)

No categorical feature showed a significant association with engagement (p < 0.05), but some showed weak-to-moderate trends:

| Feature | P-Value |
|--------|---------|
| `dependents` | 0.13 |
| `is_recently_active` | 0.20 |
| `default`, `education`, `is_high_value_user` | 0.32 – 0.42 |


## 3. Multivariate Exploratory Analysis
To supplement the univariate and bivariate analyses, a multivariate exploratory analysis was conducted. This aimed to explore how customer attributes jointly relate to engagement, moving beyond individual variable effects and assessing their combined predictive value.

### A. Logistic Regression Results
A logistic regression model was fitted using numeric and boolean customer-level features (excluding the target variable). This model aimed not to provide a reliable prediction of engagement, but to provide an initial indication of which attributes, when considered together, are associated with higher engagement.

The model produced the following classification report:
Logistic Regression Classification Report:
```
              precision    recall  f1-score   support

           0       0.00      0.00      0.00       498
           1       0.59      1.00      0.74       708

    accuracy                           0.59      1206
   macro avg       0.29      0.50      0.37      1206
weighted avg       0.34      0.59      0.43      1206
```

The model demonstrated high recall (1.00) but low precision (0.59), indicating that it successfully identified most engaged customers but also generated a large number of false positives. This is expected in an imbalanced dataset and reflects the exploratory, untuned nature of the analysis.

**Top logistic regression coefficients:**

| Feature                 | Coefficient |
|------------------------|------------:|
| `dependents`           |     -0.0246 |
| `total_logins_per_week`|      0.0193 |
| `nps`                  |     -0.0149 |
| `tenure`               |      0.0057 |
| `is_high_value_user`   |      0.0054 |

These coefficients suggest that, when controlling for other attributes:

- A higher number of dependents slightly reduces the likelihood of engagement.
- Increased digital logins and high-value user status are positively associated with engagement.
- Longer tenure and higher NPS scores have marginal effects.

While the model's predictive accuracy is limited, these results reinforce earlier findings that digital behaviour signals uch as login frequency and customer value are positively associated with engagement. However, the individual effect sizes are small, suggesting that these variables may need to be used in combination rather than isolation to inform targeting strategies.

### B. Decision Tree Feature Importance

A decision tree classifier (max depth = 4) was also fitted to assess non-linear relationships and provide an interpretable ranking of feature importance.

The top five features identified were:

| Feature                | Importance |
|-----------------------:|----------:|
| `total_transaction_amt`|     0.228 |
| `debt`                 |     0.200 |
| `income`               |     0.138 |
| `days_since_mobile_use`|     0.137 |
| `days_since_web_use`   |     0.129 |

The decision tree analysis highlighted that transactional attributes (`total_transaction_amt`, `debt`, `income`) and recency of digital activity (`days_since_mobile_use`, `days_since_web_use`) were the strongest drivers of engagement in a multivariate context. This aligns with earlier EDA findings that behavioural and financial activity, when considered jointly, shape engagement patterns.

### C. Business Insights and Limitations

**Business insights:**
These multivariate exploratory models support the overall EDA conclusion that no single attribute strongly drives engagement, but combined behavioural and financial signals can provide meaningful guidance for:

- Operational segmentation strategies (e.g., targeting recently active, high-value users with above-average transaction activity).
- Trigger-based engagement campaigns based on behavioural readiness.

**Limitations:**
- The models were not tuned for predictive performance and are intended solely for exploratory purposes.
- Class imbalance limited model accuracy, particularly for the non-engaged group.
- Demographic features remained weak contributors in both models, suggesting limited value for direct targeting.



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

Note: All missing values in the click data-related columns correspond with Telemarketing campaigns, which is expected as these campaigns do not have digital click events. This missingness is structural rather than data quality-related. To enable calculation of campaign-level metrics, missing clicks values were imputed as 0 for Telemarketing campaigns.

## 2. Key Insights by Plot Type

### A. Barplots (Categorical Features by Engagement Rate)

| Feature | Insight |
|--------|---------|
| **channel_used** | Channels like TikTok and Instagram are associated with significantly higher engagement rates. |
| **campaign_type** | Affliate Marketing shows much stronger performance than other types, about 10 percentage points more than Display Advertising, which comes in second at about one-third more than Email Marketing, and Search Engine Optimisation and Telemarketing bringing up the rear. |
| **campaign_language** | English and French campaigns often perform better; Mandarin and Spanish show more variable outcomes. |
| **target_audience** |  Certain age segments (e.g., 25-34) exhibit higher responsiveness. |
| **quarter** | Seasonal effects are visible; quarters Q3 and Q1 show better engagement outcomes than Q2 and Q4, the latter of which showing the lowest engagement. |
| **campaign_duration** | Engagement rate peaks at 30-day durations, but trends downwards as campaign duration increases thereafter. While the chi-square test did not show a statistically significant association (p = 0.0826), the visual trend remains meaningful and can inform business decisions. |

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

The violin plots visualise how the distribution of key campaign metrics varies across low, medium, and high engagement tiers.

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
# Overall Analysis

## 1. Actionable Insights for Stakeholders

### A. Campaign Optimization

- Click-through rate (CTR) remains the most effective indicator of engagement. Campaigns with higher CTRs consistently outperform others.
- Clicks per day and impressions per day are strong pacing metrics. These features help identify high-momentum campaigns that sustain engagement over time.
- Campaign type and channel show significant associations:
  - Affiliate marketing and social media platforms (e.g., TikTok, Instagram) continue to yield higher engagement.
  - These findings are visually supported by barplots and statistically reinforced by chi-square results.
- Campaign duration appears to peak around 30 days based on visual trends. This suggests a performance ceiling for longer campaigns, possibly due to diminishing novelty or customer fatigue. While statistical significance was not reached (p = 0.0826), the pattern remains operationally actionable and can serve as a benchmark when planning future campaign length.
- The variable `targets_per_day` showed a weak negative trend with engagement. This may signal oversaturation effects, where increased targeting reduces effectiveness. Campaign pacing strategies may benefit from throttling target volume per day to maintain interest and avoid fatigue.
- Seasonal trends (e.g., Q1 and Q3) showed no statistically significant effect in updated data, suggesting prior assumptions of seasonal impact may be overstated.

### B. Targeting Strategy

- Digital Activity:
  - While metrics such as logins, session time, and days since digital use did not meet strict statistical significance thresholds, they may still be high-signal indicators when used in combination. These behaviours can support propensity models and inform trigger-based outreach (e.g., push notifications after recent login).
  - Multichannel usage, though weak as a standalone signal, can be meaningful when integrated with behavioural data, to help distinguish users who are more digitally engaged and thus more likely to respond.

- Financial Behaviour:
  - Transaction volume and frequency, while higher on average for engaged customers, were not statistically significant.
  - Number of products owned shows more promise: users with more bundled products tend to engage more frequently.
- Demographics:
  - Features like age, income, education, and marital status were not strongly associated with engagement. This finding highlights that static customer attributes are less actionable than dynamic behavioural signals, and targeting strategies should prioritise what customers do, rather than who they are.
  - Contrary to earlier assumptions, job type and dependents showed weak or non-significant associations.
- Behavioural Segments:
  - Flags like `is_high_value_user`, `is_recently_active`, and `is_multichannel_user` provide practical segment definitions but were not statistically strong on their own.
  - This reinforces the need for interaction-based modeling rather than relying on individual variables.

---

## 2. Suggestions for Modelling

| Task | Updated Recommendation |
|------|-------------------------|
| **Feature Selection** | Prioritise campaign-level metrics like `click_through_rate`, `clicks_per_day`, `channel_used`, and `campaign_type`. On the customer side, include `num_products_owned`, `is_recently_active`, and possibly interaction terms involving digital usage. |
| **Preprocessing** | One-hot encode categorical variables such as `channel_used`, `campaign_type`, `job`, `education`, `marital`. Consider binning continuous variables with weak trends. |
| **Feature Pruning** | Features like `nps`, `age`, `income`, and `customer_lifetime_value` did not show meaningful association and may be excluded if they reduce model clarity or performance. |

## 3. Expected Outcome: Key Metrics for Tracking Customer Engagement

Based on current analysis, the following metrics are most useful for monitoring campaign and customer responsiveness:

- Engagement rate: The primary outcome metric for campaigns.
- Click-through rate (CTR): The most reliable campaign-level predictor of engagement.
- Clicks per day and Impressions per day: Effective pacing metrics to assess campaign momentum.
- Campaign duration: Track engagement decay beyond the 30-day mark.
- Campaign type and channel used: These remain important categorical drivers with actionable insight.
- Product bundling: Monitor `num_products_owned` as a proxy for engagement readiness on the customer side.

These metrics can support real-time performance monitoring, segmentation logic, and more accurate forecasting of future campaign outcomes.

---
# Appendix

## Visual Aids

Figures used in this EDA are stored under:

- `figures/boxplots/`: continuous variable distributions by engagement
- `figures/barplots/`: category-level engagement patterns
- `figures/violinplots/`: campaign features split across engagement tiers
- `figures/histograms/`: baseline distributions