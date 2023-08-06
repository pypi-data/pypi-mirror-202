from datetime import datetime


class bcolors:
    PURPLE = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ORANGE = "\33[38;5;208m"


levels = {
    "WARNING": bcolors.ORANGE,
    "INFO": bcolors.PURPLE,
    "ERROR": bcolors.FAIL,
    "SUCCESS": bcolors.OKGREEN,
}

PIPELINE_STR = f"{bcolors.OKBLUE}pcore{bcolors.ENDC}"


def log(val, level="INFO", flush=True):
    time_stamp = datetime.utcnow().strftime("%H:%M:%S")

    log_str = (
        f"{PIPELINE_STR} {time_stamp} - [{levels[level]}{level}{bcolors.ENDC}]: {val}"
    )

    print(f"{log_str}", flush=True)
