# Django Task for Software Engineer (L2)

## Local Setup Steps

1. Install Docker and Docker Compose.

2. Clone the repository:

   ```bash
   git clone https://github.com/sabbir-mahmud/metro-vps-task.git
   cd metro-vps-task
   ```

3. Create a `.env` file by copying the sample:

   ```bash
   cp .env.sample .env
   ```

4. Build and start the containers:

   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```

**Note:** Database migrations are handled automatically within the Docker setup. You do **not** need to run any additional commands to migrate the database.

## Loading Demo Data

To explore the project with sample data, run:

```bash
 docker exec -it django_web python manage.py loaddata data.json
```

## Running Celery

Celery and Celery Beat are included in the Docker setup. No extra configuration or commands are required to run Celery.
