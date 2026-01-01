import pandas as pd
import numpy as np
import json
from sklearn.ensemble import IsolationForest

def convert_to_python_types(obj):
    """
    Recursively converts NumPy types to standard Python types for JSON compatibility.
    """
    if isinstance(obj, dict):
        return {str(k): convert_to_python_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, np.ndarray)):
        return [convert_to_python_types(i) for i in obj]
    elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32, np.float16)):
        return float(obj) if np.isfinite(obj) else None
    elif pd.isna(obj):
        return None
    return obj

def detect_trends(df: pd.DataFrame):
    """
    Detects simple monotonic trends in numeric columns.
    """
    trends = []
    numeric_df = df.select_dtypes(include=[np.number])
    for col in numeric_df.columns:
        if len(numeric_df[col].dropna()) < 2:
            continue
        if numeric_df[col].is_monotonic_increasing:
            trends.append(f"Variable '{col}' shows a consistent increasing trend.")
        elif numeric_df[col].is_monotonic_decreasing:
            trends.append(f"Variable '{col}' shows a consistent decreasing trend.")
    return trends

def analyze_dataset(df: pd.DataFrame):
    """
    Performs comprehensive statistical analysis on the dataset.
    """
    analysis = {}
    
    # Basic dataset info
    analysis['info'] = {
        'rows': int(df.shape[0]),
        'columns': int(df.shape[1]),
        'column_names': df.columns.tolist(),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'missing_values': {col: int(val) for col, val in df.isnull().sum().to_dict().items()},
        'duplicate_count': int(df.duplicated().sum())
    }
    
    # Numeric analysis
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        # Convert stats to standard python types for JSON serialization
        raw_stats = numeric_df.describe().to_dict()
        analysis['stats'] = {
            col: {stat: float(val) if pd.notnull(val) else None for stat, val in col_stats.items()}
            for col, col_stats in raw_stats.items()
        }
        
        # Correlation matrix (only if more than 1 numeric column)
        if numeric_df.shape[1] > 1:
            raw_corr = numeric_df.corr().replace({np.nan: None}).to_dict()
            analysis['correlation'] = {
                col1: {col2: float(val) if val is not None else None for col2, val in col1_vals.items()}
                for col1, col1_vals in raw_corr.items()
            }
        else:
            analysis['correlation'] = {}
        
        # Trend detection
        analysis['trends'] = detect_trends(df)
        
        # Simple outlier detection using Isolation Forest
        if len(numeric_df) > 10:
            clean_numeric = numeric_df.fillna(numeric_df.median())
            iso = IsolationForest(contamination=0.05, random_state=42)
            outliers = iso.fit_predict(clean_numeric)
            analysis['outlier_count'] = int((outliers == -1).sum())
        else:
            analysis['outlier_count'] = 0
    else:
        analysis['stats'] = {}
        analysis['correlation'] = {}
        analysis['trends'] = []
    analysis['outlier_count'] = int(analysis.get('outlier_count', 0))
            
    return convert_to_python_types(analysis)

def generate_analytical_summary(analysis_results):
    """
    Generates a conservative, context-aware analytical summary with scientific precision.
    """
    info = analysis_results.get('info', {})
    stats = analysis_results.get('stats', {})
    missing = info.get('missing_values', {})
    outlier_count = analysis_results.get('outlier_count', 0)
    duplicate_count = info.get('duplicate_count', 0)
    correlation = analysis_results.get('correlation', {})
    
    observations = []
    quality_issues = []
    next_steps = []
    
    # 1. Observations
    var_count = info.get('columns', 0)
    row_count = info.get('rows', 0)
    
    if var_count == 1:
        observations.append(f"The dataset contains {row_count} records with a single measured variable.")
    else:
        observations.append(f"The dataset contains {row_count} records across a multidimensional space of {var_count} variables.")
    
    if stats:
        numeric_cols = list(stats.keys())
        observations.append(f"Primary numeric factors analyzed include: {', '.join(numeric_cols)}.")

    # Trend observation
    trends = analysis_results.get('trends', [])
    for trend in trends:
        observations.append(trend)

    # Correlation observation (strictly multi-variable)
    if var_count > 1 and correlation:
        strong_corr = []
        for col1 in correlation:
            for col2, val in correlation[col1].items():
                if val is not None and col1 < col2 and abs(val) > 0.7:
                    strong_corr.append(f"'{col1}' and '{col2}' (r={val:.2f})")
        if strong_corr:
            observations.append(f"Identified significant linear associations between: {', '.join(strong_corr)}.")

    # 2. Quality Issues
    if duplicate_count > 0:
        quality_issues.append(f"Duplicate detection identified {duplicate_count} identical records in the dataset.")

    for col, count in missing.items():
        if count > 0:
            if count > (row_count * 0.2):
                quality_issues.append(f"Significant data sparsity in '{col}': {count} missing values ({(count/row_count)*100:.1f}%).")
            else:
                quality_issues.append(f"Presence of missing values in '{col}': {count} entries ({(count/row_count)*100:.1f}%).")

    if outlier_count > 0:
        quality_issues.append(f"Automated anomaly detection identified {outlier_count} potential outliers in the feature distribution.")
    
    if not quality_issues:
        quality_issues.append("No significant automated quality issues were detected.")

    # 3. Next Steps (Logic hardened for scientific validity)
    if any(count > 0 for count in missing.values()):
        next_steps.append("Investigate missing data patterns to determine if values are Missing At Random (MAR) or indicate systemic measurement error.")
    
    if duplicate_count > 0:
        next_steps.append("Verify whether duplicate records represent redundant telemetry or legitimate repeated observations.")

    if var_count <= 1:
        # Univariate specific suggestions (EXACT wording from CERN-grade requirements)
        next_steps.append("Perform a comprehensive distribution analysis to understand the spread and central tendency of the measured variable.")
        next_steps.append("Conduct a frequency analysis to identify dominant values or categories within the observation set.")
        next_steps.append("Execute detailed outlier detection to determine the impact of extreme values on the overall statistical profile.")
        next_steps.append("Consider data enrichment or additional variable collection to enable bivariate or multivariate relationship discovery.")
    else:
        # Multivariate suggestions - strictly restricted to datasets with 2+ variables
        if correlation and any(any(val is not None and abs(val) > 0.7 for val in d.values() if isinstance(val, (int, float))) for d in correlation.values()):
            next_steps.append("Consider feature selection or dimensionality reduction for highly correlated variables to mitigate multicollinearity.")
        
        if outlier_count > 0:
            next_steps.append("Perform a sensitivity analysis by comparing analytical results with and without identified outliers.")
        
        next_steps.append("Proceed to specific bivariate or multivariate relationship exploration for identifying potential causal or predictive factors.")
        next_steps.append("Perform multivariate analysis to further investigate complex dependencies between the variables.")

    return {
        "observations": observations,
        "quality_issues": quality_issues,
        "next_steps": next_steps
    }
