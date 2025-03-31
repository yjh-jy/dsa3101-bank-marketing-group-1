# Measuring Campaign ROI

### Table of Contents
1. Problem Analysis
2. Exploratory Data Analysis (EDA)
3. Acquisition Cost Sub-Model
4. Conversion Rate Sub-Model
5. ROI Model
7. Key Recommendations

---

## 1. Problem Analysis

In the highly competitive banking industry, it is important for banks to maintain their competitiveness by focusing their marketing efforts on campaigns that generate the highest return on investment (ROI). However, banks often struggle to quantify the ROI for different marketing efforts, making it difficult to determine which campaigns generate the highest profitability and long-term customer value. Therefore, being able to measure and predict the ROI of marketing campaigns is crucial for efficient allocation of marketing budgets, ensuring that a bank employs the most effective marketing strategy.

To tackle this challenge, we aim to develop a model that can predict the ROI of various bank marketing campaigns based on key influencing factors such as conversion rate and acquisition cost. Conversion rate and acquisition cost will be estimated using 2 individual models, using campaign-specific features such as campaign type (email marketing, telemarketing, etc), campaign duration, target audience, campaign langauge, and campaign timeframe as inputs. Then, the outputs of these 2 sub-models will be used to develop a model to predict ROI.

---

## 2. Exploratory Data Analysis (EDA)

#### Campaign-related features vs Acquisition Cost, Conversion Rate, CLV

We explore the relationships between the campaign-related features and three key variables: Customer Lifetime Value (CLV), Acquisition Cost, and Conversion Rate. These insights guide our feature and model selection.

### **Customer Lifetime Value (CLV)**
| Observation |
|-------------|
| Campaign-related features do not significantly differentiate CLV |
| CLV has a relatively small range (680–810) |

> **Conclusion**: Omit CLV from analysis as it does not vary meaningfully across campaigns. If necessary, we may use its mean in ROI computation.

---

### **Acquisition Cost Sub-Model**

| Feature           | Insights |
|------------------|----------|
| **Campaign Type** | Clear cost hierarchy:<br>Affiliate Marketing > SEO > Telemarketing > Display Advertising > Email Marketing<br>→ **Strong differentiating factor** |
| **Target Audience** | Median acquisition cost is relatively consistent across groups<br>→ **Dropped due to low differentiating power** |
| **Campaign Language** | Cost decreases:<br>English → German → French → Spanish → Mandarin<br>→ **Included** |
| **Campaign Duration** | Slight positive trend with cost (possibly due to more resource requirements)<br>→ **Included** |

> **Model Choice**: Linear Regression using `campaign_type`, `campaign_language`, and `campaign_duration`
> Chosen for interpretability, simplicity, and favorable trial performance

---

### **Conversion Rate Sub-Model**

| Feature           | Insights |
|------------------|----------|
| **Campaign Type** | Clear conversion ranking:<br>Affiliate Marketing > SEO > Telemarketing > Display Advertising > Email Marketing<br>→ **Strong differentiating factor** |
| **Target Audience** | Conversion rate generally decreases as audience age increases<br>→ **Included** |
| **Campaign Language** | Minimal influence<br>→ **Dropped** |
| **Campaign Duration** | Minimal influence<br>→ **Dropped** |

> **Model Choice**: Linear Regression using `campaign_type` and `target_audience`  
> Same reasons as above

---

## 3. Acquisition Cost Sub-Model

After testing out several models, Linear Regression seemed to perform the best. We evaluated the model performance using metrics such as MSE, PMSE, R^2 and adjusted R^2. Then, we extracted the coefficients to analyse the contribution of each variable to the model prediction.

### **Model Performance**

| Metric         | Value | Interpretation |
|----------------|-------|----------------|
| **R²**         | 0.85  | Model explains ~85% of the variance in acquisition cost |
| **RMSE**       | $26   | Predictions deviate by ~$26 from actual values on average |

> The model is generally reliable and performs well, even when generalized to unseen data.

### **Key Relationships Between Features**

#### **Campaign Language**

| Language   | Cost Impact vs English | Insight |
|------------|------------------------|---------|
| **German** | +37%                   | High localization and media targeting costs in regions where the Portugese bank has limited presence |
| **Mandarin** | +28%                 | Similar reasons as German; reflects limited internal resources |
| **French** | +18%                   | |
| **Spanish** | −16%                  | Likely due to geographical proximity and linguistic similarity with Portuguese, reducing the need for external vendors |

> **Recommendation**: Prioritize **English** and **Spanish** campaigns for cost efficiency. Limit high-cost campaigns, such as those in **German** and **Mandarin**, unless supported by strong expected conversions.

---

#### **Campaign Type**

| Type                 | Cost Reduction vs Affiliate Marketing |
|----------------------|----------------------------------------|
| **Email Marketing**  | −94% |
| **Display Advertising** | −82% |
| **Telemarketing** | −63% |
| **SEO** | −33% |

