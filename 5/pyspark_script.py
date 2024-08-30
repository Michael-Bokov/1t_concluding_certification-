from pyspark.sql import SparkSession

def main():
    # Inicializacija Spark sessii
    spark = SparkSession.builder \
        .appName("PostgreSQL&ClickHouse") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.2.20,com.github.housepower:clickhouse-native-jdbc-shaded:2.6.5") \
        .getOrCreate()
    # Connections
    postgres_options = {
        "url": "jdbc:postgresql://localhost:5435/my_database",
        "dbtable": "employees",
        "user": "user",
        "password": "password",
        "driver": "org.postgresql.Driver"
    }
    clickhouse_options = {
        "url": "jdbc:clickhouse://localhost:9001/default",
        "dbtable": "employees",
        "user": "",
        "password": "",
        "driver": "com.github.housepower.jdbc.ClickHouseDriver"
    }
    postgres_df = spark.read \
        .format("jdbc") \
        .options(**postgres_options) \
        .load()
    clickhouse_df = spark.read \
        .format("jdbc") \
        .options(**clickhouse_options) \
        .load()
    print("Data from PostgreSQL:")
    postgres_df.show()
    print("Data from ClickHouse:")
    clickhouse_df.show()

    spark.stop()
if __name__=="__main__":
    main()
