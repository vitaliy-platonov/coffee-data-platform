
import ctypes
import logging
import os
from pathlib import Path

import logging_config
import psycopg
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType, IntegerType


LOGGER = logging.getLogger(__name__)

def configure_jdbc_driver() -> None:
    """
    Configure PostgreSQL JDBC driver for PySpark.
    """

    driver_path = Path(
        os.getenv(
            "POSTGRES_JDBC_DRIVER",
            Path(__file__).resolve().parents[2]
            / "drivers"
            / "postgresql-42.7.13.jar",
        )
    )

    LOGGER.info(
        f"JDBC driver: {driver_path}"
    )

    LOGGER.info(
        f"Driver exists: {driver_path.exists()}"
    )

    if not driver_path.exists():
        raise FileNotFoundError(
            f"JDBC driver not found: {driver_path}"
        )

    if os.name == "nt":
        buffer = ctypes.create_unicode_buffer(1024)

        ctypes.windll.kernel32.GetShortPathNameW(
            str(driver_path),
            buffer,
            1024,
        )

        driver_path_for_spark = buffer.value

        LOGGER.info(
            f"Windows short path: {driver_path_for_spark}"
        )

    else:
        driver_path_for_spark = str(driver_path)

        LOGGER.info(
            f"Linux path: {driver_path_for_spark}"
        )

    os.environ["PYSPARK_SUBMIT_ARGS"] = (
        f'--driver-class-path "{driver_path_for_spark}" pyspark-shell'
    )


def create_spark_session() -> SparkSession:
    """
    Create SparkSession for the sales MART pipeline.
    """

    return (
        SparkSession.builder
        .appName("CoffeeDataPlatform")
        .getOrCreate()
    )

def get_jdbc_config() -> tuple[str, dict]:
    """
    Return PostgreSQL JDBC connection configuration.
    """

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "coffee_data_platform")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD")

    jdbc_url = (
        f"jdbc:postgresql://{host}:{port}/{database}"
    )

    properties = {
        "user": user,
        "password": password,
        "driver": "org.postgresql.Driver",
    }

    return jdbc_url, properties


def read_core_tables(
    spark: SparkSession,
    jdbc_url: str,
    properties: dict,
):
    """
    Read required CORE tables from PostgreSQL.
    """

    fact_orders_df = spark.read.jdbc(
        url=jdbc_url,
        table="core.fact_orders",
        properties=properties,
    )

    stores_df = spark.read.jdbc(
        url=jdbc_url,
        table="core.dim_stores",
        properties=properties,
    )

    return fact_orders_df, stores_df


def join_orders_with_stores(
    fact_orders_df,
    stores_df,
):
    """
    Join orders with stores by store_key.
    """

    return fact_orders_df.join(
        stores_df,
        fact_orders_df.store_key == stores_df.store_key,
        "inner",
    )


def build_sales_base(
    joined_df,
    fact_orders_df,
    stores_df,
):
    """
    Select the columns required to build the sales MART.
    """

    return joined_df.select(
        fact_orders_df.order_date.alias("sale_date"),
        stores_df.store_id,
        stores_df.store_name,
        fact_orders_df.order_key,
        fact_orders_df.total_amount,
    )


def build_sales_mart(sales_base_df):
    """
    Aggregate daily sales by store.
    """

    return (
        sales_base_df
        .groupBy(
            "sale_date",
            "store_id",
            "store_name",
        )
        .agg(
            F.count("order_key").alias("orders_count"),
            F.sum("total_amount").alias("revenue"),
            F.round(
                F.avg("total_amount"),
                2,
            ).alias("average_check"),
        )
    )


def select_sales_mart_columns(sales_mart_df):
    """
    Select final sales MART columns in the required order.
    """

    return sales_mart_df.select(
        "sale_date",
        "store_id",
        "store_name",
        "orders_count",
        "revenue",
        "average_check",
    )


def cast_sales_mart_types(sales_mart_df):
    """
    Cast sales MART columns to the target PostgreSQL types.
    """

    return (
        sales_mart_df
        .withColumn(
            "orders_count",
            F.col("orders_count").cast(
                IntegerType()
            ),
        )
        .withColumn(
            "revenue",
            F.col("revenue").cast(
                DecimalType(12, 2)
            ),
        )
        .withColumn(
            "average_check",
            F.col("average_check").cast(
                DecimalType(10, 2)
            ),
        )
    )



def read_existing_mart(
    spark: SparkSession,
    jdbc_url: str,
    properties: dict,
):
    """
    Read the existing sales MART from PostgreSQL.
    """

    return spark.read.jdbc(
        url=jdbc_url,
        table="marts.sales_mart",
        properties=properties,
    )


