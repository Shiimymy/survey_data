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
    new_name = input('Enter the employee name:')
    new_survey.append(new_name)
    new_nps = input('Enter a number between 0 and 10:')
    new_survey.append(int(new_nps))
    new_resolve = input("Enter 'yes', 'no' or 'I don't know':\n")
    new_survey.append(new_resolve)
    
    validate_data(new_survey)


def validate_data(values):
    """
    Check if the 3 datas provided by the user are valid.
    """
    
    if (values[0]).isalpha():
        print("Valid name")

        if 0 <= values[1] <= 10:
            print("Valid NPS")
            
            if values[2] == "yes":
                return values
            elif values[2] == "no":
                return values
            elif values[2] == "I don't know":
                return values
            else:
                print("The input can only be 'yes', 'no' or 'I don't know'\n")
                get_new_survey_data()

        else:
            print("The NPS should be a number between 0 and 10\n")
            get_new_survey_data()

    else:
        print("Please enter a name with only letters from the alphabet\n")
        get_new_survey_data()
        

get_new_survey_data()