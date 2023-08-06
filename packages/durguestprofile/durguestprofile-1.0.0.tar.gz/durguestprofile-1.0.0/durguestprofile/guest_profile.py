
from durguestprofile import properties_score
criteria_file = fr"criteria_mapper.xlsx"
files_folder = fr""
# call the audit function and print the final score
FINAL_AUDIT_DATE = properties_score(files_folder=files_folder, criteria_file=criteria_file)
