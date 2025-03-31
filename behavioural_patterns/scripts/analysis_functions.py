# Importing packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

def analyze_nps(df):
    """
    Analyze NPS (Net Promoter Score) across customer segments.
    """
    # Calculating the percentage distribution NPS categories within each segment
    nps_segment_dist = pd.crosstab(df['Segment'], df['nps_category'], normalize='index') * 100
    print('Percentage distribution of NPS categories within each segment:')
    print(nps_segment_dist)
    
    # Plotting the stacked bar chart for NPS distribution
    plt.figure(figsize=(8, 6))
    ax = nps_segment_dist.plot(kind='bar', stacked=True)
    plt.title('Distribution of NPS Categories Across Customer Segments')
    plt.xlabel('Customer Segment')
    plt.ylabel('Percentage (%)')
    plt.legend(title='NPS Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    # Annotate each bar with its percentage value
    for p in ax.patches:
        height = p.get_height()
        width = p.get_width()
        x = p.get_x() + width / 2
        y = p.get_y() + height / 2
        ax.annotate(f'{height:.2f}%', (x, y), ha='center', va='center', color='black', fontsize=10)
    plt.close()

def analyze_financial_health(df):
    """
    Analyze financial health across customer segments.
    """
    # Computing the correlation matrix for the selected financial variables
    variables = ['log_balance', 'log_debt', 'log_income', 'debt_to_income', 'balance_to_debt']
    correlation_matrix = df[variables].corr()
    print('\nCorrelation matrix for financial variables:')
    print(correlation_matrix)
    
    # Heatmap of correlation matrix for financial health metrics
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix for Financial Health Metrics')
    plt.close()
    
    # Boxplots for 'debt-to-income' and 'balance-to-debt' ratios by customer segment
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    sns.boxplot(x='Segment', y='debt_to_income', data=df, ax=ax[0])
    ax[0].set_title('Debt-to-Income Ratio by Customer Segment')
    ax[0].set_xlabel('Customer Segment')
    ax[0].set_ylabel('Debt-to-Income Ratio')
    sns.boxplot(x='Segment', y='balance_to_debt', data=df, ax=ax[1])
    ax[1].set_title('Balance-to-Debt Ratio by Customer Segment')
    ax[1].set_xlabel('Customer Segment')
    ax[1].set_ylabel('Balance-to-Debt Ratio')
    plt.close()
    
    # Filtering data for customers with days_past_due < 0 (on-time payments)
    on_time = df[df['days_past_due'] < 0]
    print(on_time)
    
    # Calculating the proportion of on-time payers in each segment
    on_time_counts = on_time.groupby('Segment').size()
    total_counts = df.groupby('Segment').size()
    on_time_proportion = (on_time_counts / total_counts) * 100
    print('\nProportion of on-time payers (%) in each segment:')
    print(on_time_proportion)
    
    # Barplot of the proportion of customers with on-time loan payments for each segment
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x=on_time_proportion.index, y=on_time_proportion.values, palette='viridis')
    plt.title('Proportion of On-Time Loan Payments Across Customer Segments')
    plt.xlabel('Customer Segments')
    plt.ylabel('Proportion of On-Time Payments (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y')
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}%', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    color='black', fontsize=10, 
                    xytext=(0, 5), textcoords='offset points')
    plt.close()
    
    # Calculating the percentage distribution of loan categories within each segment
    loan_cat_percent = pd.crosstab(df['Segment'], df['loan_category'], normalize='index') * 100
    print('\nPercentage distribution of loan categories within each segment:')
    print(loan_cat_percent)
    
    # Stacked bar chart for the percentage distribution of loan categories within each segment
    fig, ax = plt.subplots(figsize=(10, 6))
    loan_cat_percent.plot(kind='bar', stacked=True, colormap='Set2', width=0.8, ax=ax)
    plt.title('Percentage Distribution of Loan Categories within Each Segment', fontsize=14)
    plt.xlabel('Segment', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Loan Category', title_fontsize='13', fontsize='11', bbox_to_anchor=(1.05, 1), loc='upper left')
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.text(p.get_x() + p.get_width() / 2, p.get_y() + height / 2,
                    f'{height:.1f}%', ha='center', va='center', fontsize=10, color='black')
    plt.close()

def analyze_product_usage(df):
    """
    Analyze product usage across customer segments.
    """
    # Specified product columns for analysis
    product_columns = ['has_investment_product', 'has_credit_card', 
                       'has_fixed_deposit', 'has_insurance']
    # Calculating the average product ownership for each segment across specified product columns
    usage_summary = df.groupby('Segment')[product_columns].mean()
    print('\nAverage product ownership (%) for each segment:')
    print(usage_summary)
    
    # Barplot of product usage proportions by customer segment
    usage_summary_reset = usage_summary.reset_index()
    usage_melted = usage_summary_reset.melt(id_vars='Segment', 
                                             var_name='Product', 
                                             value_name='Proportion')
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=usage_melted, x='Product', y='Proportion', hue='Segment')
    plt.title('Product Usage Proportions by Customer Segment')
    plt.ylabel('Proportion of Customers Owning Product')
    plt.xlabel('Product')
    plt.legend(title='Segment')
    plt.xticks(rotation=45)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    color='black', fontsize=10, 
                    xytext=(0, 5), textcoords='offset points')
    plt.close()
    
    # Performing Chi-square test for statistical significance in product usage differences across segments
    for product in product_columns:
        print(f"\nChi-Square Test for {product}:")
        ct = pd.crosstab(df['Segment'], df[product])
        print("Contingency Table:")
        print(ct)
        chi2, p, dof, expected = stats.chi2_contingency(ct)
        print(f"Chi-square Statistic: {chi2:.4f}")
        print(f"Degrees of Freedom: {dof}")
        print(f"p-value: {p:.4f}")
        print("Expected Frequencies:")
        print(expected)
        if p < 0.05:
            print("=> The difference in usage across segments is statistically significant.")
        else:
            print("=> The difference in usage across segments is not statistically significant.")

