# Cost-Effectiveness of Campaigns

## Problem Statement
How can we balance personalisation with cost-effectiveness in marketing campaigns?

## Data Preparation
**Datasets used**
- campaigns.csv: This dataset contains information about various marketing campaigns. Key details of each campaign are:
  - campaign_type: The type of marketing campaign.
  - campaign_language: The language used in the campaign.
  - target_audience: The target demographic for the campaign.
  - campaign_duration: The duration of the campaign in days.
- engagement_details.csv: This dataset captures customer engagement with various campaigns. It contains data on how customers interacted with the campaigns.
  - has_engaged: Whether a customer engaged with the campaign.
  - duration: The duration for which a customer engaged with the campaign.
  - impressions: The number of times the campaign was viewed or displayed to the customers.
- customer.csv: This dataset contains the demographic and behavioural information about the customers. 
  - age: The age of the customer.
  - income: The income of the customer.
  - eduaction: The highest level of education attained by the customer.
  - job: The occupation of the customer.
  - dependents: The number of dependents the customer has.
  - customer_lifetime_value: The total value the customer has brough to the company over their lifetime.

## Feature Engineering
Feature engineering is a crucial step in preparing the data for model training and analysis. 

### Calculating the personalisation score
The personalisation scores for each campaign reflect how tailored and relevant a campaign is for a given target audience. A higher personalisation score means that the campaign is better suited for specific audience segments, offering more customised content and messaging.

Score calculation:
- **Campaign type weights**: Different campaign types are assigned different weights based on their level of personalisation. For example, email marketing receives the highest weight as it often involves more tailored content for individual recipients. Display advertising receives the lowest weight as it is typically more generic.
- **Language score**: Campaigns targeting customers who speak languages such as Mandarin are assigned a higher language score. More common languages such as English receive a lower score.
- **Target audience score**: Different age groups are considered based on the presumed relevance of the campaign to that demographic. The age group of 35-44 receives the highest score as this group is typically highly engaged with personalised marketing content. They are often in a position where they are familiar with technology and digital campaigns, they are generally in a financially stable phase of life and are at the peak of their spending power and they are more likely to build loyalty to brands.
- **Campaign duration score**: Longer campaigns are often more engaging and personalised, as they allow for sustained interactions.

The final personalisation score is a weighted sum of the above factors.

### Calculating the engagement 
The engagement scores for each campaign indicate their effectiveness – how well the campaign has succeeded in attracting interactions from its audience. Higher engagement scores suggest campaigns have resonated well with customers and elicited more significant actions, such as clicks and views.

**Engagement rate** measures the frequency of interactions, whilst the **effective engagement rate** considers the depth of engagement by accounting for the duration of interactions. Both provide complementary insights into how well a campaign resonates with its audience.

### Preprocessing data functions
To prepare the data for model training, the script includes preprocessing functions that handle encoding categorical features and defining the features and target variables.

- **Label encoding**: The LabelEncoder is used to encode categorical variables such as campaign_type, campaign_language and target_audience into numerical values.
- **Defining features and target variables**: The preprocess_data function splits the dataset into features (X) and target variables (y).
- **Scaling acquisition cost**: acquisition_cost is normalised to make it easier for the model to predict.

### Calculating personalisation potential
The customer personalisation potential score evaluates how likely a customer is to respond positively to personalised marketing strategies.

Score calculation:
- **Age score**: A mature audience is more able to engage with personalised content as they have higher spending power.
- **Income score**: Customers with higher incomes may be responsive to premium or personalised offerings.
- **Job and education**: Professionally educated or employed customers may prefer certain types of content or campaigns.
- **Dependents**: Customers with dependents may be more receptive to personalised offers that cater to family or financial needs.
- **Customer lifetime value**: High lifetime value customers are prime candidates for more personalised, long-term engagement.

The final personalisation score is a weighted sum of the above factors.

## Models
Several models are trained and used to predict key campaign metrics that indicate cost-effectiveness.

### Personalisation model and engagement model
The personalisation model and engagement model are a Random Forest Regressors trained to predict the personalisation score and engagement score of a campaign respectively. The input features for both models included campaign_type, campaign_language, target_audience and campaign_duration.

Random Forest is used because it is a robust, ensemble learning method that can handle complex, non-linear relationships between the input features and target variables. It works well with both categorical and numerical data and helps capture interactions between features without requiring explicit specification. This makes it suitable for predicting both continuous scores with high accuracy and reliability.

### Cost model
The cost model predicts the acquisition cost for each campaign, which is crucial for understanding the financial efficiency of a campaign. The input features for the cost model are campaign_type, campaign_language, target_audience and campaign_duration.

The Random Forest Regressor is again used for the cost model because it works well for predicting continuous values and capturing the complex relationships between features and the target variable.

### Cost-benefit ratio
The cost-benefit ratio is a key metric for evaluating the effectiveness of a campaign in terms of its cost and predicted benefits. It is calculated by dividing the normalised acquisition cost by the benefit of the campaign, where the benefit is a weighted sum of the personalisation score and the engagement score.

The cost-benefit ratio helps identify the efficiency of a campaign. A higher ratio indicates a campaign with a lower cost and higher effectiveness, while a lower ratio suggests that the campaign may not be delivering enough value relative to its cost.

## Business Recommendations

### Key insights
- Telemarketing for customers below 35 years old and affiliate marketing for customers above 45 years old demonstrated the highest cost-benefit ratios, indicating that these campaigns successfully combine strong personalisation with lower costs.
- Campaigns targetted at customers in the 45-54 year old age range generally demonstrated higher cost-benefit ratios, indicating that this group of customers are most responsive to tailored campaigns.
- High value customers, due to frequent engagement and higher spending capacity, showed stronger personalisation scores.

### Business Impact
- To improve cost-effectiveness, the bank should prioritise campaigns for upper-middle-age and middle-aged customers, i.e. customers above 45 years old. For high-value customers, the bank should deepen personalisation efforts, leveraging their frequent engagement and transaction data for tailored content.