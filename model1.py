import pandas as pd

# Load the data from a CSV file
# The CSV should have columns: Name, EXP, YOS_EXP, Performance, Salary, Position
file_path = "employee_data.csv"  # Specify your CSV file path here
df = pd.read_csv(file_path)


# Define performance weights
def get_performance_weight(perf):
    if perf == "Exceeds":
        return 1.2
    else:
        return 1.0


df['Perf_Weight'] = df['Performance'].apply(get_performance_weight)


# Base increment percentage
def get_base_increment(row):
    # Interns (EXP == YOS_EXP) or lateral entry (lower package and more YOS_EXP)
    if row['EXP'] == row['YOS_EXP'] or row['YOS_EXP'] > row['EXP']:
        return 0.15  # 15% increment for interns or laterals
    return 0.1  # 10% increment for others


df['Base_Increment'] = df.apply(get_base_increment, axis=1)


# Adjusting salary increments based on salary to avoid bias towards higher packages
def calculate_adjusted_salary_v2(row):
    current_salary = row['Salary']
    perf_weight = row['Perf_Weight']
    base_increment = row['Base_Increment']

    # Define midpoint and max salary limits for Sr Software Engineers
    midpoint = 35
    max_salary = 69

    # Calculate base increment as a percentage
    if row['Position'] == "Sr Software Engineer":
        if current_salary < midpoint:
            # Higher percentage increment for salaries below midpoint (20-25%)
            percentage_increment = 0.25
        else:
            # Smaller percentage increment for salaries above midpoint (10-15%)
            percentage_increment = 0.10 if current_salary > midpoint else 0.15
    else:
        # For Lead Engineers or others, apply base increment with a cap for higher packages
        percentage_increment = 0.10 if current_salary >= 50 else 0.20

    # Adjust salary based on the calculated percentage
    adjusted_salary = current_salary + (percentage_increment * current_salary)

    # Ensure salary doesn't exceed the maximum allowed (69 lakhs for Sr Software Engineers)
    if row['Position'] == "Sr Software Engineer":
        adjusted_salary = min(adjusted_salary, max_salary)

    return adjusted_salary, percentage_increment * 100


# Apply the new salary adjustment formula
df['Adjusted_Salary'], df['Percentage_Increment'] = zip(*df.apply(calculate_adjusted_salary_v2, axis=1))

# Save the updated DataFrame with percentage increments to an Excel file
final_file_path = "final_adjusted_employee_salary_data_from_csv.xlsx"
df.to_csv(final_file_path, index=False)

print(f"Adjusted salary data has been saved to {final_file_path}")
