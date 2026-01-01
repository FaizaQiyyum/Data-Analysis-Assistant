# Research Data Analysis Assistant

## Overview
The Research Data Analysis Assistant is an internal tool designed to streamline the initial stages of data exploration within scientific and research organizations. Recommendations adapt based on variable count to ensure statistical validity. By automating data quality checks, statistical analysis, and visualization, this tool allows researchers and engineers to quickly gain an objective understanding of new datasets before proceeding to deeper investigative phases.

## The Problem it Solves
In scientific computing, the first step of any analysis involves "cleaning" and "profiling" data. This process is often repetitive and time-consuming. This tool automates the generation of:
- **Data Health Summaries**: Identifying missing values and potential outliers.
- **Statistical Profiles**: Calculating distributions and correlations.
- **Visual Evidence**: Producing histograms, box plots, and heatmaps for quick visual inspection.

Automating these steps reduces human error in initial profiling and ensures a consistent baseline of data quality across different research projects.

## Project Structure
The code is modularly structured for clarity and maintainability:
- `main.py`: The entry point for the FastAPI backend.
- `app/analysis/`: Contains the core logic for data processing and heuristic summary generation.
- `app/utils/`: Visualization utilities using Matplotlib and Seaborn.
- `app/static/`: Frontend assets (HTMl, CSS, JS) with a professional "Internal Tool" aesthetic.

## Local Execution Guide

### Prerequisites
- Python 3.8+
- Recommended: A virtual environment (`python -m venv venv`)

### Step-by-Step Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

3. **Access the Tool**:
   Open your browser and navigate to: `http://localhost:8000`

4. **Analyze Data**:
   Upload any structured CSV file to receive an automated profile.

## Project Limitations
- **File Format**: Currently supports only standard CSV files.
- **Scale**: Optimized for datasets that fit within local memory (Pandas).
- **Automation**: The "Analytical Summary" is heuristic-based and intended to support, not replace, human reasoning.

## Future Extensions
- Support for additional file formats (JSON, Parquet).
- Customizable visualization parameters.
- Integration of more advanced statistical tests (e.g., normality checks, T-tests).
- Exportable PDF research reports.

---
*This tool is intended for internal use only. It prioritizes correctness, clarity, and maintainability for collaborative research environments. The tool adapts its analysis based on dataset structure.*
