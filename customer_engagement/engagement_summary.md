# Detailed Engagement Analysis Report

This report summarises findings from separate exploratory analyses at the campaign and customer levels, based on the use of `campaign_engagement.ipynb` and `customer_engagement.ipynb`. The goal is to identify which variables are most associated with user engagement in the bank’s marketing efforts.

---

# Customer-Level Analysis

This section uses `customer_engagement.py`, which aggregates user data to customer level. The key variable is `has_engaged`, a binary variable indicating whether a customer responded to any campaign.

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
| **total_logins_per_week** | Strong visual separation between engaged and non-engaged customers; frequent login behaviour is a key indicator. |
| **transaction_count** | Higher transaction counts correlate with engagement, indicating that active financial behaviour may signal engagement readiness. |
| **transaction_frequency** | Higher normalised transaction activity is seen among engaged users. |
| **avg_total_time_per_session** | Engaged customers tend to spend more time per session, suggesting deepr digital interaction. |
| **days_since_mobile_use** | Mobile activity is more recenet among engaged users. |
| **days_since_web_use** | Same trend as mobile use, but slightly weaker. |
| **total_transaction_amt** | Higher overall transaction amounts are observed among engaged customers. |
| **tenure** | Slight trend toward shorter tenure among engaged customers, suggesting newer users might be more responsive. |
| **customer_lifetime_value**, **nps**, **income**, **debt**, **balance**, **age** | No strong separation between engagement groups observed; these demographic and financial attributes appear less relevant for engagement prediction. |

The boxplots indicate that while behavioural variables like login frequency, transaction volume, and recency of digital use show positive trends with engagement, their individual effects are limited. These findings suggest that engagement is more likely driven by combined patterns of behaviour rather than any single metric.

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
- While `is_recently_active` and `is_high_value_user` did not show statistical significance on their own, these flags may serve as practical operational segments. They can help prioritise customers who are more primed to respond, especially when paired with real-time behavioural triggers.
- Job, education, marital status, and default status showed weak visual patterns. Although not individually predictive, they may still contribute value for tailoring messaging or creative direction.

### D. Chi-Square Tests (Categorical & Binary Variables)

No categorical feature showed a significant association with engagement (p < 0.05), but some showed weak-to-moderate trends:

| Feature | P-Value |
|--------|---------|
| `dependents` | 0.13 |
| `is_recently_active` | 0.20 |
| `default`, `education`, `is_high_value_user` | 0.32 – 0.42 |

Although the chi-square results did not confirm strong associations, these categorical features can still inform practical customer segmentation strategies. For example, recent activity flags or default status may help shape targeting rules in future marketing campaigns when used in conjunction with behavioural signals.

## 3. Multivariate Exploratory Analysis
To supplement the univariate and bivariate analyses, a multivariate exploratory analysis was conducted. This aimed to explore how customer attributes jointly relate to engagement, moving beyond individual variable effects and assessing their combined predictive value.

Specifically, the following were applied:
- Logistic Regression: to examine the relative contribution of each feature to engagement likelihood.
- Decision Tree Feature Importance: to assess which variables best split engaged vs non-engaged customers.

This multivariate exploration provides an additional layer of insight beyond individual variable associations, supporting the identification of meaningful behavioural patterns.

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

This section uses `campaign_engagement.py`, which performs aggregation at the `campaign_id` level. The key engagement variable is `engagement_rate`, which is derived from dividing `num_engaged` by `num_targeted` to get the proportion of users who engaged among those targeted by a campaign.

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
| **campaign_type** | Affliate Marketing shows much stronger performance than other types. |
| **campaign_language** | English and French campaigns often perform better; Mandarin and Spanish show more variable outcomes. |
| **target_audience** |  Certain age segments (e.g., 25-34) exhibit higher responsiveness. |
| **quarter** | Seasonal effects are visible; quarters Q3 and Q1 show better engagement outcomes than Q2 and Q4, the latter of which showing the lowest engagement. |
| **campaign_duration** | Engagement rate peaks at 30-day durations, but trends downwards as campaign duration increases thereafter. While not statistically significant, the visual trend remains meaningful and can inform business decisions. |

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

### A. Customer Behaviour Insights
1. Make use of behavioural activity signals:
   Although individual behavioural metrics such as logins, session time, and transaction frequency did not meet statistical significance thresholds, they consistently trended higher among engaged customers. This indicates that customers who are digitally active and financially engaged are more likely to respond to campaigns. These behavioural signals can be integrated into propensity models or trigger-based marketing strategies.

