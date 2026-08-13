
import psycopg
from pyspark.sql.types import IntegerType, DecimalType
from pyspark.sql import functions as F
import ctypes
import os
from pathlib import Path


driver_path = (
    Path(__file__).resolve().parents[2]
    / "drivers"
    / "postgresql-42.7.13.jar"
)


buffer = ctypes.create_unicode_buffer(1024)

ctypes.windll.kernel32.GetShortPathNameW(
    str(driver_path),
    buffer,
    1024,
)

short_driver_path = buffer.value

print(f"JDBC driver: {driver_path}")
print(f"Driver exists: {driver_path.exists()}")
print(f"Short path: {short_driver_path}")


os.environ["PYSPARK_SUBMIT_ARGS"] = (
    f'--driver-class-path "{short_driver_path}" pyspark-shell'
)


import pyspark
from pyspark.sql import SparkSession


print(f"PySpark version: {pyspark.__version__}")


spark = (
    SparkSession.builder
    .appName("CoffeeDataPlatform")
    .getOrCreate()
)


jdbc_url = "jdbc:postgresql://localhost:5432/coffee_data_platform"

properties = {
    "user": "postgres",
    "password": "1234",
    "driver": "org.postgresql.Driver",
}


fact_orders_df = spark.read.jdbc(
    url=jdbc_url,
    table="core.fact_orders",
    properties=properties,
)

stores_df = spark.read.jdbc(
    url = jdbc_url,
    table = 'core.dim_stores',
    properties = properties
)

joined_df = fact_orders_df.join(
    stores_df,
    fact_orders_df.store_key == stores_df.store_key,
    'inner'
)

sales_base_df = joined_df.select(
    fact_orders_df.order_date.alias('sale_date'),
    stores_df.store_id,
    stores_df.store_name,
    fact_orders_df.order_key,
    fact_orders_df.total_amount
)

sales_mart_df = sales_base_df.groupBy(
    'sale_date',
    'store_id',
    'store_name'
).agg(
    F.count('order_key').alias('orders_count'),
    F.sum('total_amount').alias('revenue'),
    F.round(F.avg('total_amount'), 2).alias('average_check')
)

print('Sales_mart sample:')
sales_mart_df.show(10)

print('Sales_mart_rows:', sales_mart_df.count())


existing_mart_df = spark.read.jdbc(
    url=jdbc_url,
    table='marts.sales_mart',
    properties=properties
)

print('PySpark rows:', sales_mart_df.count())
print('Existing MART rows:', existing_mart_df.count())

differences = (
    sales_mart_df
    .subtract(existing_mart_df)
)

print('Differences:', differences.count())

reverse_differences = (
    existing_mart_df
    .subtract(sales_mart_df)
)

print('Reverse differences:', reverse_differences.count())

sales_mart_df = sales_mart_df.select(
    "sale_date",
    "store_id",
    "store_name",
    "orders_count",
    "revenue",
    "average_check"
)

print("Final schema:")
sales_mart_df.printSchema()

sales_mart_df = sales_mart_df.withColumn(
    "orders_count",
    F.col("orders_count").cast(IntegerType())
).withColumn(
    "revenue",
    F.col("revenue").cast(DecimalType(12, 2))
).withColumn(
    "average_check",
    F.col("average_check").cast(DecimalType(10, 2))
)

sales_mart_df.printSchema()

temp_table = "marts.sales_mart_pyspark_tmp"

sales_mart_df.write.jdbc(
    url=jdbc_url,
    table=temp_table,
    mode="overwrite",
    properties=properties,
)


temp_df = spark.read.jdbc(
    url=jdbc_url,
    table=temp_table,
    properties=properties,
)

print("Temp table rows:", temp_df.count())

temp_differences = (
    temp_df
    .subtract(existing_mart_df)
)

print("Temp differences:", temp_differences.count())

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="coffee_data_platform",
    user="postgres",
    password="1234",
) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            TRUNCATE TABLE marts.sales_mart;
        """)

        cur.execute("""
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
        """)

final_mart_df = spark.read.jdbc(
    url=jdbc_url,
    table="marts.sales_mart",
    properties=properties,
)

print("Final MART rows:", final_mart_df.count())

final_differences = (
    final_mart_df
    .subtract(sales_mart_df)
)

print("Final MART differences:", final_differences.count())


spark.stop()