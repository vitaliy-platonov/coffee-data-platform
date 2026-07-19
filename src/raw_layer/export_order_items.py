from export_utils import export_table


def export_order_items() -> None:
    export_table(
        table_name="order_items",
        output_folder="order_items"
    )


if __name__ == "__main__":
    export_order_items()