def analyze_transactions(df):
    """
    Analyze transaction history across customer segments.
    """
    # Calculating the count of transactions for each segment
    tx_counts = df.groupby('Segment').size().reset_index(name='tx_count')
    print('\nTransaction count for each segment:')
    print(tx_counts)
    
    # Calculating the count of transactions for each customer in each segment
    customer_tx = df.groupby(['customer_id', 'Segment']).size().reset_index(name='tx_count')
    print('\nTransaction count for each customer in each segment:')
    print(customer_tx)
    
    # Calculating the average transaction count per segment
    avg_tx_count_by_segment = customer_tx.groupby('Segment')['tx_count'].mean().reset_index()
    print('\nAverage transaction count per segment:')
    print(avg_tx_count_by_segment)
    
    # Calculating the distribution of transaction types across segments
    tx_type_distribution = pd.crosstab(df['Segment'], df['transaction_type'])
    print('\nDistribution of transaction types across segments:')
    print(tx_type_distribution)
    
    # Calculating the distribution of money flow across segments
    flow_distribution = pd.crosstab(df['Segment'], df['money_flow'])
    print('\nDistribution of money flow across segments:')
    print(flow_distribution)
    
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    # Barplot of the average transaction count by customer segment
    sns.barplot(data=avg_tx_count_by_segment, x='Segment', y='tx_count', palette='viridis', ax=ax[0])
    ax[0].set_xlabel('Customer Segment')
    ax[0].set_ylabel('Average Transaction Count')
    ax[0].set_title('Average Transaction Count by Customer Segment')
    for p in ax[0].patches:
        ax[0].annotate(f'{p.get_height():.2f}', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha='center', va='center', 
                       color='black', fontsize=10, 
                       xytext=(0, 5), textcoords='offset points')
    # Barplot of the average transaction value by customer segment
    avg_transaction_value = df.groupby('Segment')['transaction_amt'].mean().reset_index()
    bars = ax[1].bar(avg_transaction_value['Segment'], avg_transaction_value['transaction_amt'], 
                     color=['skyblue', 'lightgreen', 'lightcoral'])
    ax[1].set_xlabel('Customer Segment')
    ax[1].set_ylabel('Average Transaction Value')
    ax[1].set_title('Average Transaction Value by Customer Segment')
    for bar in bars:
        ax[1].text(bar.get_x() + bar.get_width() / 2, 
                   bar.get_height(), 
                   f'{bar.get_height():.2f}', 
                   ha='center', 
                   va='bottom', 
                   fontsize=10, 
                   color='black')
    plt.close()
    
    # Average transaction amount, grouped by segment and money flow
    money_summary = df.groupby(['Segment', 'money_flow'])['transaction_amt'].mean().reset_index()
    print('\nAverage transaction amount by segment and money flow:')
    print(money_summary)
    
    # Merging transaction count for each customer segment with money flow
    merged_data = pd.merge(customer_tx, df[['customer_id', 'Segment', 'money_flow']], on=['customer_id', 'Segment'], how='left')
    # Calculating the average transaction count by segment and money flow
    avg_tx_count_by_flow = merged_data.groupby(['Segment', 'money_flow'])['tx_count'].mean().reset_index()
    
    fig, ax = plt.subplots(1, 2, figsize=(18, 6))
    # Barplot of average transaction count for money flow across segments
    sns.barplot(data=avg_tx_count_by_flow, x='Segment', y='tx_count', hue='money_flow', palette='viridis', ax=ax[0])
    for container in ax[0].containers:
        ax[0].bar_label(container, padding=3)
    ax[0].set_xlabel('Customer Segment')
    ax[0].set_ylabel('Average Transaction Count')
    ax[0].set_title('Average Transaction Count by Money Flow Across Customer Segments')
    ax[0].legend(title='Money Flow')
    # Barplot of average transaction amount for money flow across segments
    sns.barplot(data=money_summary, x='Segment', y='transaction_amt', hue='money_flow', palette='viridis', ax=ax[1])
    for container in ax[1].containers:
        ax[1].bar_label(container, fmt='%.2f', padding=3)
    ax[1].set_xlabel('Customer Segment')
    ax[1].set_ylabel('Average Transaction Amount')
    ax[1].set_title('Average Transaction Amount by Money Flow Across Customer Segments')
    ax[1].legend(title='Money Flow')
    plt.close()

