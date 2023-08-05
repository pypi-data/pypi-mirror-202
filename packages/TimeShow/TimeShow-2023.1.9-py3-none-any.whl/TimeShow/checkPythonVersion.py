import sys

def checkPython37_or_earlier():
    if not sys.version_info[1] >= 8 or sys.version_info[0]<3:
        sys.exit("""Sorry, This Program Can't Use On Python 3.7 or earlier.
    Please Use it on Python 3.8 or Later.""")

def checkPython312_or_Later():
    if not sys.version_info[1] <= 11:
        sys.exit("""Sorry, This Program Can't Use On Python 3.12 or later.
    Please Use it on Python 3.11 or Earlier.""")
