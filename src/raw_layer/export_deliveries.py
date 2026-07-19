
from export_utils import export_table

def export_deliveries() -> None:
    export_table(
        table_name="deliveries",
        output_folder="deliveries"
    )

if __name__ == "__main__":
    export_deliveries()