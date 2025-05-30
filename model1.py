import pandas as pd

Mid-Year Review – Software Engineer

Success and Accomplishments
	•	Successfully led the VFD migration for multiple VIPs with zero issues reported in production, demonstrating attention to detail and strong execution capabilities.
	•	Created comprehensive documentation for the VFD process, enabling team-wide clarity, smoother onboarding, and consistent reference for future efforts.
	•	Designed and implemented automation solutions that enhanced efficiency and reduced manual intervention in recurring workflows, particularly in projects like COP.
	•	Took proactive ownership in identifying and addressing unauthorized traffic, contributing directly to improved production stability and security posture.
	•	Recognized for delivering compliant solutions and maintaining high standards in quality and governance throughout project cycles.

Areas of Focus (Going Forward)
	•	Drive AI adoption initiatives, identifying areas where machine learning or automation can further streamline operations or decision-making.
	•	Develop a plan to integrate AI capabilities in the team’s day-to-day tools or long-term strategy while ensuring alignment with organizational policies and ethics.
	•	Expand cross-team collaboration to share automation best practices and scale successful implementations across other projects.

Risk Overlay
	•	Proactively identified and mitigated production risks related to unauthorized access and traffic, reducing potential exposure and downtime.
	•	Ensured all changes were compliant and secure, with no audit or policy violations during the period under review.
	•	Intend to address AI-related risk overlays (e.g., bias, interpretability, compliance) early in the adoption process to avoid reactive fixes later and maintain regulatory alignment.

Overall Summary

This period has been marked by strong execution, proactive problem-solving, and meaningful contributions to infrastructure stability and team productivity. By successfully handling key technical migrations, introducing automation, and laying the groundwork for AI initiatives, I’ve aimed to align closely with team and organizational goals. The second half of the year will be focused on expanding impact through AI innovation, risk-aware planning, and cross-functional collaboration.

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