def validate_difference(
    sales_mart_df,
    existing_mart_df,
) -> int:
    """
    Count rows present in PySpark MART
    but missing from the existing MART.
    """

    differences = (
        sales_mart_df
        .subtract(existing_mart_df)
    )

    return differences.count()


def validate_reverse_difference(
    sales_mart_df,
    existing_mart_df,
) -> int:
    """
    Count rows present in the existing MART
    but missing from the PySpark MART.
    """

    reverse_differences = (
        existing_mart_df
        .subtract(sales_mart_df)
    )

    return reverse_differences.count()


def write_temp_mart(
    sales_mart_df,
    jdbc_url: str,
    properties: dict,
    temp_table: str,
) -> None:
    """
    Write the calculated sales MART to a temporary table.
    """

    sales_mart_df.write.jdbc(
        url=jdbc_url,
        table=temp_table,
        mode="overwrite",
        properties=properties,
    )


def read_temp_mart(
    spark: SparkSession,
    jdbc_url: str,
    properties: dict,
    temp_table: str,
):
    """
    Read the temporary sales MART from PostgreSQL.
    """

    return spark.read.jdbc(
        url=jdbc_url,
        table=temp_table,
        properties=properties,
    )

def load_temp_to_mart() -> None:
    """
    Replace the final sales MART with data
    from the temporary PySpark table.
    """

    with psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "coffee_data_platform"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    ) as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                TRUNCATE TABLE marts.sales_mart;
                """
            )

            cur.execute(
                """
                INSERT INTO marts.sales_mart (
                    sale_date,
                    store_id,
                    store_name,
                    orders_count,
                    revenue,
                    average_check
                )
                SELECT
                    sale_date,
                    store_id,
                    store_name,
                    orders_count,
                    revenue,
                    average_check
                FROM marts.sales_mart_pyspark_tmp;
                """
            )

def run() -> None:
    """
    Run the sales MART PySpark pipeline.
    """

    LOGGER.info(
        "Sales MART pipeline started"
    )

    configure_jdbc_driver()

    LOGGER.info(
        f"PySpark version: {pyspark.__version__}"
    )

    spark = None

    try:
        spark = create_spark_session()

        jdbc_url, properties = get_jdbc_config()

        # ----------------------------------------------------
        # READ CORE
        # ----------------------------------------------------

        fact_orders_df, stores_df = read_core_tables(
            spark,
            jdbc_url,
            properties,
        )



        joined_df = join_orders_with_stores(
            fact_orders_df,
            stores_df,
        )

        sales_base_df = build_sales_base(
            joined_df,
            fact_orders_df,
            stores_df,
        )

        sales_mart_df = build_sales_mart(
            sales_base_df,
        )


        existing_mart_df = read_existing_mart(
            spark,
            jdbc_url,
            properties,
        )

        differences_count = validate_difference(
            sales_mart_df,
            existing_mart_df,
        )

        LOGGER.info(
            f"Differences: {differences_count}"
        )

        reverse_differences_count = (
            validate_reverse_difference(
                sales_mart_df,
                existing_mart_df,
            )
        )

        LOGGER.info(
            f"Reverse differences: "
            f"{reverse_differences_count}"
        )


        sales_mart_df = (
            select_sales_mart_columns(
                sales_mart_df
            )
        )

        sales_mart_df = (
            cast_sales_mart_types(
                sales_mart_df
            )
        )


        temp_table = (
            "marts.sales_mart_pyspark_tmp"
        )

        write_temp_mart(
            sales_mart_df,
            jdbc_url,
            properties,
            temp_table,
        )


        temp_df = read_temp_mart(
            spark,
            jdbc_url,
            properties,
            temp_table,
        )

        LOGGER.info(
            f"Temp table rows: {temp_df.count()}"
        )

        temp_differences = (
            temp_df
            .subtract(existing_mart_df)
        )

        LOGGER.info(
            f"Temp differences: "
            f"{temp_differences.count()}"
        )


        load_temp_to_mart()


        final_mart_df = spark.read.jdbc(
            url=jdbc_url,
            table="marts.sales_mart",
            properties=properties,
        )

        LOGGER.info(
            f"Final MART rows: "
            f"{final_mart_df.count()}"
        )

        final_differences = (
            final_mart_df
            .subtract(sales_mart_df)
        )

        LOGGER.info(
            f"Final MART differences: "
            f"{final_differences.count()}"
        )

        LOGGER.info(
            "Sales MART pipeline finished"
        )

    except Exception:
        LOGGER.exception(
            "Sales MART pipeline failed"
        )
        raise

    finally:
        if spark is not None:
            spark.stop()


if __name__ == "__main__":
    run()
