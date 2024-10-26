from abc import ABC, abstractmethod


class BaseHealthChecker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def health_check_report(self):
        pass
