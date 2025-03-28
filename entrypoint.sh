#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "PostgreSQL is up and running!"

echo "Applying migrations..."
python manage.py migrate --noinput


echo "Creating superuser if it does not exist..."
 
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="$DJANGO_SUPERUSER_USERNAME").exists():
    User.objects.create_superuser("$DJANGO_SUPERUSER_USERNAME", "$DJANGO_SUPERUSER_EMAIL", "$DJANGO_SUPERUSER_PASSWORD")

EOF

FLAG_FILE="/app/.db_seeded"

if [ ! -f "$FLAG_FILE" ]; then
    echo "Populating the database with passwords..."
    python -u manage.py runscript import_rockyou
    touch "$FLAG_FILE"
else
    echo "Database already seeded, skipping runscript."
fi

exec "$@"