import pandas as pd
import json
import requests
import json




login_url = 'http://3.109.5.100/login'
empa_url = 'http://3.109.5.100/empa_register'
empb_url = 'http://3.109.5.100/empb_register'
empc_url = 'http://3.109.5.100/empc_register'
empd_url = 'http://3.109.5.100/empd_register'

data = json.dumps({"email":"admin@mozi.com","password":"admin"})
x = requests.post(login_url, data)
print(x.json())

access_token = x.json()["access_token"]

# Define a sample function to process each employee's data
def process_employee(name, grade, id, email, password):
    # print(f"Processing Employee: Name = {name}, Grade = {grade}, ID = {id}, email = {email}, password = {password}")
    # Your processing logic here, e.g., updating a database or performing calculations
    

    user_data = {"name":name, "mozi_id":str(id), "email":email, "password":str(password)}
    headers = {"Authorization":f"Bearer {access_token}"}

    grade_urls = {
    'Level A': empa_url,
    'Level B': empb_url,
    'Level C': empc_url,
    'Level D': empd_url,
    }


    if grade in grade_urls:
        response = requests.post(grade_urls[grade], headers=headers, data=json.dumps(user_data))
        print(response.text)
    else:
        print(f"Unknown grade: {grade}")

    # if grade == 'Level A':
    #     response = requests.post(empa_url, headers=headers, data=json.dumps(user_data))
    #     print(response.text, f"Processing Employee: Name = {name}, Grade = {grade}, ID = {id}, email = {email}, password = {password}")
    # elif grade == 'Level B':
    #     response = requests.post(empb_url, headers=headers, data=json.dumps(user_data))
    #     print(response.text, f"Processing Employee: Name = {name}, Grade = {grade}, ID = {id}, email = {email}, password = {password}")
    # elif grade == 'Level C':
    #     response = requests.post(empc_url, headers=headers, data=json.dumps(user_data))
    #     print(response.text, f"Processing Employee: Name = {name}, Grade = {grade}, ID = {id}, email = {email}, password = {password}")
    # elif grade == 'Level D':
    #     response = requests.post(empd_url, headers=headers, data=json.dumps(user_data))
    #     print(response.text, f"Processing Employee: Name = {name}, Grade = {grade}, ID = {id}, email = {email}, password = {password}")
    
    

# Read the Excel file into a DataFrame
file_path = "Designation_Employees.xlsx"
data = pd.read_excel(file_path)

# Loop through each row in the DataFrame
for index, row in data.iterrows():
    # Assuming column names are 'Name' and 'Grade' (update as per your file's actual headers)
    
    employee_name = row['Employee Name']
    employee_grade = row['Grade.1']
    if pd.notna(employee_grade):
        employee_grade = f'Level {employee_grade}'
    else:
        employee_grade = 'nan'
    employee_id = row['Employee ID']
    password = employee_id
    email = f"{employee_name.split(' ')[0]}.{employee_name.split(' ')[1][:1]}@mozitronics.com".lower()


    # Call the function with the extracted values
    process_employee(employee_name, employee_grade, employee_id, email, password)
