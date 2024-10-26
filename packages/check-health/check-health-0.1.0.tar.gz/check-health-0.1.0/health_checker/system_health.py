import psutil

from .health_checker import BaseHealthChecker


class SystemHealth(BaseHealthChecker):
    def __init__(self):
        super().__init__()

    def ram_usage(self):
        """Returns RAM usage as a dictionary with total and used memory in GB."""
        mem = psutil.virtual_memory()
        return {
            "total_gb": mem.total / (1024 ** 3),
            "used_gb": mem.used / (1024 ** 3),
            "percent_used": mem.percent
        }

    def swap_usage(self):
        """Returns swap memory usage as a dictionary with total and used memory in GB."""
        swap = psutil.swap_memory()
        return {
            "total_gb": swap.total / (1024 ** 3),
            "used_gb": swap.used / (1024 ** 3),
            "percent_used": swap.percent
        }

    def storage_usage(self):
        """Returns storage usage in GB and percentage for each mounted partition."""
        storage_info = {}
        for part in psutil.disk_partitions():
            usage = psutil.disk_usage(part.mountpoint)
            storage_info[part.mountpoint] = {
                "total_gb": usage.total / (1024 ** 3),
                "used_gb": usage.used / (1024 ** 3),
                "percent_used": usage.percent
            }
        return storage_info

    def health_check_report(self):
        """Returns a dictionary with all system health metrics."""
        return {
            "ram_usage": self.ram_usage(),
            "swap_usage": self.swap_usage(),
            "storage_usage": self.storage_usage(),
        }
