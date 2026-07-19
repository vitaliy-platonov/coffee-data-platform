from export_utils import export_table


def export_products() -> None:
    export_table(
        table_name="products",
        output_folder="products"
    )


if __name__ == "__main__":
    export_products()