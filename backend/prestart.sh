export BUILD="$(cat /app/.build)"

# Wait for Mysql before starting the container
while ! mysqladmin ping -h $DB_HOST --silent; do
    sleep 1
done

# Update database
alembic upgrade head
