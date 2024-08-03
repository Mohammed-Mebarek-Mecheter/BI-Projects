# process_data.py
import pandas as pd
import numpy as np

def process_data(encounters, patients, procedures, payers, organizations):
    # Ensure the ORGANIZATION column is present before merging
    if 'ORGANIZATION' not in encounters.columns:
        encounters['ORGANIZATION'] = 'Unknown'

    # Merge datasets
    data = encounters.merge(patients, left_on='PATIENT', right_on='Id', suffixes=('', '_PATIENT'))
    data = data.merge(procedures, left_on='Id', right_on='ENCOUNTER', suffixes=('', '_PROCEDURE'))
    data = data.merge(payers, left_on='PAYER', right_on='Id', suffixes=('', '_PAYER'))
    data = data.merge(organizations, left_on='ORGANIZATION', right_on='Id', suffixes=('', '_ORG'))

    # Convert 'START' and 'BIRTHDATE' to timezone-naive datetime
    data['START'] = data['START'].dt.tz_localize(None)
    data['BIRTHDATE'] = data['BIRTHDATE'].dt.tz_localize(None)

    # Calculate derived features
    data['AGE_AT_ENCOUNTER'] = (data['START'] - data['BIRTHDATE']).dt.total_seconds() / (3600*24*365.25)
    data['INSURANCE_COVERAGE'] = (data['PAYER_COVERAGE'] / data['TOTAL_CLAIM_COST'] * 100).clip(0, 100)
    data['READMISSION'] = data.duplicated(subset=['PATIENT'], keep=False).astype(int)

    # Handle outliers in numerical columns
    numerical_columns = ['DURATION', 'TOTAL_CLAIM_COST', 'PAYER_COVERAGE', 'BASE_ENCOUNTER_COST', 'AGE_AT_ENCOUNTER']
    for col in numerical_columns:
        data[col] = data[col].clip(lower=data[col].quantile(0.01), upper=data[col].quantile(0.99))

    # Ensure proper data types
    data['COVERED_BY_INSURANCE'] = data['PAYER_COVERAGE'].notna()
    data['ZIP'] = data['ZIP'].fillna(np.nan).astype(str)
    data['READMISSION'] = data['READMISSION'].astype(int)

    # Handle missing values in INSURANCE_COVERAGE
    data['INSURANCE_COVERAGE'] = data['INSURANCE_COVERAGE'].fillna(data['INSURANCE_COVERAGE'].median())

    # Save processed data
    data.to_csv("data/processed/processed_data.csv", index=False)

    return data