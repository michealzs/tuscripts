from bs4 import BeautifulSoup
import requests
import pandas as pd 
import json
import os

#os.chdir("E:/Work Files")
#url = 'https://go.careacademy.com/agencies/3278/compliance_report'
url = "https://go.careacademy.com/api/agencies/3278/"
auth=('###', '###')
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
page = requests.get(url, auth=auth, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')
print(soup)
#report = soup.find("script", attrs={"id": "compliance_report_vue_config"})
report = soup.find("script", attrs={"id": "administrator_dashboard_vue_config"})
report = soup.find("script", attrs={"id": "administrator_dashboard_vue_config"})
#
string_report = str(report.string) 
report_dump = json.dumps(string_report) 
json_report = json.loads(string_report)
dict_json = dict(json_report)  #  Result of dict_json.keys() -> 'twilio_success_code', 'incomplete_course_status', 'complete_course_status', 'caregiver
cur_caregivers = dict_json.get("caregiver_list", "Does not exist Currently")    #  Returns a list
#insightly = pd.read_csv('insight.csv')
#insightly_dic = insightly.to_dict('index')
#insightly_names = []
carecad_caregivers = {}
carecad = []
emails = {}
csv = []
ucsv = []

print(cur_caregivers)
for x in cur_caregivers:
    print('Full name : ', x['first_name'], x['last_name'])
    print('Phone Number : ', x['phone_number'])
    if x['initial_completed'] < x['total_initial']:
        print('Training Not Completed')
        status = 'Training Not Completed'
    elif x['initial_completed'] == x['total_initial']: 
        print('Training Completed')
        status = 'Training Completed'
    else: 
        print('Error Occured')
    print('Classes : ', x['initial_completed'] ,' of ', x['total_initial'], 'Done' )
    print('*'*50)
    name = x['last_name'].strip() + " " + x['first_name'].strip() 
    carecad_caregivers[name] = status 
    carecad.append(name.lower())
##print(carecad_caregivers)
carecad_set = set(carecad)

'''
for names in insightly_dic.values():
    #pprint(names)
    first_name = names['First Name'].strip()
    last_name = names['Last Name'].strip()
    name = f'{last_name} {first_name}'
    lower_name = name.lower()
    emails[lower_name] = names['Email Address']
    insightly_names.append(lower_name)
insightly_set = set(insightly_names)

diff = insightly_set.symmetric_difference(carecad_set)
#print(diff)
#for x in sorted(diff):
    #print(x)
'''
    
for x in carecad_caregivers:
    y = x.lower()
    if y:
        gemail = emails.get(y,'Where at')
        #print('#'*100)
        print(y , gemail)
        csv.append(f'{y}, {gemail}')
        f = open("carecad_emails.csv", "w")
        for x in csv:
            f.write(f'\n {x}')
        f.close()

    if y in emails and carecad_caregivers.get(y.title(),'Does Not Exsist') == 'Training Completed':
        gemail = emails.get(y,'Where at')
        #print('#'*100)
        print(y , gemail)
        csv.append(f'{y}, {gemail}')
        f = open("completed_carecad.csv", "w")
        for x in csv:
            f.write(f'\n {x}')
        f.close()

    if y in emails and carecad_caregivers.get(y.title(),'Does Not Exsist') == 'Training Not Completed':
        gemail = emails.get(y,'Where at')
        #print('#'*100)
        print(y , gemail)
        ucsv.append(f'{y}, {gemail}')
        f = open("uncompleted_carecad.csv", "w")
        for x in ucsv:
            f.write(f'\n {x}')
        f.close()

print(str(csv))
