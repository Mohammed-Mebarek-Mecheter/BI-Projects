# clean_data.py
import pandas as pd
import numpy as np

def clean_encounters(encounters):
    # Calculate encounter duration
    encounters['DURATION'] = (encounters['STOP'] - encounters['START']).dt.total_seconds() / 3600  # duration in hours

    # Handle missing values
    encounters['REASONCODE'] = encounters['REASONCODE'].fillna(-1)
    encounters['REASONDESCRIPTION'] = encounters['REASONDESCRIPTION'].fillna('Unknown')
    encounters['PAYER_COVERAGE'] = encounters['PAYER_COVERAGE'].fillna(encounters['PAYER_COVERAGE'].median())

    # Handle outliers
    encounters['DURATION'] = encounters['DURATION'].clip(lower=0, upper=encounters['DURATION'].quantile(0.99))
    encounters['TOTAL_CLAIM_COST'] = encounters['TOTAL_CLAIM_COST'].clip(lower=0, upper=encounters['TOTAL_CLAIM_COST'].quantile(0.99))

    # Drop irrelevant columns
    columns_to_drop = ['REASONCODE', 'REASONDESCRIPTION']
    encounters = encounters.drop(columns=columns_to_drop)

    return encounters

def clean_patients(patients):
    # Handle missing values
    patients['DEATHDATE'] = patients['DEATHDATE'].fillna(pd.NaT)
    patients['MAIDEN'] = patients['MAIDEN'].fillna('')
    patients['SUFFIX'] = patients['SUFFIX'].fillna('')
    patients['ZIP'] = patients['ZIP'].fillna(np.nan)
    patients['MARITAL'] = patients['MARITAL'].fillna('Unknown')

    # Drop irrelevant columns
    columns_to_drop = ['PREFIX', 'SUFFIX', 'MAIDEN']
    patients = patients.drop(columns=columns_to_drop)

    return patients

def clean_procedures(procedures):
    # Drop irrelevant columns
    columns_to_drop = ['REASONCODE', 'REASONDESCRIPTION']
    procedures = procedures.drop(columns=columns_to_drop)

    return procedures

def clean_payers(payers):
    # Handle missing values
    payers = payers.fillna('Unknown')

    # Drop irrelevant columns
    columns_to_drop = ['ADDRESS', 'CITY', 'STATE_HEADQUARTERED', 'ZIP', 'PHONE']
    payers = payers.drop(columns=columns_to_drop)

    return payers

def clean_organizations(organizations):
    # No irrelevant columns to drop based on requirements
    return organizations