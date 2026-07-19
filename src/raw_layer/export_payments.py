from export_utils import export_table


def export_payments() -> None:
    export_table(
        table_name="payments",
        output_folder="payments"
    )


if __name__ == "__main__":
    export_payments()