def analyze_digital_engagement(df):
    """
    Analyze digital engagement across customer segments.
    """
    # Barplot of the mobile and web engagement rate for each customer segment
    fig, ax = plt.subplots(1, 2, figsize=(14, 7))
    sns.barplot(x='Segment', y='has_mobile_app', data=df, ax=ax[0])
    ax[0].set_title('Mobile App Usage Across Segments')
    for p in ax[0].patches:
        ax[0].annotate(f'{p.get_height():.2f}', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha='center', va='center', 
                       color='black', fontsize=10, 
                       xytext=(0, 20), textcoords='offset points')
    sns.barplot(x='Segment', y='has_web_account', data=df, ax=ax[1])
    ax[1].set_title('Web Account Usage Across Segments')
    for p in ax[1].patches:
        ax[1].annotate(f'{p.get_height():.2f}', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha='center', va='center', 
                       color='black', fontsize=10, 
                       xytext=(0, 20), textcoords='offset points')
    plt.close()
    
    # Grouping by segment and computing the most recent usage date for mobile and web
    recency_metrics = df.groupby('Segment').agg({
        'last_mobile_use': 'max',
        'last_web_use': 'max'
    })
    print('\nMost recent mobile and web usage dates by segment:')
    print(recency_metrics)
    
    # Boxplot of mobile and web engagement ratio across customer segments
    sns.boxplot(x='Segment', y='mobile_web_ratio', data=df)
    plt.title('Mobile vs Web Engagement Ratio Across Segments')
    plt.close()
    
    # Identifying inactive users (those with no mobile or web logins)
    inactive_users = df[(df['mobile_logins_wk'] == 0) & (df['web_logins_wk'] == 0)]
    inactive_by_segment = inactive_users.groupby('Segment').size()
    print('\nNumber of inactive users in each segment:')
    print(inactive_by_segment)