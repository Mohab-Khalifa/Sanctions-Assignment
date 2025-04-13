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

## 🚀 Setup 

### 1. Clone 

```bash
git clone https://github.com/Mohab-Khalifa/Sanctions-Assignment.git
```

### 2. cd into the project folder

### 3. Create a virtual environment, activate it and then install dependencies
On macOS and Linux
```bash
python -m venv venv
source env/bin/activate
pip install -r requirements.txt
```

On Windows
```bash
python -m venv venv
env\Scripts\activate
pip install -r requirements.txt
```