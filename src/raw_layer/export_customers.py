
from export_utils import export_table

def export_customers() -> None:
    export_table(
        table_name="customers",
        output_folder="customers"
    )

if __name__ == "__main__":
    export_customers()