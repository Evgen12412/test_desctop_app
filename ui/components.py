import flet as ft


def create_interval_input(on_change):
    """Создает поле для ввода интервала обновления."""
    return ft.TextField(
        label="Интервал обновления (сек)",
        value="1",  # Значение по умолчанию
        width=200,
        on_change=on_change,
    )


def create_interval_button(on_click):
    """Создает кнопку для применения интервала."""
    return ft.ElevatedButton(
        text="Применить",
        on_click=on_click,
    )


def create_start_button(on_click):
    """Создает кнопку 'Начать запись'."""
    return ft.ElevatedButton(
        text="Начать запись",
        on_click=on_click,
    )


def create_stop_button(on_click):
    """Создает кнопку 'Остановить'."""
    return ft.ElevatedButton(
        text="Остановить",
        on_click=on_click,
        visible=False,  # Изначально скрыта
    )


def create_timer_text():
    """Создает текстовое поле для отображения таймера."""
    return ft.Text(value="00:00:00", size=20)