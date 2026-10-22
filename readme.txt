P14 - HOSPITAL PATIENT RECORDS
AIXcelerate Python Projects Level 
=====================================

OVERVIEW
--------
A terminal-based Python 3 application to register patients, record visits,
view patient history, search records and generate reports. Data is stored in
plain text files with fields separated by '|'. The program runs until the
user selects 0 (Exit).

FILES
-----
hospital_records.py  - the program (core Python only, no import statements)
patients.txt         - patient records (12 sample patients)
visits.txt           - visit records (26 sample visits)
sample_run.txt       - actual terminal output captured from a run
README.txt           - this file

HOW TO RUN
----------
1. Keep all files in the same folder.
2. Open a terminal in that folder.
3. Run:  python hospital_records.py   (or python3 hospital_records.py)

MENU OPTIONS
------------
1. Register patient   - auto-generates ID (P0001, P0002, ...); stores name,
                        age, gender, phone, blood group.
2. Record visit       - patient ID, date, doctor, symptoms, diagnosis, fee.
3. Patient history    - all visits, total visits and total fees.
4. Search patients    - by patient ID, partial name or phone number.
5. Doctor-wise report - patients seen, visits and fees per doctor.
6. Patient statistics - patients with more than 3 visits; patients per
                        blood group.
7. Monthly report     - (bonus) visits and fees for each month.
0. Exit

FILE FORMATS
------------
patients.txt : ID|Name|Age|Gender|Phone|BloodGroup
visits.txt   : PatientID|Date|Doctor|Symptoms|Diagnosis|Fee
Dates use DD-MM-YYYY. Blood groups: A+, A-, B+, B-, AB+, AB-, O+, O-.

VALIDATION
----------
- Empty inputs are rejected.
- The '|' character is rejected in all text fields.
- Age must be 0-120; gender M/F/O; phone exactly 10 digits.
- Blood group must be one of the allowed values.
- Dates are checked for format, month length and leap years.
- Fee must be a whole number (0-100000).
- Visits can only be recorded for existing patient IDs.
- Menu choices outside 0-7 or non-numeric are rejected.
- Missing data files are handled with FileNotFoundError (the program starts
  with no records and creates the file, with header, when data is saved).

NOTES
-----
sample_run.txt was captured from a real run starting with the supplied
patients.txt and visits.txt. It registered P0013 and recorded one visit.
Re-run the program and update sample_run.txt whenever the code changes.