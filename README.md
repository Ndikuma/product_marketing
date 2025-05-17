Product Marketing
A Django-based digital marketing platform to promote products, manage ads, track performance metrics, send email notifications, and support multiple product images, with a modern frontend using Tailwind CSS.
Prerequisites

Python 3.8+
PostgreSQL 13+
pip
SMTP server (e.g., Gmail)

Setup Instructions

Clone the Repository
git clone <repository_url>
cd product_marketing


Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies
pip install -r requirements.txt


Configure PostgreSQL

Create a database named product_marketing_db.
Update .env with your PostgreSQL credentials:DB_NAME=product_marketing_db
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432




Configure Email

For Gmail, create an App Password (https://myaccount.google.com/security).
Update .env with email settings:EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=Product Marketing <your_email@gmail.com>
ADMIN_EMAIL=admin@example.com




Set Django Secret Key

Generate a secure key and add to .env:DJANGO_SECRET_KEY=your_secure_secret_key




Configure Media Storage

Create a media/product_images/ directory in the project root.
Ensure write permissions for the web server user.


Apply Migrations
python manage.py makemigrations
python manage.py migrate


Create a Superuser
python manage.py createsuperuser


Populate Sample Data
python manage.py populate_data


Run the Development Server
python manage.py runserver


Access the Application

Frontend: http://localhost:8000
Admin: http://localhost:8000/admin
Send performance report: python manage.py send_performance_report --email your_email@example.com



Features

Modern Frontend: Responsive UI with Tailwind CSS, including homepage, product/ad/metric lists, details, and forms.
Multiple Product Images: Upload or link multiple images per product, displayed in a carousel.
CRUD Operations: Create, read, update, and delete products, ads, metrics, and images via function-based views.
Product Management: Manage products with purchase URLs, low stock alerts, and multiple images.
Ad Management: Create and optimize ads with A/B testing and targeting.
Performance Tracking: Track metrics (CTR, ROAS, engagement).
Email Notifications: Automated emails for ad pauses, low stock, and ad creation.
Performance Reports: Send reports via admin actions or management command.
Admin Interface: Easy management with search, filters, email actions, and image inlines.
Sample Data: Pre-populated data for testing.

Notes

Secure SECRET_KEY and email credentials in production.
For API integrations, explore xAI’s API at https://x.ai/api.
SuperGrok subscribers can leverage higher quotas (details at https://x.ai/grok).
Tailwind CSS is included via CDN for simplicity.
Use a production-ready media storage solution (e.g., AWS S3) in production.

Current Time

Project configured for Africa/Johannesburg (CAT) timezone, current time: 12:40 PM, May 17, 2025.

