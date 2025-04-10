# Library service

- Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before start

## About project:

Library Service allows users to rent books through a web interface, pay for the rentals using Stripe, and receive notifications via Telegram.

### Requirements:
- Python 3.8+
- Docker
- PostgreSQL
- Stripe account (for test payments)


### Environment Setup:
1. Clone the repository:
   ```bash
   git clone <your-repository-url>

2. Run next commands:
   ```bash
   docker-compose build
   docker-compose up
3. For creating superuser run: 
   ```bash
   docker-compose exec app python manage.py createsuperuser   

Navigate to http://127.0.0.1:8080 in your browser.