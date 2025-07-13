# ALX Travel App 0x03

## Milestone 5: Setting Up Background Jobs for Email Notifications

### Overview

## Overview
A Django-based travel booking application with RESTful APIs and asynchronous email notifications using Celery and RabbitMQ.

---

### Repository

- GitHub: [alx_travel_app_0x02](https://github.com/BunnyeNyash/alx_travel_app_0x03.git)
- Main Directory: `alx_travel_app`

### Project Structure
```
alx_travel_app_0x03/
├── alx_travel_app/
│   ├── listings/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── alx_travel_app/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3
│   ├── manage.py
│   └── requirements.txt
├── README.md
```

### Key Files and Their Roles
- listings/models.py: Defines the database models:

  - Listing: Represents a travel listing.
  - Booking: Represents a user's booking for a listing.
  - Review: Represents a user's review of a listing.

- listings/serializers.py: Contains serializers for the Listing and Booking models, facilitating the conversion between model instances and JSON representations for API interactions.

- listings/management/commands/seed.py: Implements a custom Django management command to seed the database with sample data for testing and development purposes.

- listings/views.py: Contains view functions or classes to handle HTTP requests and return responses.

- listings/urls.py: Maps URLs to the corresponding views in the listings app.

- alx_travel_app/settings.py: Configures the Django project's settings, including installed apps, middleware, database configurations, and more.

- manage.py: A command-line utility that lets you interact with this Django project in various ways.

- requirements.txt: Lists the Python packages required to run the project.

- README.md: Provides an overview of the project, setup instructions, and other relevant information.


### How to Use
1. Clone the Repository

```bash
git clone https://github.com/BunnyeNyash/alx_travel_app_0x03.git
cd alx_travel_app_0x03
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
  
3. Install dependencies:

- Ensure requests and celery are installed:

```bash
pip install requests django-celery-results
pip freeze >> requirement.txt
```

4. Install and start RabbitMQ:
```bash
sudo apt-get install rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
```

5. Install and start Redis (if used):
```bash
sudo apt-get install redis-server
sudo systemctl enable redis
sudo systemctl start redis
```

6. Apply migrations and then start the Django server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

6. Celery Configuration:
- Set up Celery for sending confirmation emails. Ensure a message broker like **Redis** is configured:

```python
# settings.py
CELERY_BROKER_URL = 'amqp://localhost'  # RabbitMQ as the message broker
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Redis for storing task results
```

- Run Celery worker:

```bash
celery -A alx_travel_app worker -l info
```

7. Testing:
- Use Chapa's sandbox environment to test payment initiation and verification.
- Test the `/api/payments/initiate/` endpoint to start a payment and receive a checkout URL.
- Test the `/api/payments/verify/` endpoint to confirm payment status.
- Verify email delivery for successful payments.



### API Endpoints
**Listings:**
- `GET /api/listings/`: List all listings
- `POST /api/listings/`: Create a new listing
- `GET /api/listings/<id>/`: Retrieve a listing
- `PUT /api/listings/<id>/`: Update a listing
- `DELETE /api/listings/<id>/`: Delete a listing

**Bookings:**
- `GET /api/bookings/`: List all bookings
- `POST /api/bookings/`: Create a new booking and trigger a confirmation email.
- `GET /api/bookings/<id>/`: Retrieve a booking
- `PUT /api/bookings/<id>/`: Update a booking
- `DELETE /api/bookings/<id>/`: Delete a booking

**Payments:**
- `POST /api/payments/initiate/`: Initiates a payment for a booking and returns a checkout URL
- `GET /api/payments/verify/`: Verifies payment status using the transaction ID and updates the Payment model


### Payment Workflow
- User creates a booking.
- User initiates payment via the `/api/payments/` initiate/ endpoint.
- User is redirected to Chapa's payment page using the provided checkout URL.
- After payment, Chapa redirects to the callback URL, and the `/api/payments/verify/` endpoint updates the payment status.
- On successful payment, a confirmation email is sent via Celery.


### Swagger Documentation
Access the API documentation at http://127.0.0.1:8000/swagger/.

**Expected Responses:**
```
GET: 200 OK
POST: 201 Created
PUT: 200 OK
DELETE: 204 No Content
Errors (e.g., invalid data): 400 Bad Request
```


### Testing
Use Postman to test the endpoints

**1. Listings:**

**GET** `http://127.0.0.1:8000/api/listings/`: *Retrieve all listings*

**POST** `http://127.0.0.1:8000/api/listings/`:
```json
{
    "title": "Cozy Cabin",
    "description": "A nice cabin in the woods",
    "price": 100.00,
    "location": "Mountain Valley"
}
```

**GET** `http://127.0.0.1:8000/api/listings/1/`: *Retrieve a specific listing*

**PUT** `http://127.0.0.1:8000/api/listings/1/`:
```json
{
    "title": "Updated Cozy Cabin",
    "description": "A nice cabin in the woods",
    "price": 120.00,
    "location": "Mountain Valley"
}
```

**DELETE** `http://127.0.0.1:8000/api/listings/1/`: *Delete a listing*



**2. Bookings:**

**GET** `http://127.0.0.1:8000/api/bookings/`: *Retrieve all bookings*

**POST** `http://127.0.0.1:8000/api/bookings/`:
```json
{
    "listing": 1,
    "user": 1,
    "start_date": "2025-07-01",
    "end_date": "2025-07-05"
}
```

**GET** `http://127.0.0.1:8000/api/bookings/1/`: *Retrieve a specific booking*

**PUT** `http://127.0.0.1:8000/api/bookings/1/`:
```json
{
    "listing": 1,
    "user": 1,
    "start_date": "2025-07-02",
    "end_date": "2025-07-06"
}
```

**DELETE** `http://127.0.0.1:8000/api/bookings/1/`: *Delete a booking*


### Notes
- Ensure RabbitMQ and Redis are running.
- Make sure Celery worker starts without errors.
- Ensure Booking creation triggers the email task. and the Email is sent (or logged to console if using console backend).
