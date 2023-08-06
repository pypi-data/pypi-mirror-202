from durguestprofile import properties_score
import os

# Define the directory where the text or xml files are located,
# the same folder should contain criteria_mapper.xlsx file
files_path = r"C:\Users\user\Desktop\Dur\testfiles"
data_source = properties_score(
    files_folder=files_path, 
    criteria_file=os.path.join(files_path, "criteria_mapper.xlsx")
    )
print(data_source)