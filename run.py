import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

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
    new_name = input('Enter the employee name:\n')
    new_survey.append(new_name.capitalize())
    # bug to fix : add ValueError exception
    new_nps = input('Enter a number between 0 and 10:\n')
    new_survey.append(int(new_nps))
    print("How the customers reponded to : Did you issue was resolved?")
    new_resolve = input("Enter 'yes', 'no' or 'i don't know':\n")
    new_survey.append(new_resolve.lower())
    
    validate_data(new_survey)

    return new_survey


def validate_data(values):
    """
    Check if the 3 datas provided by the user are valid.
    """
    # bug to fix : doesn't get new value to worksheet
    if (values[0]).isalpha():
        print("Valid name")
        # new function 

        if 0 <= values[1] <= 10:
            print("Valid NPS")
            # new function
            if values[2] == "yes":
                # new function after user input
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


def calculate_resolution_percentage(employee_list):
    """
    Calculate the percentage of survey with resolved issue
    """
    count_yes = 0

    for x in employee_list[1:]:
        count_yes += x[2].count('yes')
    
    percentage_yes = ((count_yes*100)/len(employee_list[1:]))
    return round(percentage_yes)


def identify_leader_meeting(nps, resolution):
    """
    Identify if the Team Leader would need to organise a meeting
    to improve Team performances.
    """
    meeting_action = 5 <= nps <= 7 or 55 <= resolution <= 75

    if meeting_action:
        meeting = "Meeting"
        return meeting
    else:
        no_action = ""
        return no_action


def identify_leader_training(nps, resolution):
    """
    Identify if the Team Leader would need to organise a training
    to improve Team performances.
    """
    training_action = nps < 5 and resolution < 55

    if training_action:
        training = "Training"
        return training
    else:
        no_action = ""
        return no_action


def get_leader_action(meeting, training):
    if not (meeting or training):
        no_action = "None"
        return no_action
    else: 
        return f"{meeting}{training}"


def get_date():
    """
    Get the date from the datetime library and return it
    """
    date = datetime.now().date()
    return date

def update_score_worksheet(date, nps, resolution, action):
    """
    Update the score worksheet with actions to plan for the user
    wich are linked with the average NPS score of the Team
    and the issue resolution percentage.
    """
    new_score = [str(date), nps, f"{resolution}%", action]
    score_worksheet = SHEET.worksheet("score")
    score_worksheet.append_row(new_score)
    print("The score worksheet is updated: please check your Team score.")


def main():
    """
    Run all program functions.
    """
    new_data = get_new_survey_data()
    update_survey_worksheet(new_data)
    employee_list = get_employees()
    average_nps = get_average_nps(employee_list)
    resolution_percentage = calculate_resolution_percentage(employee_list)
    meeting = identify_leader_meeting(average_nps, resolution_percentage)
    training = identify_leader_training(average_nps, resolution_percentage)
    action = get_leader_action(meeting, training)
    date = get_date()
    update_score_worksheet(date, str(average_nps), str(resolution_percentage), str(action))


main()