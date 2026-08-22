# Coffee Data Platform

End-to-End Data Engineering платформа для обработки операционных данных сети кофеен и подготовки аналитических данных для бизнес-аналитики.

## Статус проекта

**Project status: Completed**

Проект завершён как portfolio-level End-to-End Data Engineering проект.

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
PostgreSQL OLTP
        ↓
RAW
        ↓
STAGING
        ↓
CORE Data Warehouse
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
│
├── airflow/
│   ├── dags/
│   └── plugins/
│
├── data/
│   ├── initial/
│   ├── incremental/
│   └── raw/
│
├── dbt/
│   ├── models/
│   │   └── marts/
│   └── dbt_project.yml
│
├── docker/
│   └── postgres/
│       └── init/
│
├── docs/
│
├── sql/
│
├── src/
│   ├── initial_load/
│   ├── incremental_load/
│   ├── raw_layer/
│   ├── staging_load/
│   ├── core_load/
│   ├── marts/
│   └── spark/
│
├── tests/
│
├── utils/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md


## Документация

Подробное описание проекта находится в каталоге `docs/`.

- `docs/architecture.md` — архитектура платформы и потоки данных.
- `docs/business_model.md` — бизнес-модель и аналитические задачи.
- `docs/er_diagram.md` — ER-модель OLTP.

## Запуск проекта

### 1. Клонирование репозитория

```powershell
git clone https://github.com/vitaliy-platonov/coffee-data-platform.git
cd coffee-data-platform
```

### 2. Настройка конфигурации

Создай локальные файлы конфигурации:

```powershell
Copy-Item .env.example .env
Copy-Item .env.docker.example .env.docker
Copy-Item .dbt\profiles.yml.example .dbt\profiles.yml
```

Файлы `.env`, `.env.docker` и `.dbt/profiles.yml` используются только локально и не добавляются в Git.

Указанные в шаблонах учётные данные предназначены только для локальной разработки. Не используйте их в production.

### 3. Запуск инфраструктуры

```powershell
docker compose up -d --build
```

### 4. Проверка контейнеров

```powershell
docker compose ps
```

### Airflow

После запуска инфраструктуры Airflow Web UI доступен по адресу:

[http://localhost:8080](http://localhost:8080)

Для локального входа используются:

- Username: `airflow`
- Password: `airflow`

Основной ETL workflow:

`etl_pipeline`

### 5. Запуск основного ETL pipeline

Основной pipeline запускается через Apache Airflow.

DAG:

`etl_pipeline`

Основная последовательность:

```text
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
```

### 6. Запуск PySpark workflow

Отдельный DAG:

`sales_pyspark_dag`

Он запускает построение Sales MART с использованием PySpark.

## Power BI

В репозитории находится готовый Power BI report:

`coffee_data_platform_power_bi.pbix`

Отчёт используется для аналитического представления подготовленных данных.

Основные направления анализа:

- Sales;
- Customers;
- Products;
- Stores.
