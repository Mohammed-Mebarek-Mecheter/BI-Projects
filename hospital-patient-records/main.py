# main.py
from src.data.load_data import load_data, initial_type_conversion
from src.data.clean_data import clean_encounters, clean_patients, clean_procedures, clean_payers, clean_organizations
from src.data.process_data import process_data

def main():
    # Load data
    dictionary, encounters, organizations, payers, patients, procedures = load_data()

    # Initial data type conversions
    encounters, patients, procedures, organizations = initial_type_conversion(encounters, patients, procedures, organizations)

    # Clean data
    encounters = clean_encounters(encounters)
    patients = clean_patients(patients)
    procedures = clean_procedures(procedures)
    payers = clean_payers(payers)
    organizations = clean_organizations(organizations)

    # Process data
    processed_data = process_data(encounters, patients, procedures, payers, organizations)

    print("Data processing complete. Processed data saved to data/processed/processed_data.csv")

if __name__ == "__main__":
    main()