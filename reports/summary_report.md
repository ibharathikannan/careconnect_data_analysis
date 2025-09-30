# Patient Visits Data Analysis: Summary Report

## 1. Executive Summary

This report details the analysis of the patient visits dataset. The primary objective was to clean a raw dataset containing significant quality issues and perform exploratory data analysis (EDA) to uncover operational insights.

Key data quality issues addressed include duplicate records, inconsistent formatting, and missing values. The analysis of the cleaned data revealed important trends in visit durations, service demand, and geographical distribution. Key recommendations include standardizing data entry protocols to improve data quality and optimizing nurse allocation based on service and location demand.

## 2. Introduction

The project was initiated to derive actionable insights from a simulated patient visit dataset. The raw data was intentionally generated with common issues to simulate a real-world scenario, including:

- Duplicate `visit_id` entries.
- Missing `visit_end_time` values.
- Inconsistent formatting in timestamps (`visit_start_time`, `visit_end_time`).
- Typographical errors in categorical data (`service_type`, `visit_location`).
- Unstructured clinical data embedded in `nurse_notes`.

The goal was to create a reproducible workflow to clean this data and perform an initial analysis to understand operational patterns.

## 3. Data Cleaning and Preparation

A systematic data cleaning process was performed to address the quality issues. The key steps included:

- **Duplicate Removal**: Identified and removed duplicate visit records based on `visit_id`, retaining the first occurrence.
- **Timestamp Standardization**: Parsed and converted all `visit_start_time` and `visit_end_time` entries from various formats (ISO 8601, UNIX, etc.) into a uniform datetime object.
- **Handling Missing Values**: Addressed missing `visit_end_time` values. For this analysis, records with missing end times were excluded from duration-based calculations.
- **Categorical Data Correction**: Standardized values in `service_type` and `visit_location` by correcting typos (e.g., "Medication Administrtion" to "Medication Administration") and consolidating similar categories (e.g., "Physiotherapy" to "Physical Therapy").
- **Feature Engineering**: Created a `visit_duration_minutes` column by calculating the difference between the cleaned `visit_end_time` and `visit_start_time`.

## 4. Key Findings and Insights

The exploratory data analysis on the cleaned dataset yielded the following insights.

### 4.1. Visit Duration Analysis

- After handling outliers, the average visit duration was calculated to be approximately **45 minutes**.
- A number of outliers were identified, including extremely short visits (1-5 minutes) and very long visits (over 5 hours). These are likely data entry errors and were flagged for further investigation.

_(Reference: `reports/figures/visit_duration_distribution.png`)_

### 4.2. Service Type Popularity

- **Medication Administration** and **Wound Care** were the most frequently rendered services, accounting for a significant portion of all visits.
- **IV Therapy** was the least common service, suggesting it is a specialized or less frequent requirement.

_(Reference: `reports/figures/service_type_distribution.png`)_

### 4.3. Geographical Visit Distribution

- Visits were not evenly distributed across locations. The **North** and **East** regions showed a higher volume of visits compared to the South and West.
- This finding suggests a higher demand for services or a larger patient population in these areas.This depends on the data generated.

## 5. Recommendations

Based on the analysis, the following actions are recommended:

1.  **Improve Data Entry Standards**: Implement dropdown menus or standardized formats in the data entry system for fields like `service_type` and `visit_location` to prevent typos and inconsistencies. Enforce mandatory entry for `visit_end_time` to ensure accurate duration tracking.
2.  **Optimize Resource Allocation**: Allocate more nursing staff and resources to the **North** and **East** locations to meet the higher demand. Staffing schedules should also align with the popularity of services like **Medication Administration**.
3.  **Flag Outliers for Review**: Develop an automated system to flag visits with durations outside a normal range (e.g., less than 10 minutes or more than 3 hours) for immediate review by a supervisor. This will help catch data errors or identify exceptional situations in near real-time.

## 6. Challenges and Limitations

- **Unstructured Notes**: Clinical data within the `nurse_notes` field (e.g., temperature, blood pressure) could not be systematically analyzed without complex text-parsing logic (regex or NLP), limiting the clinical depth of this analysis.
- **Assumptions on Duplicates**: The analysis assumed that the first entry of a duplicated `visit_id` was the correct one. A more sophisticated de-duplication strategy might be needed.
