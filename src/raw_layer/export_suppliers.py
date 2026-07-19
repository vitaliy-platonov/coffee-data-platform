from export_utils import export_table


def export_suppliers() -> None:
    export_table(
        table_name="suppliers",
        output_folder="suppliers"
    )


if __name__ == "__main__":
    export_suppliers()