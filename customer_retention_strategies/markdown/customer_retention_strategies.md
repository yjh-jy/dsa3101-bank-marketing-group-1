# Customer Churn Prediction

## Problem Statement

How can we proactively identify and mitigate customer churn by analyzing behavioral, transactional, and financial patterns using machine learning techniques?

---

## Churn Risk Segments

| Risk Level     | Behaviour                                                                 |
|----------------|---------------------------------------------------------------------------|
| High Risk      | Digitally inactive, low product engagement, high debt burden              |
| Medium Risk    | Moderate digital activity, some product usage, average risk profile       |
| Low Risk       | Frequent engagement, high product usage, financially stable               |

---

## Data Preparation Summary

### Datasets Used

- `customer.csv`: Demographic & financial attributes  
    1. **Debt & Income**: Used to derive debt-to-income ratio  
    2. **Balance**: Used to understand account activity and financial health  
    3. **Age, Tenure, NPS, Dependents**: Profile features  

- `digital_usage.csv`: Digital engagement behavior  
    1. **has_mobile_app / has_web_account**  
        - Binary digital onboarding status  
    2. **mobile_logins_wk / web_logins_wk**  
        - Engagement frequency indicators  

- `products_owned.csv`: Ownership of bank products  
    - Counted total products to reflect relationship depth  

- `loans.csv`: Loan status, especially **unpaid loans** as churn risk signals  

- `transactions.csv`: Transaction activity  
    1. **transaction_date**: Used to measure recency  
    2. **paid_off_date**: Used for churn labeling when unpaid for 12+ months  

---

## Feature Engineering

### Financial Features
- **Debt-to-Income Ratio**: Indicates financial pressure  
- **Total Products Owned**: Sum of all product binary flags  

### Digital Activity
- **Last Mobile & Web Use**: Measures digital engagement recency  

### Churn Labeling Logic
- Customers with **no transactions in the past 15 days** and **digital inactivity for 6+ months**  
- Customers with **unpaid loans** and **no transactions for 12+ months**  

### Target
- Created binary label: `churn_risk` (True = churn risk)

---

## Visual Insights

### ⚖️ Balanced Churn Class Distribution

![Churn Class Distribution](visuals/churn_class_distribution.png)

SMOTE was used to handle class imbalance, ensuring that churn and non-churn samples are equally represented in training. This helps avoid bias in predictions and improves model fairness.

---

### 📊 Confusion Matrix

![Confusion Matrix](visuals/confusion_matrix.png)

| Predicted → / Actual ↓ | Non-Churn | Churn |
|------------------------|-----------|-------|
| **Non-Churn**          | 2355      | 2     |
| **Churn**              | 80        | 623   |

- **True Positives:** 623 churners correctly identified  
- **False Negatives:** 80 churners missed by model  
- **False Positives:** Just 2 non-churners incorrectly flagged  

**Interpretation:**  
The model achieves **high accuracy** with very few false positives and strong recall for churners, making it highly useful for CRM-triggered interventions.

---

### 🔍 Feature Importance

![Feature Importance](visuals/feature_importance.png)

**Top Features Driving Churn Risk:**

| Feature                | Interpretation                                         |
|------------------------|--------------------------------------------------------|
| `debt`                | High debt correlates with increased churn likelihood   |
| `debt_to_income_ratio`| Reflects financial pressure                            |
| `balance`, `income`   | Financial wellness and stability                       |
| `mobile_logins_wk`    | Low usage suggests digital disengagement               |
| `total_products_owned`| Strong engagement predictor; fewer products → churn    |

**Observation:**  
Churn is largely driven by a combination of **financial stress** and **digital inactivity**. Customers with fewer product ties, low engagement, or high debt are most likely to churn.

---

## Output: Churn Warning Report

The final output file `churn_warning_report.csv` includes:
- Churn probability score (0 to 1)
- Risk level (Low / Medium / High)
- Key attributes: age, balance, tenure, digital flags, product count

This file can be used to trigger automated CRM actions or retention team alerts.

---

## Business Recommendations

1. **Prioritize High-Risk Customers:**
   - Use the churn scores to filter and flag at-risk individuals.
   - Consider proactive outreach (SMS, email, or call).

2. **Launch Digital Engagement Campaigns:**
   - Re-engage customers with low or no recent app/web usage.

3. **Offer Targeted Products:**
   - Upsell products to customers with low product ownership.

4. **Support Financially Strained Clients:**
   - Customers with high debt or low income may need personalized financial advisory services.

5. **CRM Integration:**
   - Feed churn scores into CRM system to automate retention triggers and assign high-risk customers to relationship managers.

---
