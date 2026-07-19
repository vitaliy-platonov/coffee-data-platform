from export_utils import export_table


def export_employees() -> None:
    export_table(
        table_name="employees",
        output_folder="employees"
    )


if __name__ == "__main__":
    export_employees()