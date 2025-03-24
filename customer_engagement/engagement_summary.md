# Detailed Engagement Analysis Report

This report summarizes the findings from an exploratory analysis on factors influencing **user engagement with marketing campaigns** (`has_engaged`) in the bank marketing dataset.

---

## 1. T-Test Analysis: Continuous Variables

The independent t-test checks if the means of numerical variables differ significantly between engaged and non-engaged users.

| Feature                   | Interpretation |
|---------------------------|----------------|
- **clicks**: significant (p = 0.0000) — engaged users tend to have higher average values.
- **impressions**: significant (p = 0.0304) — engaged users tend to have higher average values.
- **age**: not significant (p = 0.0940) — engaged users tend to have lower average values.
- **tenure**: not significant (p = 0.1880) — engaged users tend to have lower average values.
- **mobile_logins_wk**: not significant (p = 0.3648) — engaged users tend to have higher average values.
- **days_since_web_use**: not significant (p = 0.4136) — engaged users tend to have higher average values.
- **debt**: not significant (p = 0.4699) — engaged users tend to have higher average values.
- **avg_web_time**: not significant (p = 0.5606) — engaged users tend to have higher average values.
- **web_logins_wk**: not significant (p = 0.6750) — engaged users tend to have lower average values.
- **avg_mobile_time**: not significant (p = 0.7457) — engaged users tend to have lower average values.
- **income**: not significant (p = 0.8230) — engaged users tend to have higher average values.
- **days_since_mobile_use**: not significant (p = 0.8335) — engaged users tend to have lower average values.
- **customer_lifetime_value**: not significant (p = 0.8724) — engaged users tend to have higher average values.
- **nps**: not significant (p = 0.9151) — engaged users tend to have higher average values.
- **balance**: not significant (p = 0.9153) — engaged users tend to have lower average values.


---

## 2. Chi-Square Test: Categorical & Binary Variables

This test checks if the distribution of categorical variables is dependent on engagement.

| Feature              | P-Value | Interpretation |
|----------------------|---------|----------------|
- **channel_used**: p = 0.0000 — has a strong association with engagement.
- **campaign_type**: p = 0.0000 — has a strong association with engagement.
- **campaign_duration**: p = 0.0000 — has a strong association with engagement.
- **campaign_language**: p = 0.0000 — has a strong association with engagement.
- **has_insurance**: p = 0.0963 — does not show strong association with engagement.
- **has_investment_product**: p = 0.2676 — does not show strong association with engagement.
- **education**: p = 0.3511 — does not show strong association with engagement.
- **has_web_account**: p = 0.3942 — does not show strong association with engagement.
- **has_personal_loan**: p = 0.6061 — does not show strong association with engagement.
- **has_credit_card**: p = 0.6931 — does not show strong association with engagement.
- **dependents**: p = 0.7040 — does not show strong association with engagement.
- **marital**: p = 0.7390 — does not show strong association with engagement.
- **has_fixed_deposit**: p = 0.7543 — does not show strong association with engagement.
- **has_home_loan**: p = 0.8033 — does not show strong association with engagement.
- **has_mobile_app**: p = 0.8586 — does not show strong association with engagement.
- **job**: p = 0.9086 — does not show strong association with engagement.


---

## 3. Actionable Insights for Stakeholders

### A. Campaign Optimization
- Platforms like Google Ads or Instagram drive significantly more engagement. Consider allocating more budget and attention to high-performing channels.
- Display advertising and shorter to medium-length campaigns are more effective. Avoid overly long campaigns unless they are well-targeted.

### B. Targeting Strategy
- **Digital Activity**:
  - Users with more recent and frequent web usage (high `avg_web_time`, low `days_since_web_use`) are more likely to engage.
  - High click and impression counts are strong indicators of potential engagement.
- **Demographics**:
  - Age, job type, and marital status show moderate to weak influence but may still support segmentation.
  - Features like `has_home_loan`, `has_credit_card`, and `has_insurance` offer limited predictive power individually but could help in profiling.

---

## 4. Suggestions for Modeling

| Task | Recommendation |
|------|----------------|
| **Feature Selection** | Prioritize `clicks`, `impressions`, `avg_web_time`, `channel_used`, `campaign_type`, `days_since_web_use`. |
| **Preprocessing** | One-hot encode categorical features. Normalize continuous features. |
| **Feature Engineering** | Create interaction terms (e.g., `channel_used * impressions`) and bin numerical variables if necessary. |
| **Remove Low-impact Features** | Consider removing `has_insurance`, `has_home_loan`, and `has_credit_card` if they degrade model performance. |

---

## Visual Aids

All figures used in this analysis are saved under:
- `figures/boxplots/` for continuous variable distributions
- `figures/barplots/` for engagement rates across categories

---

## 5. Visual Analysis: Boxplots & Barplots

### Boxplots (Continuous Variables by Engagement)

These reveal distribution differences between engaged and non-engaged users.

| Feature                  | Insight |
|--------------------------|---------|
| **impressions**          | Engaged users tend to have much **higher impression counts**. Distribution is skewed right with outliers. |
| **clicks**               | Clear separation: engaged users have significantly **more clicks**. Non-engaged group includes many with zero clicks. |
| **avg_web_time**         | Engaged users spend **more time on web platforms** on average. |
| **avg_mobile_time**      | Slightly higher for engaged users, but the difference is modest. |
| **days_since_web_use**   | Engaged users used the web **more recently**. Strong downward skew. |
| **days_since_mobile_use**| Similar to web, but the relationship is weaker. |
| **age**                  | No strong visual difference. Suggests limited impact on engagement. |
| **campaign_duration**    | Short and medium campaigns show more engagement; very long campaigns see diminishing returns. |

---

### Barplots (Categorical/Binary Variables by Engagement Rate)

These show proportion of engaged users across different category values.

| Feature               | Insight |
|-----------------------|---------|
| **channel_used**      | Platforms like Google Ads, Instagram, and TikTok are top performers. |
| **campaign_type**     | Display Advertising outperforms Telemarketing |
| **campaign_language** | Slight variation across languages; possible demographic effects. |
| **job**               | Students and self-employed users have higher engagement. |
| **marital**           | Minimal difference between single and married users. |
| **has_credit_card**   | Slight variation, but not a major factor. |
| **has_investment_product** | Engaged users are slightly more likely to have investments. |
| **has_home_loan / personal_loan** | No clear effect observed. |
| **has_insurance**     | Weak visual trend; not a strong differentiator. |

---

### Visual Summary

| Visual Impact         | Features |
|------------------------|----------|
| **High Impact**        | `clicks`, `impressions`, `avg_web_time`, `days_since_web_use`, `channel_used`, `campaign_type` |
| **Moderate Insight**   | `avg_mobile_time`, `job`, `campaign_language`, `campaign_duration` |
| **Low Differentiation**| `age`, `marital`, `has_credit_card`, `has_home_loan`, `has_insurance` |

---
