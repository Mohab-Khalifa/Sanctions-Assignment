import pandas as pd

pd.set_option('display.max_columns', None)

# Load dataset
def load_data(file_path):
    return pd.read_csv(file_path)

# Load list of countries from a text file
def load_countries(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        return [line.strip() for line in file if line.strip()]
    
def remove_duplicates(df):
    return df.drop_duplicates(keep='first')

# Create 'Full Name' from name parts
def create_full_name(df):
    name_cols = ['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5', 'Name 6']
    df['Full Name'] = df[name_cols].fillna('').apply(lambda row: ' '.join(row).strip(), axis=1)
    df['Full Name'] = df['Full Name'].str.replace(r'\s+', ' ', regex=True)
    return df

# Clean DOB column: replace '00' with '01' and standardize format
def clean_dob(df):
    def standardize_dob(dob):
        if pd.isna(dob) or str(dob).strip() == "":
            return pd.NA
        try:
            parts = str(dob).replace('-', '/').strip().split('/')
            if len(parts) != 3:
                return pd.NA
            day = parts[0] if parts[0] != "00" else "01"
            month = parts[1] if parts[1] != "00" else "01"
            year = parts[2]
            return f"{day.zfill(2)}-{month.zfill(2)}-{year}"
        except:
            return pd.NA

    df['DOB'] = df['DOB'].apply(standardize_dob)
    return df

# Combine all address fields into one full address
def create_full_address(df):
    address_cols = ['Address 1', 'Address 2', 'Address 3', 'Address 4', 'Address 5', 'Address 6']
    df['Full Address'] = df[address_cols].fillna('').apply(
        lambda row: ', '.join([x for x in row if x.strip() != '']), axis=1
    )
    return df

# Match country names across specified columns and build 'Associated Countries'
def map_associated_countries(df, countries):
    columns_to_check = ['Country of Birth', 'Nationality', 'Country', 'Other Information', 'Regime']

    def extract_countries(row):
        found = set()
        for col in columns_to_check:
            if col in df.columns and pd.notna(row[col]):
                text = str(row[col]).lower()
                for country in countries:
                    if country.lower() in text:
                        found.add(country)
        return ', '.join(sorted(found)) if found else pd.NA

    df['Associated Countries'] = df.apply(extract_countries, axis=1)
    return df

def clean_non_english_characters(df, replace_with=''):
    """
    Removes non-ASCII characters from all object columns in the DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        replace_with (str): Character(s) to replace non-ASCII characters with. Default is '' (remove them).

    Returns:
        pd.DataFrame: A cleaned DataFrame with non-ASCII characters removed or replaced.
    """
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(
                lambda x: ''.join(c if c.isascii() else replace_with for c in str(x)) if pd.notna(x) else x
            )
    return df

def data_quality_report(df_before, df_after):
    def summarize(df, label):
        print(f"\n📋 Data Quality Summary: {label}")
        print(f"→ Shape: {df.shape[0]} rows × {df.shape[1]} columns")

        # Overall missing value count
        total_missing = df.isna().sum().sum()
        print(f"→ Total missing values: {total_missing}")

        # 1. Missing fields
        missing = df.isna().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            print("→ Missing fields:")
            for col, count in missing.items():
                print(f"   - {col}: {count} missing")
        else:
            print("→ No missing values detected.")

        # 2. Duplicate records
        duplicate_count = df.duplicated().sum()
        print(f"→ Duplicate rows: {duplicate_count}")

        # 3. Blank or unnamed entries 
        if 'Full Name' in df.columns:
            blank_names = df['Full Name'].apply(lambda x: str(x).strip() == '').sum()
            print(f"→ Blank 'Full Name' entries: {blank_names}")

        # 4. DOB format check 
        if 'DOB' in df.columns:
            suspicious_dobs = df['DOB'].apply(lambda x: isinstance(x, str) and ('00' in x or len(x) < 8)).sum()
            print(f"→ Suspected invalid DOBs: {suspicious_dobs}")

        # 5. Optional: Check for missing 'Associated Countries'
        if 'Associated Countries' in df.columns:
            no_country = df['Associated Countries'].isna().sum()
            print(f"→ Rows with no Associated Countries: {no_country}")

         # 6. Non-English character detection
        print("→ Columns with non-English (non-ASCII) characters:")
        non_ascii_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':
                if df[col].dropna().apply(lambda x: not str(x).isascii()).any():
                    non_ascii_columns.append(col)
        if non_ascii_columns:
            for col in non_ascii_columns:
                print(f"   - {col}")
        else:
            print("   None detected.")

    # Run summary for both versions
    summarize(df_before, "Before Cleaning")
    summarize(df_after, "After Cleaning")

def save_data(df, output_file):
    df.to_csv(output_file, index=False)



# MAIN EXECUTION
def main():
    # Load data
    df = load_data('Sanctions-Assignment/data/raw/ConList.csv')

    df_original = df.copy()

    # Clean non-English before cleaning
    df = clean_non_english_characters(df)

    # Load country list
    print("Loading countries...")
    countries = load_countries('Sanctions-Assignment/data/countries.txt')
    print("Countries loaded:", countries[:10])

    # Clean and transform data
    df = create_full_name(df)
    df = clean_dob(df)
    df = map_associated_countries(df, countries)
    df = create_full_address(df)

    # Final selection of columns
    columns_to_keep = [
        'Full Name', 'DOB', 'Town of Birth', 'Associated Countries',
        'Passport Number', 'National Identification Number', 'Position',
        'Full Address', 'Other Information', 'Group Type', 'Group ID'
    ]
    df_cleaned = df[columns_to_keep]
    df_cleaned = remove_duplicates(df_cleaned)

    # Preview cleaned output
    print("\n Final cleaned data sample:")
    print(df_cleaned.head(20))

    # Data quality report
    data_quality_report(df_original, df_cleaned)

    save_data(df_cleaned, "Sanctions-Assignment/data/output/sanctions_cleaned.csv")
    print("Cleaned data saved to: Sanctions-Assignment/data/output/sanctions.csv")




# Run the script
if __name__ == '__main__':
    main()