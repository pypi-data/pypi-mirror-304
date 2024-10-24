import time


class Control:
    # 等待
    @staticmethod
    def wait(delay: float):
        time.sleep(delay)

    @staticmethod
    def wait_delay(is_delay: bool):
        while not is_delay:
            pass
