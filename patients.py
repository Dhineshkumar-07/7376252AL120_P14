PATIENT_FILE = "patients.txt"
VISIT_FILE = "visits.txt"
PATIENT_HEADER = "ID|Name|Age|Gender|Phone|BloodGroup"
VISIT_HEADER = "PatientID|Date|Doctor|Symptoms|Diagnosis|Fee"
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# File handling
def load_records(filename, field_count):
    """Read a '|' separated file and return a list of field lists."""
    records = []
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Note: '" + filename + "' not found. Starting with no records.")
        return records
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        parts = line.split("|")
        if parts[0] in ("ID", "PatientID"): 
            continue
        if len(parts) != field_count:  
            continue
        records.append(parts)
    return records


def load_patients():
    return load_records(PATIENT_FILE, 6)


def load_visits():
    return load_records(VISIT_FILE, 6)


def append_record(filename, header, fields):
    """Append one record; create the file with a header if it is missing."""
    try:
        open(filename, "r").close()
        exists = True
    except FileNotFoundError:
        exists = False
    with open(filename, "a") as f:
        if not exists:
            f.write(header + "\n")
        f.write("|".join(fields) + "\n")


# ---------------------------------------------------------------
# Input validation helpers
# ---------------------------------------------------------------
def get_text(prompt):
    """Non-empty text that does not contain the '|' separator."""
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Error: input cannot be empty.")
        elif "|" in value:
            print("Error: the '|' character is not allowed.")
        else:
            return value


def get_int(prompt, low, high):
    while True:
        value = get_text(prompt)
        if not value.isdigit():
            print("Error: please enter a whole number.")
            continue
        number = int(value)
        if number < low or number > high:
            print("Error: value must be between " + str(low) + " and " + str(high) + ".")
            continue
        return number


def get_gender():
    while True:
        value = get_text("Gender (M/F/O): ").upper()
        if value in ("M", "F", "O"):
            return value
        print("Error: enter M, F or O.")


def get_phone():
    while True:
        value = get_text("Phone (10 digits): ")
        if value.isdigit() and len(value) == 10:
            return value
        print("Error: phone must be exactly 10 digits.")


def get_blood_group():
    while True:
        value = get_text("Blood group (" + ", ".join(BLOOD_GROUPS) + "): ").upper()
        if value in BLOOD_GROUPS:
            return value
        print("Error: invalid blood group.")


def is_valid_date(text):
    """Check DD-MM-YYYY, including leap years, without any imports."""
    parts = text.split("-")
    if len(parts) != 3:
        return False
    d, m, y = parts
    if not (d.isdigit() and m.isdigit() and y.isdigit()):
        return False
    if len(d) != 2 or len(m) != 2 or len(y) != 4:
        return False
    d, m, y = int(d), int(m), int(y)
    if y < 1900 or y > 2100 or m < 1 or m > 12:
        return False
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
        days[1] = 29
    return 1 <= d <= days[m - 1]


def get_date():
    while True:
        value = get_text("Visit date (DD-MM-YYYY): ")
        if is_valid_date(value):
            return value
        print("Error: invalid date. Use DD-MM-YYYY (e.g. 11-10-2026).")


def find_patient(patient_id, patients):
    for p in patients:
        if p[0] == patient_id:
            return p
    return None


def next_patient_id(patients):
    highest = 0
    for p in patients:
        digits = p[0][1:]
        if digits.isdigit() and int(digits) > highest:
            highest = int(digits)
    return "P" + str(highest + 1).zfill(4)


def fee_total(visits):
    total = 0
    for v in visits:
        if v[5].isdigit():
            total += int(v[5])
    return total


# ---------------------------------------------------------------
# Menu option functions
# ---------------------------------------------------------------
def register_patient():
    print("\n--- Register Patient ---")
    patients = load_patients()
    pid = next_patient_id(patients)
    name = get_text("Name: ")
    age = get_int("Age (0-120): ", 0, 120)
    gender = get_gender()
    phone = get_phone()
    blood = get_blood_group()
    append_record(PATIENT_FILE, PATIENT_HEADER,
                  [pid, name, str(age), gender, phone, blood])
    print("Patient registered successfully. Patient ID: " + pid)


def record_visit():
    print("\n--- Record Visit ---")
    patients = load_patients()
    while True:
        pid = get_text("Patient ID: ").upper()
        patient = find_patient(pid, patients)
        if patient is not None:
            break
        print("Error: patient ID not found.")
    print("Patient: " + patient[1])
    date = get_date()
    doctor = get_text("Doctor: ")
    symptoms = get_text("Symptoms: ")
    diagnosis = get_text("Diagnosis: ")
    fee = get_int("Fee (Rs.): ", 0, 100000)
    append_record(VISIT_FILE, VISIT_HEADER,
                  [pid, date, doctor, symptoms, diagnosis, str(fee)])
    print("Visit recorded successfully.")


