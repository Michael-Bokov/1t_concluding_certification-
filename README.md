# 1t_concluding_certification

DockerHub
task1: michaelbokov/concluding_cert:task1
tesk2: michaelbokov/concluding_cert:task2


1)Задание 1. Создание Docker-контейнера, который запускает Python-скрипт для анализа файловой системы и вывода приветствия.
Example:
![image](https://github.com/user-attachments/assets/61791a4b-a2f0-4cdc-9b7c-a39da08aca50)

Container:
michaelbokov/concluding_cert:task1
2)Задание 2. Создание Docker-контейнера с PostgreSQL и Python-приложением
В Dockerfile опишите шаги для создания Docker-образа Python-приложения, которое будет работать с PostgreSQL.Создайте docker-compose.yml, чтобы оркестрировать контейнеры с PostgreSQL и Python-приложением.После выполнения команды docker-compose up Вы увидите в логах вывод от Python-приложения, который должен включать данные из таблицы employees.
Example:
![image](https://github.com/user-attachments/assets/b7be859e-88fa-4355-928b-e1ddbd3d1d57)

Container:
michaelbokov/concluding_cert:task1

5)Создание Docker-контейнер с PostgreSQL и ClickHouse


Цель: Научиться развертывать базы данных PostgreSQL и ClickHouse в Docker с использованием Docker Compose, создавать таблицы и данные в этих базах данных, а затем использовать PySpark для чтения данных из обеих баз данных и работы с ними в рамках одного DataFrame.

Описание задания:

    Создайте директорию для проекта и необходимые файлы.

    Создайте файлы create_tables.sql, которые будут содержать SQL-запросы для создания таблиц и вставки данных в обе базы данных.

    В docker-compose.yml опишите конфигурацию для развертывания контейнеров с PostgreSQL и ClickHouse.

    Выполните команду для запуска контейнеров с PostgreSQL и ClickHouse.

    Создайте файл pyspark_script.py в вашем локальном окружении (вне Docker), который будет подключаться к обеим базам данных и читать данные.

    Вы должны увидеть вывод данных из обеих баз данных (PostgreSQL и ClickHouse), считанных и обработанных PySpark.

Пример вывода: 


Результат задания — после выполнения задания у вас будет Docker-среда, в которой будет 2 базы данных. Используя PySpark, необходимо прочитать данные из обеих БД в рамках одного скрипта.




