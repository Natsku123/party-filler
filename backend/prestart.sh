# Wait for Mysql before starting the container
while ! mysqladmin ping -h db --silent; do
    sleep 1
done

# Update database
alembic upgrade head
