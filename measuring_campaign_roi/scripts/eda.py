import os
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting


def generate_eda_plots(df, save_path):
    """
    Generates and saves standard EDA plots (boxplots and lineplots) 
    showing relationships between campaign features and target variables.
    """
    os.makedirs(save_path, exist_ok=True)

    categorical_vars = ['campaign_type', 'target_audience', 'campaign_language']
    numerical_targets = ['avg_clv', 'log_acquisition_cost', 'conversion_rate']
    titles = ['Customer Lifetime Value (CLV)', 'Log Acquisition Cost', 'Conversion Rate']

    # ---- Boxplots ----
    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    for i, cat in enumerate(categorical_vars):
        for j, num in enumerate(numerical_targets):
            sns.boxplot(data=df, x=cat, y=num, ax=axes[i, j])
            axes[i, j].set_title(f'{titles[j]} by {cat.replace("_", " ").title()}')
            axes[i, j].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(os.path.join(save_path, "EDA_boxplots_categorical_vs_targets.png"))
    plt.close()

    # ---- Lineplots: Campaign Duration vs numerical targets ----
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for j, num in enumerate(numerical_targets):
        sns.lineplot(data=df, x="campaign_duration", y=num, ax=axes[j])
        axes[j].set_title(f'{titles[j]} by Campaign Duration')
        axes[j].set_xlabel("Campaign Duration (Days)")
        axes[j].set_ylabel(titles[j])

    plt.tight_layout()
    plt.savefig(os.path.join(save_path, "EDA_lineplots_duration_vs_targets.png"))
    plt.close()


def generate_3d_roi_scatterplots(df, preds_conv, preds_cost, save_path):
    """
    Generates 3D scatterplots of:
    1. Actual conversion rate vs acquisition cost vs ROI
    2. Predicted conversion rate vs predicted acquisition cost vs ROI

    Parameters:
    - df (DataFrame): Original data containing 'conversion_rate', 'acquisition_cost', and 'roi'
    - preds_conv (array-like): Predicted conversion rates
    - preds_cost (array-like): Predicted acquisition costs
    - save_path (str): Directory to save the plot
    """
    os.makedirs(save_path, exist_ok=True)
    fig = plt.figure(figsize=(18, 8))

    # Actual data
    ax1 = fig.add_subplot(121, projection='3d')
    sc1 = ax1.scatter(df['conversion_rate'], df['acquisition_cost'], df['roi'],
                      c=df['roi'], cmap='viridis', alpha=0.8)
    ax1.set_xlabel("Conversion Rate")
    ax1.set_ylabel("Acquisition Cost")
    ax1.set_zlabel("ROI")
    ax1.set_title("Actual: Conversion Rate & Acquisition Cost vs ROI")
    fig.colorbar(sc1, ax=ax1, shrink=0.5, aspect=10)

    # Predicted data
    ax2 = fig.add_subplot(122, projection='3d')
    sc2 = ax2.scatter(preds_conv, preds_cost, df['roi'],
                      c=df['roi'], cmap='viridis', alpha=0.8)
    ax2.set_xlabel("Predicted Conversion Rate")
    ax2.set_ylabel("Predicted Acquisition Cost")
    ax2.set_zlabel("ROI")
    ax2.set_title("Predicted: Conversion Rate & Acquisition Cost vs ROI")
    fig.colorbar(sc2, ax=ax2, shrink=0.5, aspect=10)

    plt.tight_layout()
    plot_path = os.path.join(save_path, "scatterplot_conversion_cost_vs_roi.png")
    plt.savefig(plot_path)
    plt.close()