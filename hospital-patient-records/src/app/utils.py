import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

def load_data():
    data = pd.read_csv('data/records.csv')
    data['START'] = pd.to_datetime(data['START'])
    data['STOP'] = pd.to_datetime(data['STOP'])
    data['BIRTHDATE'] = pd.to_datetime(data['BIRTHDATE'])  # Ensure BIRTHDATE is in datetime format
    data['ADMISSION_DATE'] = data['START'].dt.date
    data['AGE'] = (data['START'] - data['BIRTHDATE']).dt.days // 365
    return data

def filter_data_by_criteria(data, start_date, end_date, age_group, gender, encounter_class, insurance_provider, readmitted):
    # Convert date inputs to datetime64[ns]
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter by date range
    filtered_data = data[(data['START'] >= start_date) & (data['START'] <= end_date)]

    # Filter by age group
    if age_group != 'All':
        age_ranges = {
            '0-18': (0, 18),
            '19-35': (19, 35),
            '36-50': (36, 50),
            '51-65': (51, 65),
            '66+': (66, 120)
        }
        age_min, age_max = age_ranges[age_group]
        filtered_data = filtered_data[(filtered_data['AGE'] >= age_min) & (filtered_data['AGE'] <= age_max)]

    # Filter by gender
    if gender != 'All':
        filtered_data = filtered_data[filtered_data['GENDER'] == gender]

    # Filter by encounter class
    if encounter_class != 'All':
        filtered_data = filtered_data[filtered_data['ENCOUNTERCLASS'] == encounter_class]

    # Filter by insurance provider
    if insurance_provider != 'All':
        filtered_data = filtered_data[filtered_data['PAYER'] == insurance_provider]

    # Filter by readmitted status
    if readmitted != 'All':
        readmitted_status = {'Yes': 1, 'No': 0}
        filtered_data = filtered_data[filtered_data['READMISSION'] == readmitted_status[readmitted]]

    return filtered_data

def display_aggrid(data, height=400):
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True)
    grid_options = gb.build()
    AgGrid(data, gridOptions=grid_options, height=height, fit_columns_on_grid_load=True)
