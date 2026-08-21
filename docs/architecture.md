# Coffee Data Platform — Архитектура

## 1. Обзор проекта

Coffee Data Platform — это End-to-End Data Engineering платформа для обработки операционных данных сети кофеен и подготовки аналитических данных для бизнес-аналитики.

Платформа реализует полный цикл обработки данных:

- первоначальную загрузку данных;
- инкрементальную загрузку;
- формирование RAW Layer;
- подготовку данных в STAGING Layer;
- построение CORE Data Warehouse;
- формирование аналитических MARTS;
- SQL-трансформации с помощью dbt;
- аналитическую обработку с помощью PySpark;
- оркестрацию рабочих процессов с помощью Apache Airflow;
- контейнеризацию инфраструктуры с помощью Docker;
- визуализацию данных в Power BI.

Основным хранилищем платформы является PostgreSQL.

## 2. Архитектура верхнего уровня

Платформа состоит из основного End-to-End pipeline и отдельного PySpark workflow.

Основной pipeline:

Initial / Incremental Data
↓
Python Ingestion
↓
OLTP
↓
RAW
↓
STAGING
↓
CORE
↓
dbt MARTS
↓
Power BI

Отдельный PySpark workflow:

CORE
↓
PySpark
↓
Sales MART
↓
Аналитическое использование

Apache Airflow используется для оркестрации обоих workflow.

## 3. Инфраструктура

Проект запускается с использованием Docker Compose.

Основные инфраструктурные компоненты:

### PostgreSQL

PostgreSQL 15 является центральной базой данных.

Используемая база данных:

coffee_data_platform

PostgreSQL используется для хранения операционных данных, слоёв Data Warehouse и аналитических MARTS.

### Python ETL

Python используется для:

- загрузки исходных данных;
- инкрементальной обработки;
- формирования RAW Layer;
- загрузки STAGING;
- загрузки CORE.

Основной Python-код расположен в:

src/

### Apache Airflow

Apache Airflow отвечает за оркестрацию pipeline.

DAG расположены в:

airflow/dags/

Основной DAG:

airflow/dags/etl_pipeline_dag.py

Отдельный PySpark DAG:

airflow/dags/sales_pyspark_dag.py

### dbt

dbt используется для построения аналитических MARTS.

Проект расположен в:

dbt/

Модели расположены в:

dbt/models/marts/

### PySpark

PySpark используется для отдельного аналитического workflow построения Sales MART.

Основная реализация:

src/spark/sales_mart.py

### Power BI

Power BI является конечным BI-слоем платформы.

Файл отчёта:

coffee_data_platform_power_bi.pbix

## 4. Архитектура данных

Данные проходят через следующие логические слои:

OLTP
↓
RAW
↓
STAGING
↓
CORE
↓
MARTS

Каждый слой имеет отдельную ответственность.

### 4.1. OLTP

OLTP содержит операционные данные предметной области.

Основные таблицы:

- categories;
- suppliers;
- stores;
- customers;
- products;
- employees;
- orders;
- order_items;
- payments;
- deliveries.

OLTP представляет транзакционную модель исходных бизнес-данных.

### 4.2. RAW Layer

RAW Layer содержит данные, экспортированные из PostgreSQL без изменения бизнес-структуры.

Реализация:

src/raw_layer/

Результат сохраняется в:

data/raw/

RAW Layer является промежуточной границей между операционными данными и последующей обработкой Data Warehouse.

### 4.3. STAGING Layer

STAGING Layer предназначен для подготовки данных перед загрузкой в CORE Data Warehouse.

Реализация:

src/staging_load/

STAGING содержит подготовленные данные исходных сущностей и выполняет проверки перед загрузкой в CORE.

### 4.4. CORE Data Warehouse

CORE является центральным слоем Data Warehouse.

SQL-структура:

sql/create_core_tables.sql

Python loaders:

src/core_load/

CORE содержит:

- dimension tables;
- fact tables;
- surrogate keys;
- связи между dimensions и facts.

Основные dimensions:

- core.dim_categories;
- core.dim_suppliers;
- core.dim_stores;
- core.dim_customers;
- core.dim_products;
- core.dim_employees.

Основные facts:

- core.fact_orders;
- core.fact_order_items;
- core.fact_payments;
- core.fact_deliveries.

Последовательность загрузки:

STAGING
↓
CORE Dimensions
↓
CORE Facts

### 4.5. MARTS Layer

MARTS Layer содержит аналитические наборы данных, подготовленные для бизнес-анализа.

Структура:

sql/create_marts_tables.sql

Основные MARTS:

- marts.sales_mart;
- marts.customer_mart;
- marts.product_mart;
- marts.store_mart.

MARTS предназначены для анализа:

- продаж;
- клиентов;
- продуктов;
- магазинов.


## 5. Загрузка данных

Платформа поддерживает первоначальную и инкрементальную загрузку.

### 5.1. Initial Load

Исходные данные расположены в:

data/initial/

Реализация:

src/initial_load/

Основная точка входа:

src/initial_load/initial_load.py

Initial Load используется для первоначального наполнения операционной базы данных.

### 5.2. Incremental Load

Инкрементальные данные расположены в:

data/incremental/

Реализация:

src/incremental_load/

Основная точка входа:

src/incremental_load/incremental_pipeline.py

Incremental Load используется для обработки новых записей.

Обрабатываются следующие сущности:

- customers;
- orders;
- order_items;
- payments;
- deliveries.

## 6. Оркестрация Apache Airflow

Основной End-to-End workflow определён в:

airflow/dags/etl_pipeline_dag.py

DAG:

etl_pipeline

Последовательность выполнения:

Initial Load
↓
Incremental Load
↓
RAW Pipeline
↓
STAGING Pipeline
↓
CORE Pipeline
↓
dbt Marts

Каждый основной этап выполняется отдельным Airflow task.

Основной DAG настроен на ручной запуск.

Для задач используются retry и execution timeout.

Отдельный PySpark workflow определяется в:

airflow/dags/sales_pyspark_dag.py

PySpark workflow запускается независимо от основного etl_pipeline.


## 7. dbt

dbt-проект расположен в:

dbt/

Модели расположены в:

dbt/models/marts/

Текущие модели:

- customer_mart.sql;
- product_mart.sql;
- sales_mart.sql;
- store_mart.sql.

Конфигурация моделей и тесты определены в:

dbt/models/marts/schema.yml

В основном Airflow pipeline выполняется:

dbt run

dbt используется как SQL-based transformation layer для построения аналитических MARTS.


## 8. PySpark Sales MART

PySpark реализован как отдельный аналитический workflow и не является частью основного etl_pipeline.

Airflow DAG:

airflow/dags/sales_pyspark_dag.py

Основная реализация:

src/spark/sales_mart.py

PySpark использует следующие таблицы CORE:

- core.fact_orders;
- core.dim_stores.

Между таблицами выполняется JOIN по store_key.

Формируется агрегированный набор данных по дате и магазину:

- sale_date;
- store_id;
- store_name;
- orders_count;
- revenue;
- average_check.

Результат записывается во временную таблицу:

marts.sales_mart_pyspark_tmp

После проверки результат загружается в:

marts.sales_mart

Pipeline выполняет сравнение рассчитанного PySpark результата с существующим аналитическим набором перед заменой финальных данных.

PostgreSQL JDBC driver:

drivers/postgresql-42.7.13.jar

PySpark запускается внутри Airflow Docker-контейнера.


## 9. Аналитическое использование данных

Финальным BI-слоем платформы является Power BI.

Power BI использует аналитические данные, сформированные в MARTS Layer.

Основной путь аналитических данных:

PostgreSQL Data Warehouse
↓
MARTS
↓
Power BI

Power BI представляет конечный business-facing слой платформы.

Основные аналитические направления:

- продажи;
- клиенты;
- продукты;
- магазины.

## 10. Конфигурация

Конфигурация приложения отделена от основной логики с помощью environment variables.

Основные параметры подключения к PostgreSQL:

- DB_HOST;
- DB_PORT;
- DB_NAME;
- DB_USER;
- DB_PASSWORD.

Конфигурация проекта загружается через python-dotenv.

Шаблон конфигурации:

.env.example

Секреты и пароли не должны храниться непосредственно в исходном коде.

Docker-сервисы используют environment-based configuration.


## 11. Структура проекта

Основные директории проекта:

coffee-data-platform/

airflow/
dags/
logs/
plugins/

data/
initial/
incremental/
raw/

dbt/
models/
marts/

docs/

drivers/

sql/

src/
initial_load/
incremental_load/
raw_layer/
staging_load/
core_load/
spark/

tests/

utils/

Основные конфигурационные файлы:

docker-compose.yml
Dockerfile
requirements.txt
README.md


## 12. Ответственность технологий

Python — ingestion и ETL processing.

PostgreSQL — OLTP, Data Warehouse и MARTS.

Docker — контейнеризация инфраструктуры.

Apache Airflow — оркестрация workflow.

dbt — SQL-based transformation.

PySpark — специализированная аналитическая обработка Sales MART.

Power BI — Business Intelligence и визуализация.

Git — контроль версий проекта.


## 13. Архитектурные принципы

Платформа следует следующим принципам:

1. Разделение ingestion, storage, transformation и consumption layers.
2. Чёткое разделение RAW, STAGING, CORE и MARTS.
3. PostgreSQL используется как центральная платформа хранения данных.
4. Python используется для ingestion и ETL processing.
5. dbt используется для SQL-based analytical transformations.
6. PySpark используется для специализированной аналитической обработки.
7. Apache Airflow используется для orchestration.
8. Docker используется для контейнеризации инфраструктуры.
9. Power BI используется как конечный business-facing слой.
10. Конфигурация приложения отделена от основной логики с помощью environment variables.
11. Аналитические данные проходят через отдельный MARTS Layer перед использованием в BI.
12. Основной ETL workflow и PySpark workflow разделены.