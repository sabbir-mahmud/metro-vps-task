# Django Task for Software Engineer (L2)

## Local Setup Steps

1. Install Docker and Docker Compose.

2. Clone the repository:

   ```bash
   git clone https://github.com/sabbir-mahmud/metro-vps-task.git
   cd metro-vps-task
   ```

3. Create a `.env` file by copying the sample:
   Update `EXCHANGE_RATE_API_KEY` with a valid API key.

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

## API Endpoints

**POSTMAN Documentation:** [View Here](https://documenter.getpostman.com/view/20333890/2sB3BALsXT)

### Authentication

#### Get Token

Endpoint: `POST /auth/api/v1/token/`
Generates access and refresh tokens for a user.

```bash
curl --location 'http://127.0.0.1:8000/auth/api/v1/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "demoStaff",
    "password": "demo@112"
}'
```

#### Refresh Token

Endpoint: `POST /auth/api/v1/token/refresh/`
Refreshes the access token using a valid refresh token.

```bash
curl --location 'http://127.0.0.1:8000/auth/api/v1/token/refresh/' \
--header 'Content-Type: application/json' \
--data '{
    "refresh": "<your-refresh-token>"
}'
```

### Subscription Management

#### Create a Subscription

Endpoint: `POST /services/api/v1/subscriptions/`
Creates a new subscription to a plan (authentication required).
**Required field:**

* `plan`: ID of the plan the user wants to subscribe to.

```bash
curl --location 'http://127.0.0.1:8000/services/api/v1/subscriptions/' \
--header 'Authorization: Bearer <access-token>' \
--header 'Content-Type: application/json' \
--data '{
    "plan": 1
}'
```

#### List Subscriptions

Endpoint: `GET /services/api/v1/subscriptions/`
Retrieves a list of all active subscriptions for the authenticated user.

```bash
curl --location 'http://127.0.0.1:8000/services/api/v1/subscriptions/' \
--header 'Authorization: Bearer <access-token>'
```

#### Cancel a Subscription

Endpoint: `POST /services/api/v1/cancel-subscription/`
Cancels an existing subscription. Optional `reason` field for feedback.
**Required field:**

* `plan`: ID of the plan to cancel.
  **Optional field:**
* `reason`: Text explaining why the subscription is being canceled.

```bash
curl --location 'http://127.0.0.1:8000/services/api/v1/cancel-subscription/' \
--header 'Authorization: Bearer <access-token>' \
--header 'Content-Type: application/json' \
--data '{
    "plan": 1,
    "reason": "Performance Issue"
}'
```

### Exchange Rate API

#### Get Exchange Rate

Endpoint: `GET /services/api/v1/exchange-rate/?base=USD&target=BDT`
Fetches real-time exchange rates between two currencies using a public API.
**Query Parameters:**

* `base`: The base currency (e.g., USD)
* `target`: The target currency (e.g., BDT)

```bash
curl --location 'http://127.0.0.1:8000/services/api/v1/exchange-rate/?base=usd&target=bdt'
```

**Note:** All protected endpoints require a valid Bearer token in the `Authorization` header.
