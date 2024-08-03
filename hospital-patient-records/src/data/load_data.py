# load_data.py
import pandas as pd

def load_data():
    # Load all CSV files
    dictionary = pd.read_csv("data/raw/data_dictionary.csv")
    encounters = pd.read_csv("data/raw/encounters.csv")
    organizations = pd.read_csv("data/raw/organizations.csv")
    payers = pd.read_csv("data/raw/payers.csv")
    patients = pd.read_csv("data/raw/patients.csv")
    procedures = pd.read_csv("data/raw/procedures.csv")

    return dictionary, encounters, organizations, payers, patients, procedures

def initial_type_conversion(encounters, patients, procedures, organizations):
    # Convert date columns to datetime
    date_columns = ['START', 'STOP', 'BIRTHDATE', 'DEATHDATE', 'START_PROCEDURE', 'STOP_PROCEDURE']
    for df in [encounters, patients, procedures]:
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce', utc=True).dt.tz_localize(None)

    # Convert numeric columns
    numeric_columns = ['BASE_ENCOUNTER_COST', 'TOTAL_CLAIM_COST', 'PAYER_COVERAGE', 'ZIP', 'LAT', 'LON', 'BASE_COST']
    for df in [encounters, patients, procedures, organizations]:
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

    # Convert boolean columns
    if 'COVERED_BY_INSURANCE' in encounters.columns:
        encounters['COVERED_BY_INSURANCE'] = encounters['COVERED_BY_INSURANCE'].astype('bool')

    return encounters, patients, procedures, organizations