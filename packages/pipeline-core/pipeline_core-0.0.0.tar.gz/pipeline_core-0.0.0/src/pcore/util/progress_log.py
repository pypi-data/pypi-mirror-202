import sys
import threading
import time

from pipeline.util.logging import bcolors


class ProgressContext:
    busy = False
    delay = 0.1

    text: str = None
    last_string: str = ""

    @staticmethod
    def spinning_cursor():
        start_time = time.time()
        while 1:
            yield int((time.time() - start_time) * 100.0) / 100.0

    def __init__(self, delay: float = None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        while self.busy:
            new_string = (
                f"{bcolors.OKBLUE}pcore{bcolors.ENDC} "
                f"({str(next(self.spinner_generator))}s) - {self.text}"
            )

            if len(new_string) < len(self.last_string):
                new_string += " " * (len(self.last_string) - len(new_string) - 1)

            new_string += "\r"
            self.last_string = new_string
            new_string.replace("\n", "")
            sys.stdout.write(new_string)
            sys.stdout.flush()
            time.sleep(self.delay)

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()
        return self

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False
        print("")

    @staticmethod
    def set_text(msg: str) -> None:
        ProgressContext.text = msg
