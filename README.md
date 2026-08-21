# Coffee Data Platform

End-to-End Data Engineering платформа для обработки операционных данных сети кофеен и подготовки аналитических данных для бизнес-аналитики.

## Цель проекта

Проект демонстрирует полный цикл построения Data Engineering платформы:

- загрузка исходных данных;
- инкрементальная обработка;
- RAW Layer;
- STAGING Layer;
- CORE Data Warehouse;
- аналитические MARTS;
- SQL-трансформации с помощью dbt;
- аналитическая обработка с помощью PySpark;
- оркестрация с помощью Apache Airflow;
- контейнеризация с помощью Docker;
- визуализация данных в Power BI.

Основное хранилище данных — PostgreSQL.

## Архитектура

Основной поток данных:

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

Отдельный аналитический workflow:

CORE
↓
PySpark
↓
Sales MART
↓
Аналитическое использование

Apache Airflow используется для оркестрации workflow.

PostgreSQL является центральным хранилищем данных.

## Технологический стек

### Data Engineering

- Python
- PostgreSQL
- SQL
- Apache Airflow
- dbt
- PySpark

### Infrastructure

- Docker
- Docker Compose

### Analytics

- Power BI

### Development

- Git
- GitHub

## Реализовано

### Data Ingestion

- Initial Load;
- Incremental Load;
- загрузка данных в PostgreSQL;
- обработка новых записей.

### Data Warehouse

- RAW Layer;
- STAGING Layer;
- CORE Data Warehouse;
- dimension tables;
- fact tables;
- surrogate keys.

### Analytical Layer

- Sales MART;
- Customer MART;
- Product MART;
- Store MART.

### Orchestration

- основной ETL pipeline в Apache Airflow;
- отдельный PySpark workflow;
- retry и execution timeout для основных ETL-задач.

### Transformations

- dbt models для аналитических MARTS;
- PySpark processing для Sales MART.

### BI

- Power BI report;
- аналитика продаж;
- аналитика клиентов;
- аналитика продуктов;
- аналитика магазинов.


## Аналитические MARTS

### Sales MART

Ежедневные показатели продаж по магазинам:

- количество заказов;
- выручка;
- средний чек.

### Customer MART

Показатели клиентов:

- количество заказов;
- общая сумма покупок;
- средний чек.

### Product MART

Показатели продуктов:

- количество заказов;
- количество проданных единиц;
- общая выручка.

### Store MART

Показатели магазинов:

- количество заказов;
- количество клиентов;
- общая выручка;
- средний чек.


## Структура проекта

coffee-data-platform/

├── airflow/
│   └── dags/

├── data/
│   ├── initial/
│   ├── incremental/
│   └── raw/

├── dbt/
│   └── models/
│       └── marts/

├── docs/

├── drivers/

├── sql/

├── src/
│   ├── initial_load/
│   ├── incremental_load/
│   ├── raw_layer/
│   ├── staging_load/
│   ├── core_load/
│   └── spark/

├── tests/

├── utils/

├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md


## Документация

Подробное описание проекта находится в каталоге `docs/`.

- `docs/architecture.md` — архитектура платформы и потоки данных.
- `docs/business_model.md` — бизнес-модель и аналитические задачи.
- `docs/er_diagram.md` — ER-модель OLTP.

## Запуск проекта

### 1. Клонирование репозитория

git clone <URL_репозитория>

cd coffee-data-platform

### 2. Настройка конфигурации

Создай необходимые environment variables на основе:

.env.example

### 3. Запуск инфраструктуры

docker compose up -d --build

### 4. Проверка контейнеров

docker compose ps

### 5. Запуск основного ETL pipeline

Основной pipeline запускается через Apache Airflow.

DAG:

etl_pipeline

Основная последовательность:

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

### 6. Запуск PySpark workflow

Отдельный DAG:

sales_pyspark_dag

Он запускает построение Sales MART с использованием PySpark.


## Результат проекта

В результате построена End-to-End Data Engineering платформа, которая объединяет:

- операционные данные;
- ETL-процессы;
- Data Warehouse;
- аналитические MARTS;
- SQL-трансформации;
- распределённую аналитическую обработку;
- оркестрацию;
- BI-визуализацию.

Проект демонстрирует практическое применение Python, PostgreSQL, Docker, Apache Airflow, dbt, PySpark и Power BI в единой Data Engineering платформе.

## Назначение проекта для портфолио

Проект демонстрирует навыки:

- построения ETL pipeline;
- работы с PostgreSQL;
- проектирования Data Warehouse;
- работы с RAW, STAGING, CORE и MARTS слоями;
- разработки SQL-трансформаций;
- оркестрации процессов;
- контейнеризации;
- аналитической обработки данных с помощью PySpark;
- подготовки данных для BI;
- документирования Data Engineering проекта.

## Статус проекта

Проект находится в стадии финальной подготовки portfolio release.

Основные компоненты платформы реализованы и проходят финальный технический аудит.

