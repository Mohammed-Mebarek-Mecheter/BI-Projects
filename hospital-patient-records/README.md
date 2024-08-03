# Massachusetts General Hospital KPI Dashboard

## Project Overview

This project involves creating a high-level KPI dashboard for Massachusetts General Hospital (MGH). The purpose of the dashboard is to provide the executive team with visibility into the hospital's recent performance based on a subset of patient records. The key questions addressed by the dashboard are:

1. How many patients have been admitted or readmitted over time?
2. How long are patients staying in the hospital, on average?
3. How much is the average cost per visit?
4. How many procedures are covered by insurance?

The dashboard is built using Streamlit and integrates interactive visualizations and tables to explore the data effectively.

## Project Structure

```
hospital-patient-records/
├── .gitignore
├── app.py
├── data/
│   ├── processed/
│   │   ├── processed_data.csv
│   │   ├── records.csv
│   ├── raw/
│   │   ├── data_dictionary.csv
│   │   ├── encounters.csv
│   │   ├── organizations.csv
│   │   ├── patients.csv
│   │   ├── payers.csv
│   │   ├── procedures.csv
├── main.py
├── notebooks/
│   ├── exploratory_data_analysis.ipynb
│   ├── simple.ipynb
├── src/
│   ├── app/
│   │   ├── components.py
│   │   ├── utils.py
│   │   ├── __init__.py
│   ├── data/
│   │   ├── clean_data.py
│   │   ├── load_data.py
│   │   ├── process_data.py
│   │   ├── __init__.py
│   ├── visualizations/
│   │   ├── admissions.py
│   │   ├── cost_per_visit.py
│   │   ├── insurance_coverage.py
│   │   ├── length_of_stay.py
│   │   ├── readmissions.py
│   │   ├── __init__.py
│   ├── __init__.py
├── __init__.py
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/hospital-patient-records.git
cd hospital-patient-records
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

## App Features and Components

### Filters

The app includes a sidebar with various filters to customize the data view:

- **Date Range Filter**: Select the start and end dates to filter data by a specific time range.
- **Age Group**: Filter patients based on age groups (e.g., 0-18, 19-35, 36-50, 51-65, 66+).
- **Gender**: Filter patients based on gender (e.g., Male, Female, Other).
- **Encounter Class**: Filter based on the type of encounter (e.g., Inpatient, Outpatient, Emergency, Ambulatory).
- **Insurance Provider**: Filter based on the insurance provider.
- **Readmitted**: Filter based on whether the patient was readmitted (Yes/No).

### Tabs and Visualizations

The app has five main tabs, each providing insights into different performance metrics:

1. **Admissions Over Time**: Shows a line chart of the number of admissions over time.
2. **Readmissions Over Time**: Displays a line chart of the number of readmissions over time.
3. **Average Length of Stay**: Visualizes the average length of hospital stay using a bar chart.
4. **Average Cost Per Visit**: Presents the average cost per visit through a bar chart.
5. **Insurance Coverage**: Features a heatmap showing the top 10 percentages of procedures covered by insurance.

### Interactive Tables

Each tab also includes an interactive table displayed using `AgGrid`. The tables allow for easy exploration and pagination of the filtered data.

### File Descriptions

- **`app.py`**: Main file to run the Streamlit app. Sets up the layout, sidebar filters, tabs, and visualizations.
- **`main.py`**: To execute the ETL process and clean the raw data.
- **`src/app/utils.py`**: Contains utility functions for loading and filtering data.
- **`src/app/components.py`**: Handles the rendering of the sidebar and its filters.
- **`src/data/load_data.py`**: Script to load the raw data files.
- **`src/data/clean_data.py`**: Script to clean and preprocess the data.
- **`src/data/process_data.py`**: Script to process the cleaned data for analysis.
- **`src/visualizations/`**: Directory containing separate modules for each type of visualization (admissions, readmissions, length of stay, cost per visit, and insurance coverage).

### Data Cleaning and Processing

1. **Loading Data**: The `load_data` function reads the raw CSV files and converts relevant columns to datetime format.
2. **Cleaning Data**: The `clean_data` script handles missing values and irrelevant columns.
3. **Processing Data**: The `process_data` script merges datasets and calculates derived features like encounter duration and patient age at the time of encounter.

## Conclusion

This Streamlit app provides a comprehensive dashboard to explore key performance metrics for Massachusetts General Hospital. The interactive visualizations and filters enable detailed analysis of admissions, readmissions, length of stay, cost per visit, and insurance coverage. The app is designed to offer valuable insights to the hospital's executive team, aiding in data-driven decision-making.

Feel free to contribute to the project by submitting issues or pull requests on GitHub.