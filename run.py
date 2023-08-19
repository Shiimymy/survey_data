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
    new_survey.append(new_name.capitalize())
    new_nps = input('Enter a number between 0 and 10:')
    new_survey.append(int(new_nps))
    new_resolve = input("Enter 'yes', 'no' or 'i don't know':\n")
    new_survey.append(new_resolve.lower())
    
    validate_data(new_survey)

    return new_survey


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
            elif values[2] == "i don't know":
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
        

def update_survey_worksheet(data):
    """
    Update survey worksheet, add new row with the list data provided by user"
    """
    print(f"Adding {data} to survey worksheet...")
    survey_worksheet = SHEET.worksheet("survey")
    survey_worksheet.append_row(data)
    print("New survey added successfully. \n")


def get_employees():
    """
    Collect employees data to calculate their stats
    """
    survey_worksheet = SHEET.worksheet('survey')
    surveys = survey_worksheet.get_all_values()
    return surveys


def get_average_nps(employee_list):
    """
    Calculate the average NPS of the Team
    """
    total = 0
    for survey in employee_list[1:]:
        total += int(survey[1])
    
    total /= len(employee_list[1:])
    return round(total)


def main():
    """
    Run all program functions.
    """
    new_data = get_new_survey_data()
    update_survey_worksheet(str(new_data))
    employee_list = get_employees()
    average_nps = get_average_nps(employee_list)


main()