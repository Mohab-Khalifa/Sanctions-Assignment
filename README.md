# Sanctions-Assignment
## ⚙️ What It Does

- Cleans non-English characters from the dataset.
- Combines name columns into a single Full Name.
- Standardizes date of birth (DOB), replacing unknown values like "00".
- Combines address fields into a single Full Address.
- Matches known country names in multiple fields and creates an Associated Countries column.
- Generates a before-and-after data quality report.
- Outputs a cleaned CSV file ready for comparison or further use.

---

## 🧪 Columns Retained in Final Output

- Full Name  
- DOB  
- Town of Birth  
- Associated Countries  
- Passport Number  
- National Identification Number  
- Position  
- Full Address  
- Other Information  
- Group Type  
- Group ID

---

## 🧼 Data Quality Checks

The script reports issues such as:

- Missing or blank fields
- Duplicate records
- Suspected invalid DOBs (containing "00")
- Fields with non-English (non-ASCII) characters

## 🚀 How to Run

### 1. Make sure you have Python 3 and pandas installed:

Check Python version:
```bash
python --version

pip install pandas
```

### 2. Set up project structure
Ensure the following file structure exists:

```bash
Sanctions-Assignment/
├── conList.py                  # Main script
├── data/
│   ├── raw/
│   │   └── ConList.csv         # Raw UK sanctions list
│   └── countries.txt           # List of countries (1 per line)
├── data/output/                # (Created automatically for results)
├── README.md
```

### 3. Run the script
From the root directory, run:
```bash
python conList.py
```

### 4. Output
The cleaned dataset will be saved to:

```bash
data/output/sanctions_cleaned.csv
```
