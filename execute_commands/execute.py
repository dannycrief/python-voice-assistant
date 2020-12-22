from additional_functions.functions import get_numbers_from_string


def start_browser(browser_name):
    if browser_name.lower() in ["google chrome", "chrome", "google chrome browser"]:
        return 'start chrome'
    elif browser_name.lower() in ["edge", "microsoft browser", "microsoft edge browser"]:
        return 'start MicrosoftEdge'
    elif browser_name.lower() in ["opera", "opera browser"]:
        return 'start opera'
    else:
        return "Cannot find this browser"


def execute_math(phrase, text):
    numbers = get_numbers_from_string(phrase, text)
    first_number = numbers[0]
    second_number = numbers[1]
    if phrase in ["add", "plus", "+"]:
        return first_number + second_number
    elif phrase in ["subtract", "minus", "-"]:
        return first_number - second_number
    elif phrase in ["divide", "divided by", "/"]:
        try:
            return first_number / second_number
        except ZeroDivisionError as e:
            return e
    elif phrase in ["multiply", "multiplied by", "times", "*"]:
        return first_number * second_number


def set_timer():
    pass

