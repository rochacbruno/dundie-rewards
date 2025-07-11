import flet as ft
from dundie.core import read, add, get_transactions, ResultDict


def main(page: ft.Page):
    """Entry point for Application"""
    page.title = "Dundie Rewards"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT
    selected_email = ft.Ref[str]()

    def router(event):
        """Called when page.go navigates to a given route"""
        page.views.clear()
        if event.route == "/":
            page.views.append(create_users_list_view())
        elif event.route == "/transactions":
            page.views.append(create_user_transactions_view())
        page.update()

    def go_to_user_transactions(e):
        """Navigate to the transactions page for a given user"""
        selected_email.current = e.control.data
        page.go("/transactions")

    def create_users_list_table() -> ft.DataTable:
        """Create a table of all users"""
        users = read(add_rates=False)
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Balance")),
                ft.DataColumn(ft.Text("Action")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(user["name"])),
                        ft.DataCell(ft.Text(user["email"])),
                        ft.DataCell(ft.Text(f"{user['balance']:.2f}")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.ADD_CIRCLE,
                                icon_color=ft.Colors.GREEN,
                                on_click=go_to_user_transactions,
                                data=user["email"],
                            )
                        ),
                    ]
                )
                for user in users
            ],
        )

    def create_transactions_rows(transactions: ResultDict) -> list[ft.DataRow]:
        """Create a list of rows for a given list of transactions"""
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(transaction["date"])),
                    ft.DataCell(ft.Text(transaction["actor"])),
                    ft.DataCell(
                        ft.Text(
                            f"{transaction['value']:.2f}",
                            color=ft.Colors.GREEN
                            if transaction["value"] > 0
                            else ft.Colors.RED,
                        )
                    ),
                ]
            )
            for transaction in transactions
        ]

    def create_users_list_view() -> ft.View:
        """Create the main view for the users list"""
        data_table = create_users_list_table()
        view = ft.View(
            "/",
            [
                ft.AppBar(
                    title=ft.Text("Dundie Rewards - Users"),
                    bgcolor=ft.Colors.BLUE_GREY_50,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "All Users", size=24, weight=ft.FontWeight.BOLD
                            ),
                            ft.Container(height=20),
                            data_table,
                        ],
                    ),
                    padding=20,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
        return view

    def create_user_transactions_view() -> ft.View:
        """Create the view for the transactions of a given user"""
        amount_field = ft.TextField(
            label="Amount",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200,
            icon=ft.Icons.MONEY,
        )
        user_info = read(add_rates=False, email=selected_email.current)
        user_info = user_info[0] if user_info else None
        balance_text = ft.Text(
            f"Current Balance: {user_info['balance']:.2f}"
            if user_info
            else "User not found",
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        def refresh_page():
            user_info = read(add_rates=False, email=selected_email.current)
            if user_info:
                balance_text.value = (
                    f"Current Balance: {user_info[0]['balance']:.2f}"
                )
            transactions = get_transactions(selected_email.current)
            transactions_table.rows = create_transactions_rows(transactions)
            page.update()

        def on_add_click(e):
            try:
                value = int(amount_field.value)
                add(value=value, email=selected_email.current)
                amount_field.value = ""
                page.open(
                    ft.SnackBar(
                        content=ft.Text(
                            f"That's what she said! Successfully added {value} points!"
                        ),
                        bgcolor=ft.Colors.GREEN,
                    )
                )
            except ValueError:
                page.open(
                    ft.SnackBar(
                        content=ft.Text(
                            "No! No! No!Please enter a valid integer"
                        ),
                        bgcolor=ft.Colors.RED,
                    )
                )
            except Exception as ex:
                page.open(
                    ft.SnackBar(
                        content=ft.Text(f"Error: {str(ex)}"),
                        bgcolor=ft.Colors.RED,
                    )
                )
            finally:
                refresh_page()

        transactions = get_transactions(selected_email.current)
        rows = create_transactions_rows(transactions)
        transactions_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("Actor")),
                ft.DataColumn(ft.Text("Value")),
            ],
            rows=rows,
        )

        return ft.View(
            "/transactions",
            [
                ft.AppBar(
                    title=ft.Text(f"Transactions - {selected_email.current}"),
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    leading=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda _: page.go("/"),
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            balance_text,
                            ft.Container(height=20),
                            ft.Row(
                                [
                                    amount_field,
                                    ft.ElevatedButton(
                                        "Add",
                                        icon=ft.Icons.ADD,
                                        on_click=on_add_click,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Container(height=30),
                            ft.Text(
                                "Transaction History",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Container(height=10),
                            transactions_table,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=20,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    page.on_route_change = router
    page.go(page.route)


def run():
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)


if __name__ == "__main__":
    run()
