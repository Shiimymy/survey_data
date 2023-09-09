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


def choose_action():
    """
    Prompt user to either enter a new survey
    or get the result for a date in the score sheet
    """
    print("You can choose between 2 actions to manage the surveys' datas.")

    user_choice = None

    while True:
        print("You can add a new survey or generate a new result for")
        print("the end of day. \n")
        user_choice = input("Enter 'survey' or 'result' to choose: ")
        if validate_action(user_choice.lower()):
            break
        else:
            print("Invalid : enter only 'survey' or 'result' ")
            continue

    return user_choice


def validate_action(user_choice):
    """
    Validate user action choice
    """
    if user_choice == "survey":
        return True
    elif user_choice == "result":
        return True
    else:
        return False


def get_user_action(user_action):
    """
    Get the user input to redirect the programm
    to the asked action
    """
    if user_action == "survey":
        new_data = get_new_survey_data()
        update_survey_worksheet(new_data)
        main()
    else:
        employee_list = get_employees()
        average_nps = get_average_nps(employee_list)
        reso_percentage = calculate_resolution_percentage(employee_list)
        meeting = identify_leader_meeting(average_nps, reso_percentage)
        training = identify_leader_training(average_nps, reso_percentage)
        action = get_leader_action(meeting, training)
        date = get_date()
        update_score_worksheet(date, average_nps, str(reso_percentage), action)


def get_new_survey_data():
    """
    Get a new survey data with 3 information from the user.
    The first should be a employee name
    The second a number between 0 and 10
    The last a 3 options string.
    """
    new_survey = []

    new_name = get_new_name()

    new_nps = get_new_nps()

    new_resolve = get_new_resolution()

    new_survey.append(new_name.capitalize())
    new_survey.append(int(new_nps))
    new_survey.append(new_resolve)

    return new_survey


def get_new_name():
    """
    Get new employee name from user to complete new survey data
    """
    new_name = None

    while True:
        print('Please enter the results of the new survey\n')
        new_name = input('Enter the employee name: \n')
        if validate_name(new_name):
            break
        else:
            print(f"{new_name} is not valid")
            continue

    return new_name


def get_new_nps():
    """
    Get new NPS from user to complete new survey data
    """
    new_nps = None

    while True:
        new_nps = input('Enter a number between 0 and 10 for the NPS: \n')
        if validate_nps(new_nps):
            break
        else:
            print("The NPS should be a number between 0 and 10\n")

    return new_nps


def get_new_resolution():
    """
    Get new resolution answer from user to complete new survey data
    """
    new_resolve = None

    while True:
        print("How the customers reponded to : Did you issue was resolved?")
        new_resolve = input("Enter 'yes', 'no' or 'i don't know': \n")
        if validate_resolution(new_resolve.lower()):
            break
        else:
            print("The input can only be 'yes', 'no' or 'I don't know'\n")

    return new_resolve


def validate_name(new_name):
    """
    Validate name given by user
    """
    if new_name.isalpha():
        return True
    else:
        return False


def validate_nps(new_nps):
    """
    Validate new nps given by user
    """
    try:
        0 <= int(new_nps) <= 10
        if not 0 <= int(new_nps) <= 10:
            return False
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def validate_resolution(new_resolve):
    """
    Validate new resolution answer given by user
    """
    if new_resolve == "yes":
        return True
    elif new_resolve == "no":
        return True
    elif new_resolve == "i don't know":
        return True
    else:
        return False


def update_survey_worksheet(data):
    """
    Update survey worksheet, add new row with the list data provided by user
    """
    survey_worksheet = SHEET.worksheet("survey")
    survey_worksheet.append_row(data)
    print("New survey added successfully. \n")


def get_employees():
    """
    Collect employees data in the
    survey sheet to calculate their stats.
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
    meeting_action = 5 < nps <= 7 or 55 < resolution <= 75

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
    training_action = nps <= 5 and resolution <= 55

    if training_action:
        training = "Training"
        return training
    else:
        no_action = ""
        return no_action


def get_leader_action(meeting, training):
    """
    Get the leader action and return what the
    leader should organize with it's Team
    """
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
    Update the score worksheet with actions to do for the user
    based on the average NPS score of the Team
    and the issue resolution percentage.
    """
    new_score = [str(date), str(nps), f"{resolution}%", str(action)]
    score_worksheet = SHEET.worksheet("score")
    score_worksheet.append_row(new_score)
    print(f"Team leader action needed : {action}")
    print("The score worksheet is updated: please check your Team score. \n")
    print("You are done for today!")
    print("Please remember to add the new survey tommorow too.")


def main():
    """
    Run the functions which start
    the programm.
    """
    user_action = choose_action()
    get_user_action(str(user_action))


main()
