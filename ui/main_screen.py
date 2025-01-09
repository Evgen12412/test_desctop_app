import asyncio
import flet as ft
from datetime import datetime

from backend.database import Database
from backend.services import get_system_metrics
from ui.components import (
    create_interval_input,
    create_interval_button,
    create_start_button,
    create_stop_button,
    create_timer_text,
)


def main_screen(page: ft.Page):
    # Текстовые элементы для отображения метрик
    cpu_text = ft.Text(value="Загрузка ЦП: ", size=20)
    ram_text = ft.Text(value="ОЗУ: ", size=20)
    disk_text = ft.Text(value="ПЗУ: ", size=20)

    # Изначально виден только текст ЦП
    cpu_text.visible = True
    ram_text.visible = False
    disk_text.visible = False

    # Переменная для хранения интервала обновления (по умолчанию 1 секунда)
    update_interval = 1

    # Переменная для хранения состояния записи
    is_recording = False

    # Переменная для хранения времени начала записи
    start_time = None

    # Таймер для отображения времени записи
    timer_text = create_timer_text()

    # Инициализация базы данных
    db = Database()

    # Функция для обновления метрик
    async def update_metrics():
        while True:
            try:
                # Получаем данные
                metrics = get_system_metrics()

                # Обновляем значения текста
                cpu_text.value = f"Загрузка ЦП: {metrics['cpu_percent']}%"
                ram_text.value = f"ОЗУ: {metrics['ram_free'] / (1024 ** 3):.2f} ГБ свободно / {metrics['ram_total'] / (1024 ** 3):.2f} ГБ всего"
                disk_text.value = f"ПЗУ: {metrics['disk_free'] / (1024 ** 3):.2f} ГБ свободно / {metrics['disk_total'] / (1024 ** 3):.2f} ГБ всего"

                # Если запись активна, сохраняем данные в БД
                if is_recording:
                    db.insert_metrics(
                        metrics['cpu_percent'],
                        metrics['ram_free'],
                        metrics['ram_total'],
                        metrics['disk_free'],
                        metrics['disk_total'],
                    )

                page.update()  # Обновляем страницу
            except Exception as ex:
                print(f"Ошибка в update_metrics: {ex}")

            # Ждем заданный интервал перед следующим обновлением
            await asyncio.sleep(update_interval)

    # Запускаем асинхронный цикл для обновления метрик
    page.run_task(update_metrics)

    # Функция для обработки нажатий кнопок и переключения видимости
    def toggle_visibility(e, text_widget):
        try:
            cpu_text.visible = text_widget == cpu_text
            ram_text.visible = text_widget == ram_text
            disk_text.visible = text_widget == disk_text
            page.update()  # Обновляем страницу
        except Exception as ex:
            print(f"Ошибка в toggle_visibility: {ex}")

    # Функция для изменения интервала обновления
    def change_update_interval(e):
        nonlocal update_interval
        try:
            # Получаем значение из текстового поля и преобразуем в число
            new_interval = int(interval_input.value)
            if new_interval > 0:
                update_interval = new_interval
                print(f"Интервал обновления изменен на {update_interval} секунд")
            else:
                print("Интервал должен быть больше 0")
        except ValueError:
            print("Введите корректное число")

    # Функция для запуска записи
    def start_recording(e):
        nonlocal is_recording, start_time
        is_recording = True
        start_time = datetime.now()
        start_button.visible = False
        stop_button.visible = True
        page.run_task(update_timer)  # Запускаем таймер
        page.update()

    # Функция для остановки записи
    def stop_recording(e):
        nonlocal is_recording, start_time
        is_recording = False
        start_time = None
        start_button.visible = True
        stop_button.visible = False
        timer_text.value = "00:00:00"  # Сбрасываем таймер
        page.update()

    # Функция для обновления таймера
    async def update_timer():
        while is_recording:
            elapsed_time = datetime.now() - start_time
            timer_text.value = str(elapsed_time).split(".")[0]  # Отображаем время без миллисекунд
            page.update()
            await asyncio.sleep(1)

    # Поле для ввода интервала обновления
    interval_input = create_interval_input(change_update_interval)

    # Кнопка для применения нового интервала
    interval_button = create_interval_button(change_update_interval)

    # Кнопка "Начать запись"
    start_button = create_start_button(start_recording)

    # Кнопка "Остановить"
    stop_button = create_stop_button(stop_recording)

    # Кнопки для переключения видимости
    container_title = ft.Row([
        ft.TextButton(
            content=ft.Text("ЦП"),
            on_click=lambda e: toggle_visibility(e, cpu_text),
        ),
        ft.TextButton(
            content=ft.Text("ОЗУ"),
            on_click=lambda e: toggle_visibility(e, ram_text),
        ),
        ft.TextButton(
            content=ft.Text("ПЗУ"),
            on_click=lambda e: toggle_visibility(e, disk_text),
        ),
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Основной макет
    return ft.Column([
        ft.Container(container_title, width=300, height=20, alignment=ft.alignment.top_center),
        ft.Container(
            content=ft.Row([cpu_text, ram_text, disk_text], alignment=ft.MainAxisAlignment.CENTER),
            padding=10,
            border=ft.border.all(1, ft.colors.BLACK)
        ),
        ft.Row([interval_input, interval_button], alignment=ft.MainAxisAlignment.CENTER),  # Поле и кнопка для интервала
        ft.Row([start_button, stop_button, timer_text], alignment=ft.MainAxisAlignment.CENTER),  # Кнопки и таймер
    ], alignment=ft.MainAxisAlignment.CENTER)
