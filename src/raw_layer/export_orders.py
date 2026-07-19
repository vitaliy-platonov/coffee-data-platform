from export_utils import export_table


def export_orders() -> None:
    export_table(
        table_name="orders",
        output_folder="orders"
    )


if __name__ == "__main__":
    export_orders()