> **Recommendation**: For cost-cutting, banks should focus on **email marketing** and **display advertising** campaigns, which scale more easily to larger audiences without incurring significant additional costs.

---

#### **Campaign Duration**

| Relationship | Insight |
|--------------|---------|
| Slight positive correlation | Each additional campaign day increases cost by ~1% |

> While longer campaigns cost more due to increased resources (manpower, ad space, tracking), the effect is minor compared to campaign type or language. Hence, it should not be prioritised as a lever for cost control.

---

Although we've identified methods to reduce marketing expenditure, these insights must be integrated with analysis on value generation (e.g. conversion rates) to fully assess ROI impact across different campaign strategies.

## 4. Conversion Rate Sub-Model

Similar to the acquisition cost model, Linear Regression performed best for predicting conversion rates after testing various models.

### **Model Performance**

| Metric         | Value      | Interpretation |
|----------------|------------|----------------|
| **R²**         | 0.82       | Model explains ~82% of the variance in conversion rate |
| **RMSE**       | 2.1%       | Predictions deviate by ~2.1 percentage points on average |

> Strong predictive ability with consistent performance

---

### **Relationships Between Features**

#### **Campaign Type**

| Campaign Type        | Conversion Rate Change vs Affiliate Marketing |
|----------------------|-----------------------------------------------|
| **SEO**              | −1.6 percentage points                        |
| **Telemarketing**    | −5.2 percentage points                        |
| **Display Advertising** | −8.4 percentage points                     |
| **Email Marketing**  | −11.9 percentage points                       |

> **Insights**:
- **Affiliate Marketing** yields the highest conversion rates; often driven by influencers, so they offer a more personalized and relatable experience that builds trust
- **Email Marketing** performs the worst, possibly due to spam filters and lack of personalization

> **Recommendations**:
- Focus on Affiliate Marketing and SEO for better conversion outcomes
- Improve email strategy by avoiding spam-triggering keywords and personalizing messages to boost reach and engagement

---

#### **Target Audience Age Group**

| Age Group     | Conversion Rate Change vs Age 18–24 |
|---------------|--------------------------------------|
| **25-34**     | −1.0 percentage points               |
| **35-44**     | −1.5 percentage points               |
| **45–54**     | −3.2 percentage points               |
| **55+**       | −4.1 percentage points               |

> Older age groups show reduced conversion, possibly due to lower digital engagement or a preference for in-person banking among older customers

> **Recommendations**:
- Prioritize younger age groups (especially 18–34) in digital marketing efforts.
- For older segments, consider exploring alternative channels or messaging strategies to better engage older audiences

---

Once again, these insights should be synthesized with those from other models to generate more holistic reccommendations.

## 5. ROI Model

We analyzed the distributions of **conversion rate** and **acquisition cost** to understand their relationship with ROI. Plotting a scatterplot of ROI against acquisition cost and conversion rate suggested a Linear Regression model would be appropriate.

---

### **Model Performance**

| Metric         | Value  | Interpretation |
|------------------|--------|----------------|
| **R²**           | 0.70   | Model explains ~70% of the variance in ROI |
| **RMSE**         | 0.52   |  Predictions deviate by ~0.5 percentage points on average |

> Strong model fit — ROI can be reliably predicted using conversion rate and acquisition cost.

---

### **Feature Relationships with ROI**

| Feature          | Coefficient | Insight |
|------------------|-------------|---------|
| **Conversion Rate** | +0.86      | Strong positive impact — increases in conversion rate significantly improve ROI |
| **Acquisition Cost** | −0.053    | Mild negative impact — cost slightly reduces ROI |

> **Key Insight**: 
- While minimizing cost is helpful, increasing conversion rate has a far greater effect on ROI and should be prioritized.

---

## 6. Key Recommendations

| **Goal**                  | **Action**                                                        | **Rationale**                                                                  |
|---------------------------|-------------------------------------------------------------------|--------------------------------------------------------------------------------|
| Increase Conversion Rate  | Prioritize conversion-improving strategies (listed below)         | These yield higher ROI, even if they come with slightly higher costs           |
|                           | Invest in Affiliate Marketing                                     | Highest conversions due to personalization and trust via influencer marketing  |
|                           | Invest in SEO                                                     | Generates organic traffic and higher-quality leads                             |
|                           | Re-evaluate Email Marketing Campaigns                             | Avoid spam-triggering language, add strong CTAs, personalize messages          |
|                           | Target younger audiences (18–34)                                  | Younger users are more digitally engaged and responsive to online campaigns    |
|                           | Use traditional channels for older audiences                      | Older users may prefer in-person or conventional communication methods         |
| Reduce Acquisition Cost   | Enhance Display Ads                                               | Make ads visually appealing, include CTAs, optimize for multiple devices       |
|                           | Scale improved Email and Display campaigns                        | Once optimized, these are low-cost channels that can scale to large audiences  |
