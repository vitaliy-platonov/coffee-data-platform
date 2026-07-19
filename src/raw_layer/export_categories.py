
from export_utils import export_table

def export_categories() -> None:
    export_table(
        table_name="categories",
        output_folder="categories"
    )

if __name__ == "__main__":
    export_categories()