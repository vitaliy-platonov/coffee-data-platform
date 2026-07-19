from export_utils import export_table


def export_stores() -> None:
    export_table(
        table_name="stores",
        output_folder="stores"
    )


if __name__ == "__main__":
    export_stores()