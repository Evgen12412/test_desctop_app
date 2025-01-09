import psutil


def get_system_metrics():
    """Получает текущие метрики системы."""
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu_percent": cpu,
        "ram_free": ram.free,
        "ram_total": ram.total,
        "disk_free": disk.free,
        "disk_total": disk.total,
    }
