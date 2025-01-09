import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="system_monitoring.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        """Создает таблицу для хранения метрик, если она не существует."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                cpu_percent REAL,
                ram_free REAL,
                ram_total REAL,
                disk_free REAL,
                disk_total REAL
            )
        """)
        conn.commit()
        conn.close()

    def insert_metrics(self, cpu_percent, ram_free, ram_total, disk_free, disk_total):
        """Добавляет метрики в базу данных."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO metrics (timestamp, cpu_percent, ram_free, ram_total, disk_free, disk_total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, cpu_percent, ram_free, ram_total, disk_free, disk_total))
        conn.commit()
        conn.close()