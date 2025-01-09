from dataclasses import dataclass


@dataclass
class SystemMetrics:
    cpu_percent: float
    ram_free: float
    ram_total: float
    disk_free: float
    disk_total: float
