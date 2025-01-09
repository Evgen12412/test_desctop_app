import flet as ft

from ui.main_screen import main_screen


def main(page: ft.Page):
    page.title = "System Monitoring"
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Добавление основного экрана
    page.add(main_screen(page))

if __name__ == '__main__':
    ft.app(
        main,
        view=ft.AppView.FLET_APP,
    )