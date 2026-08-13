
import ctypes
import os
from pathlib import Path


# Путь к JDBC-драйверу внутри проекта
driver_path = (
    Path(__file__).resolve().parents[2]
    / "drivers"
    / "postgresql-42.7.13.jar"
)


# Получаем короткий Windows-путь без кириллицы
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


# Передаём JDBC-драйвер JVM ДО запуска PySpark
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

print('Joined sample:')
joined_df.show(5)

print(joined_df.count())



spark.stop()