import asyncio

import flet as ft
import psutil


def main_screen(page: ft.Page):
    # Текстовые элементы для отображения метрик
    cpu_text = ft.Text(value="Загрузка ЦП: ", size=20)
    ram_text = ft.Text(value="Загрузка ОЗУ: ", size=20)
    disk_text = ft.Text(value="Загрузка ПЗУ: ", size=20)

    # Изначально виден только текст ЦП
    cpu_text.visible = True
    ram_text.visible = False
    disk_text.visible = False

    # Переменная для хранения интервала обновления (по умолчанию 1 секунда)
    update_interval = 1

    # Функция для обновления метрик
    async def update_metrics():
        while True:
            try:
                # Получаем данные
                cpu = psutil.cpu_percent()  # Процент загрузки CPU
                ram = psutil.virtual_memory()  # Информация об ОЗУ
                disk = psutil.disk_usage('/')  # Информация о диске

                # Обновляем значения текста
                cpu_text.value = f"Загрузка ЦП: {cpu}%"
                ram_text.value = f"ОЗУ: {ram.free / (1024 ** 3):.2f} ГБ свободно / {ram.total / (1024 ** 3):.2f} ГБ всего"
                disk_text.value = f"ПЗУ: {disk.free / (1024 ** 3):.2f} ГБ свободно / {disk.total / (1024 ** 3):.2f} ГБ всего"
                page.update()  # Обновляем страницу

            except Exception as ex:
                print(f"Ошибка в update_metrics: {ex}")

            # Ждем 1 секунду перед следующим обновлением
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

    # Поле для ввода интервала обновления
    interval_input = ft.TextField(
        label="Интервал обновления (сек)",
        value="1",  # Значение по умолчанию
        width=200,
    )

    # Кнопка для применения нового интервала
    interval_button = ft.ElevatedButton(
        text="Применить",
        on_click=change_update_interval,
    )


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
            padding=10,  # Добавляем отступы для видимости
            border=ft.border.all(1, ft.colors.BLACK)  # Добавляем рамку для видимости
        ),
        ft.Row([interval_input, interval_button], alignment=ft.MainAxisAlignment.CENTER),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

