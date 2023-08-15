import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('survey_data')

survey = SHEET.worksheet('survey')
data = survey.get_all_values()
print(data)


def get_new_survey_data():
    """
    Get a new survey data with 3 information from the user.
    The first should be a employee name
    The second a number between 0 and 10
    The last a 3 options string.
    """
    new_survey = []

    print('Please enter the results of the new survey\n')
    new_name = input('Enter the employee name: \n')
    new_survey.append(new_name)
    new_nps = input('Enter a number between 0 and 10: \n')
    new_survey.append(new_nps)
    new_resolve = input("Enter 'yes', 'no' or 'I don't know': \n")
    new_survey.append(new_resolve)

    print(f"The data from the surrvey is:{new_survey}")


get_new_survey_data()

