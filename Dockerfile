FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y iputils-ping

COPY . .
ENV DJANGO_SETTINGS_MODULE=pharm.settings
EXPOSE 8000
# Run migrations, create superuser, and start server
CMD ["sh", "-c", "python manage.py migrate && echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python manage.py shell && python manage.py runserver 0.0.0.0:8000"]
