# Data Directory

This directory should contain the UIDAI Aadhaar datasets.

## Required Files

Place the following CSV files in this directory:

### Enrolment Data
- `api_data_aadhar_enrolment_0_500000.csv`
- `api_data_aadhar_enrolment_500000_1000000.csv`
- `api_data_aadhar_enrolment_1000000_1006029.csv`

### Demographic Update Data
- `api_data_aadhar_demographic_0_500000.csv`
- `api_data_aadhar_demographic_500000_1000000.csv`
- `api_data_aadhar_demographic_1000000_1500000.csv`
- `api_data_aadhar_demographic_1500000_2000000.csv`
- `api_data_aadhar_demographic_2000000_2071700.csv`

### Biometric Update Data
- `api_data_aadhar_biometric_0_500000.csv`
- `api_data_aadhar_biometric_500000_1000000.csv`
- `api_data_aadhar_biometric_1000000_1500000.csv`
- `api_data_aadhar_biometric_1500000_1861108.csv`

## Data Schema

### Enrolment Dataset
| Column | Description |
|--------|-------------|
| date | Date of enrolment (DD-MM-YYYY) |
| state | State name |
| district | District name |
| pincode | 6-digit pincode |
| age_0_5 | Count of enrolments for age 0-5 |
| age_5_17 | Count of enrolments for age 5-17 |
| age_18_greater | Count of enrolments for age 18+ |

### Demographic Update Dataset
| Column | Description |
|--------|-------------|
| date | Date of update (DD-MM-YYYY) |
| state | State name |
| district | District name |
| pincode | 6-digit pincode |
| demo_age_5_17 | Count of updates for age 5-17 |
| demo_age_17_ | Count of updates for age 17+ |

### Biometric Update Dataset
| Column | Description |
|--------|-------------|
| date | Date of update (DD-MM-YYYY) |
| state | State name |
| district | District name |
| pincode | 6-digit pincode |
| bio_age_5_17 | Count of updates for age 5-17 |
| bio_age_17_ | Count of updates for age 17+ |

## Note

The actual data files are not included in this repository as they are proprietary datasets provided by UIDAI for the hackathon. Participants should download the data from the official UIDAI hackathon portal.
