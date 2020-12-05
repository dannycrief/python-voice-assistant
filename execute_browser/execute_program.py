def start_browser(browser_name):
    if browser_name.lower() in ["google chrome", "chrome", "google chrome browser"]:
        return 'start chrome'
    elif browser_name.lower() in ["edge", "microsoft browser", "microsoft edge browser"]:
        return 'start MicrosoftEdge'
    elif browser_name.lower() in ["opera", "opera browser"]:
        return 'start opera'
    else:
        return "Cannot find this browser"