def patient_history():
    print("\n--- Patient History ---")
    patients = load_patients()
    visits = load_visits()
    pid = get_text("Patient ID: ").upper()
    patient = find_patient(pid, patients)
    if patient is None:
        print("Patient not found.")
        return
    print("\n" + patient[0] + " | " + patient[1] + " | Age " + patient[2] +
          " | " + patient[3] + " | " + patient[4] + " | " + patient[5])
    mine = [v for v in visits if v[0] == pid]
    if len(mine) == 0:
        print("No visits recorded for this patient.")
        return
    print("\n" + "Date".ljust(12) + "Doctor".ljust(14) + "Symptoms".ljust(20) +
          "Diagnosis".ljust(24) + "Fee")
    print("-" * 76)
    for v in mine:
        print(v[1].ljust(12) + v[2].ljust(14) + v[3].ljust(20) +
              v[4].ljust(24) + v[5])
    print("-" * 76)
    print("Total visits: " + str(len(mine)))
    print("Total fees  : Rs. " + str(fee_total(mine)))


def search_patients():
    print("\n--- Search Patients ---")
    patients = load_patients()
    query = get_text("Enter patient ID, part of name, or phone number: ").lower()
    matches = []
    for p in patients:
        if p[0].lower() == query or query in p[1].lower() or query in p[4]:
            matches.append(p)
    if len(matches) == 0:
        print("No matching patients found.")
        return
    print("\n" + "ID".ljust(8) + "Name".ljust(16) + "Age".ljust(6) +
          "Gender".ljust(8) + "Phone".ljust(13) + "Blood")
    print("-" * 56)
    for p in matches:
        print(p[0].ljust(8) + p[1].ljust(16) + p[2].ljust(6) +
              p[3].ljust(8) + p[4].ljust(13) + p[5])
    print(str(len(matches)) + " patient(s) found.")


def doctor_report():
    print("\n--- Doctor-wise Report ---")
    visits = load_visits()
    if len(visits) == 0:
        print("No visit records available.")
        return
    seen = {}
    fees = {}
    counts = {}
    for v in visits:
        doc = v[2]
        if doc not in seen:
            seen[doc] = []
            fees[doc] = 0
            counts[doc] = 0
        if v[0] not in seen[doc]:
            seen[doc].append(v[0])
        counts[doc] += 1
        if v[5].isdigit():
            fees[doc] += int(v[5])
    print("\n" + "Doctor".ljust(16) + "Patients Seen".ljust(16) +
          "Visits".ljust(10) + "Fees Collected")
    print("-" * 56)
    for doc in sorted(seen):
        print(doc.ljust(16) + str(len(seen[doc])).ljust(16) +
              str(counts[doc]).ljust(10) + "Rs. " + str(fees[doc]))


def patient_statistics():
    print("\n--- Patient Statistics ---")
    patients = load_patients()
    visits = load_visits()
    print("Patients with more than 3 visits:")
    found = False
    for p in patients:
        count = len([v for v in visits if v[0] == p[0]])
        if count > 3:
            print("  " + p[0] + "  " + p[1].ljust(14) + str(count) + " visits")
            found = True
    if not found:
        print("  None")
    print("\nPatients per blood group:")
    for bg in BLOOD_GROUPS:
        count = len([p for p in patients if p[5] == bg])
        print("  " + bg.ljust(4) + ": " + str(count))


def monthly_report():
    """Bonus: number of visits and fees collected for each month."""
    print("\n--- Monthly Report (Bonus) ---")
    visits = load_visits()
    if len(visits) == 0:
        print("No visit records available.")
        return
    months = {}
    for v in visits:
        key = v[1][3:]  # MM-YYYY
        if key not in months:
            months[key] = [0, 0]
        months[key][0] += 1
        if v[5].isdigit():
            months[key][1] += int(v[5])
    ordered = sorted(months, key=lambda k: (k[3:], k[:2]))
    print("\n" + "Month".ljust(12) + "Visits".ljust(10) + "Fees Collected")
    print("-" * 36)
    for key in ordered:
        print(key.ljust(12) + str(months[key][0]).ljust(10) +
              "Rs. " + str(months[key][1]))


# ---------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------
def show_menu():
    print("\n==========================================")
    print("      HOSPITAL PATIENT RECORDS SYSTEM")
    print("==========================================")
    print("1. Register patient")
    print("2. Record visit")
    print("3. Patient history")
    print("4. Search patients")
    print("5. Doctor-wise report")
    print("6. Patient statistics")
    print("7. Monthly report (bonus)")
    print("0. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (0-7): ").strip()
        if choice == "":
            print("Error: choice cannot be empty.")
        elif not choice.isdigit() or int(choice) > 7:
            print("Error: invalid choice. Please enter a number from 0 to 7.")
        elif choice == "1":
            register_patient()
        elif choice == "2":
            record_visit()
        elif choice == "3":
            patient_history()
        elif choice == "4":
            search_patients()
        elif choice == "5":
            doctor_report()
        elif choice == "6":
            patient_statistics()
        elif choice == "7":
            monthly_report()
        elif choice == "0":
            print("\nThank you for using the Hospital Patient Records System. Goodbye!")
            break


main()