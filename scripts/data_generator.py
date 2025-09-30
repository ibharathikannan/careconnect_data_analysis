import pandas as pd 
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# --- Configuration ---
NUM_RECORDS = 2000
OUTPUT_CSV_PATH = 'data/raw/visits.csv'

# --- Initialize Faker ---
fake = Faker()

# --- Lists with potential typos ---
SERVICE_TYPES = [
    "Medication Administration", "Medication Administration", "Medication Administrtion",
    "Wound Care", "Wound Care", "WoundCare",
    "Physical Therapy", "Physical Therapy", "Physiotherapy",
    "General Check-up", "General Check-up", "General Checkup",
    "IV Therapy"
]
VISIT_LOCATIONS = ["North", "South", "East", "West", "Noth", "Suth", "Est", "Wst"]

# --- Data Generation Functions ---

def generate_visit_ids(n):
    """Generates a list of visit IDs with some duplicates."""
    visit_ids = [f"v{1000 + i}" for i in range(n)]
    # Introduce duplicates
    for _ in range(int(n * 0.05)): # 5% duplicates
        dup_index = random.randint(0, n - 1)
        original_index = random.randint(0, n - 1)
        if dup_index != original_index:
            visit_ids[dup_index] = visit_ids[original_index]
    return visit_ids

def generate_timestamps(n):
    """Generates start and end timestamps with outliers and inconsistent formats."""
    start_times = []
    end_times = []
    
    date_formats = [
        '%Y-%m-%d %H:%M:%S',
        '%m/%d/%Y %I:%M %p',
        '%d-%b-%Y %H:%M',
        'ISO8601',
        'unix_time'
    ]

    for i in range(n):
        # Generate base start time
        start_time = fake.date_time_between(start_date='-1y', end_date='now')
        
        # Default visit duration
        duration_minutes = random.randint(20, 90)
        
        # Introduce outliers
        if i % 50 == 0: # Unusually long visit
            duration_minutes = random.randint(300, 600)
        elif i % 30 == 0: # Unusually short visit
            duration_minutes = random.randint(1, 5)
            
        end_time = start_time + timedelta(minutes=duration_minutes)

        # Apply inconsistent formatting
        chosen_format = random.choice(date_formats)
        
        if chosen_format == 'ISO8601':
            start_times.append(start_time.isoformat())
            end_times.append(end_time.isoformat())
        elif chosen_format == 'unix_time':
            start_times.append(int(start_time.timestamp()))
            end_times.append(int(end_time.timestamp()))
        else:
            start_times.append(start_time.strftime(chosen_format))
            end_times.append(end_time.strftime(chosen_format))
            
    return start_times, end_times

def generate_notes(n):
    """Generates nurse notes with noise and missing values."""
    notes = []
    for _ in range(n):
        if random.random() < 0.7: # 70% chance of having a note
            note = fake.sentence(nb_words=15)
            # Add noise
            if random.random() < 0.3:
                note += f" PATIENT_TEMP={random.uniform(97.0, 102.0):.1f}F BP={random.randint(110, 140)}/{random.randint(70, 90)} "
            if random.random() < 0.2:
                note = f"***CHECK THIS*** {note} !!!"
            notes.append(note)
        else:
            notes.append(None) # Missing note
    return notes

# --- Main Data Generation Logic ---
def generate_dataset(num_records):
    """Generates the full dataset and saves it to a CSV file."""
    
    # Generate base columns
    visit_ids = generate_visit_ids(num_records)
    patient_ids = [f"p{random.randint(100, 100 + int(num_records/4))}" for _ in range(num_records)]
    nurse_ids = [f"n{random.randint(20, 30)}" for _ in range(num_records)]
    start_times, end_times = generate_timestamps(num_records)
    service_types = [random.choice(SERVICE_TYPES) for _ in range(num_records)]
    visit_locations = [random.choice(VISIT_LOCATIONS) for _ in range(num_records)]
    nurse_notes = generate_notes(num_records)

    # Create DataFrame
    df = pd.DataFrame({
        'visit_id': visit_ids,
        'patient_id': patient_ids,
        'nurse_id': nurse_ids,
        'visit_start_time': start_times,
        'visit_end_time': end_times,
        'service_type': service_types,
        'visit_location': visit_locations,
        'nurse_notes': nurse_notes
    })

    # Introduce missing visit_end_time
    missing_end_time_indices = df.sample(frac=0.1).index # 10% missing
    df.loc[missing_end_time_indices, 'visit_end_time'] = np.nan
    
    # Ensure duplicates are not just copies but have some variation
    dup_ids = df[df.duplicated(subset=['visit_id'], keep=False)]['visit_id'].unique()
    for vid in dup_ids:
        dup_rows = df[df['visit_id'] == vid]
        if len(dup_rows) > 1:
            # Slightly alter one of the duplicated rows to make it more realistic
            index_to_change = dup_rows.index[1]
            df.loc[index_to_change, 'nurse_notes'] = "DUPLICATE ENTRY - PLEASE VERIFY"
            df.loc[index_to_change, 'service_type'] = "Unknown"

    # Create directories if they don't exist
    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)

    # Save to CSV
    df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Successfully generated '{OUTPUT_CSV_PATH}' with {len(df)} records.")

if __name__ == '__main__':
    generate_dataset(NUM_RECORDS)