import datetime


def parse_tasks(text: str):
    tasks = []
    strings = text.split("\n")
    for string in strings:
        string = string.strip()
        if string == "":
            continue
        try:
            time, repeat, message = string.split(" ", 2)
        except Exception:
            continue
        message = message.strip()
        try:
            time = datetime.datetime.strptime(time, "%H:%M").time()
        except Exception:
            continue
        time = time.strftime("%H:%M")
        tasks.append((time, message, repeat))
    return tasks
