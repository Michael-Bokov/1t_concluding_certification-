from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("PostgreSQL to ClickHouse Migration") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.2.20,com.github.housepower:clickhouse-native-jdbc-shaded:2.6.5") \
        .getOrCreate()

    # подключения к PostgreSQL
    postgres_options = {
        "url": "jdbc:postgresql://localhost:5435/my_database",
        "dbtable": "users",
        "user": "user",
        "password": "password",
        "driver": "org.postgresql.Driver"
    }

    # подключения к ClickHouse
    clickhouse_options = {
        "url": "jdbc:clickhouse://localhost:9001/default",
        "dbtable": "users",
        "driver": "com.github.housepower.jdbc.ClickHouseDriver"
    }

    # Чтение данных из PostgreSQL
    postgres_df = spark.read \
        .format("jdbc") \
        .options(**postgres_options) \
        .load()

    # Запись данных в ClickHouse
    postgres_df.write \
        .format("jdbc") \
        .options(**clickhouse_options) \
        .mode("append") \
        .save()

    spark.stop()

if __name__ == "__main__":
    main()