2. Use operational segmentation flags for targeting:
   Binary flags such as `is_recently_active`, `is_high_value_user`, and `is_multichannel_user` were not individually predictive of engagement but offer practical value for operational segmentation. These attributes can help prioritise customers who are more behaviourally primed to respond, especially when combined with real-time triggers (e.g., recent digital activity).

3. Monitor product bundling as an engagement proxy:
   Customers holding three or more financial products showed marginally higher engagement rates. This supports using product bundling as an indicator of cross-sell potential and engagement readiness.

4. Deprioritise demographic features in targeting:
   Demographic attributes such as age, income, education, marital status, and job type demonstrated minimal association with engagement. This suggests that static customer characteristics are less useful for targeting decisions compared to dynamic behavioural indicators.

5. Consider combined behavioural patterns rather than isolated metrics:
   Multivariate exploratory analysis confirmed that engagement is not driven by any single customer attribute. Instead, combined behavioural and financial signals such as digital activity, transaction volume, and product ownership provide more meaningful guidance for segmentation and targeting.

### B. Campaign Effectiveness Insights

1. Prioritise high-performing channels and campaign types:
   Campaigns delivered through affiliate marketing and social media platforms (TikTok, Instagram) consistently achieved higher engagement rates. This indicates that future marketing budgets and resources should prioritise these channels, which drive stronger customer responsiveness compared to traditional channels like telemarketing or SEO.

2. Optimise campaign duration:
   Engagement rates tended to peak for campaigns lasting around 30 days. Campaigns running beyond this duration experienced diminishing returns, likely due to customer fatigue or reduced novelty. This suggests a need to structure campaigns within this optimal duration to maximise engagement.

3. Monitor pacing metrics for real-time adjustment:
   Metrics such as click-through rate (CTR), clicks per day, and impressions per day showed strong, positive associations with engagement. These metrics can be incorporated into a real-time campaign monitoring dashboard to inform tactical decisionsm such as reallocating budget or refining creative strategy based on early performance signals.

4. Avoid audience oversaturation:
   The analysis revealed a weak negative relationship between targets per day and engagement. This suggests that over-targeting customers may reduce campaign effectiveness. Campaign teams should consider setting daily targeting caps to maintain customer interest and avoid engagement fatigue.

5. Refine audience segmentation cautiously:
   Factors such as age group (25–34) and campaign language (English, French) showed some association with engagement but were relatively weak. These demographic variables may help guide creative messaging but should not be primary criteria for targeting, which should instead focus on channel and behavioural engagement patterns.

## 2. Expected Outcome: Key Metrics for Tracking Customer Engagement
Based on the customer-level and campaign-level analyses, as well as multivariate exploration, the following metrics have emerged as the most meaningful indicators for monitoring and improving engagement:

- Engagement Rate:
  The primary outcome metric at the campaign level, representing the proportion of targeted users who engaged.

- Click-Through Rate (CTR):
  The strongest campaign-level predictor of engagement. High CTR is consistently associated with higher engagement rates and can be used as a real-time performance indicator.

- Clicks per day & impressions per day:
  Useful pacing metrics that reflect campaign momentum. Sustained performance on these metrics is associated with higher engagement and can inform budget allocation during campaign execution.

- Campaign Duration:
  Engagement trends suggest an optimal duration of around 30 days, beyond which engagement rates decline. This insight can inform campaign planning and resource allocation.

- Campaign Type & Channel:
  Affiliate marketing and social media channels (e.g., TikTok, Instagram) demonstrated significantly higher engagement rates. These attributes should inform future channel strategy and investment.

- Product Bundling:
  At the customer level, holding multiple financial products was associated with higher engagement rates. Monitoring num_products_owned can serve as a proxy for engagement readiness and cross-sell opportunities.

- Behavioural Activity Indicators:
   Digital engagement metrics such as `total_logins_per_week`, `transaction_frequency`, and recency of digital activity emerged as useful, though individually weak, predictors. When combined, they offer practical value for real-time segmentation and targeted outreach.

These metrics can support campaign planning, real-time monitoring, and segmentation logic. In future modelling efforts, they can also inform propensity scoring and help forecast campaign outcomes more accurately.















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
- `figures/multivariate/`: 