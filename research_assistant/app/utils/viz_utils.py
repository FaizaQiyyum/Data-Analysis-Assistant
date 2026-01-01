import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
import numpy as np

# Set a professional style for research reports
plt.style.use('bmh') # Bayesian Methods for Hackers style - clean and readable

def get_base64_plot():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_visualizations(df: pd.DataFrame):
    viz_data = {}
    
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return viz_data

    # 1. Histograms
    cols_to_plot = numeric_df.columns[:4]
    n_cols = len(cols_to_plot)
    rows = (n_cols + 1) // 2
    
    plt.figure(figsize=(12, 4 * rows))
    for i, col in enumerate(cols_to_plot):
        plt.subplot(rows, 2, i + 1)
        sns.histplot(numeric_df[col].dropna(), kde=True, color='#2c3e50')
        plt.title(f'Distribution: {col}', fontsize=10)
        plt.xlabel('')
    plt.tight_layout()
    viz_data['distributions'] = get_base64_plot()

    # 2. Box Plots
    plt.figure(figsize=(max(6, 3 * n_cols), 6))
    sns.boxplot(data=numeric_df[cols_to_plot], palette='deep')
    plt.title('Outlier Detection (Box Plot)', fontsize=12)
    plt.xticks(rotation=45 if n_cols > 1 else 0)
    viz_data['boxplots'] = get_base64_plot()

    # 3. Correlation Heatmap (only if > 1 column)
    if numeric_df.shape[1] > 1:
        plt.figure(figsize=(10, 8))
        corr = numeric_df.corr()
        if not corr.isnull().all().all():
            mask = np.triu(np.ones_like(corr, dtype=bool))
            sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='RdBu_r', center=0)
            plt.title('Correlation Analysis', fontsize=12)
            viz_data['heatmap'] = get_base64_plot()

    return viz_data

    return viz_data
