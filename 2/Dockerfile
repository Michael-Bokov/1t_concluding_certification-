FROM python:3.11
# Устанавливаем зависимости
RUN pip install psycopg2-binary
WORKDIR /app
COPY . .
#po umolchanija dlja app, vozmet otsuda.Potom docker-compose ih pereopredelit.
#a eski compose ne budet to app budet brat eti.
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=employees_base
ENV DB_USER=admin
ENV DB_PASSWORD=superadmin


CMD ["python", "app.py"]
