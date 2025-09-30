pply

# Patient Visits Data Analysis

## Project Overview

This project aims to clean, analyze, and derive insights from a simulated dataset of patient visits. The primary goal is to process raw data containing various quality issues and prepare it for analysis.

## Project Structure

- `data/raw/`: Contains the original, raw `visits.csv` dataset.
- `data/processed/`: Contains the cleaned and processed data, ready for analysis.
- `notebooks/`: Contains Jupyter notebooks for exploratory data analysis (EDA).
- `scripts/`: Contains Python scripts for reproducible tasks like data generation and cleaning.
- `reports/figures/`: Contains visualizations generated during analysis.

## Setup

1.  **Clone the repository (if applicable)**

    ```bash
    git clone https://github.com/ibharathikannan/careconnect_data_analysis.git
    cd data_analysis_project
    ```

2.  **Create a virtual environment and activate it**

    ```bash
    conda create -n visits python=3.7.10 -y
    ```

    ```bash
    conda activate visits
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Generate the dataset**
    Run the data generator script to create the raw `visits.csv` file.

    ```bash
    python scripts/data_generator.py
    ```

2.  **Perform Data Cleaning and EDA**
    Launch JupyterLab and open the notebooks in the `notebooks/` directory to start the analysis.
    ```bash
    jupyter lab
    ```
