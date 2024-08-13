# SwiftRide Application

SwiftRide is an innovative application designed to enhance the train ticket reservation experience. This app offers a range of advanced features to make train travel more convenient and enjoyable for passengers.

## Key Features

- **Seat Selection:** Passengers can choose their preferred seats during the booking process.
- **Online Payment:** Secure online payment options with credit and debit cards.
- **Optical Tickets:** Digital tickets that can be stored and accessed on mobile devices.
- **Train Tracking:** Real-time tracking of trains to keep passengers informed of their journey status.
- **Ticket Scanning:** Scan tickets to access detailed trip information, including departure times, stops, and more.

## Technologies Used

- **Backend Framework:** Django
- **Database:** PostgreSQL
- **Payment Gateway:** Stripe
- **Real-Time Features:** WebSockets
- **API Communication:** RESTful APIs
- **Security:** Implemented best practices for data protection

## How to Run the Project

### 1. Clone the Repository
First, clone the SwiftRide repository to your local machine:

```bash
git clone https://github.com/Waleeddarwesh/SwiftRide.git
cd SwiftRide
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment:
```bash
pip install virtualenv
Vitrualenv venv
cd venv
Scripts/activate
cd..
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Setting Up PostgreSQL Database

To configure your PostgreSQL database for the SwiftRide application, follow these steps:

1. **Install PostgreSQL:**
   - If PostgreSQL is not already installed, download and install it from the official [PostgreSQL website](https://www.postgresql.org/download/).

2. **Create a New Database:**
   - After installing PostgreSQL, open your terminal and run the following commands to create a new database:
     ```bash
     psql
     CREATE DATABASE swiftride_db;
     CREATE USER swiftride_user WITH PASSWORD 'your_password';
     ALTER ROLE swiftride_user SET client_encoding TO 'utf8';
     ALTER ROLE swiftride_user SET default_transaction_isolation TO 'read committed';
     ALTER ROLE swiftride_user SET timezone TO 'UTC';
     GRANT ALL PRIVILEGES ON DATABASE swiftride_db TO swiftride_user;
     \q
     ```

3. **Configure Django Settings:**
   - Open your `settings.py` file and configure the `DATABASES` setting to use PostgreSQL:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'swiftride_db',
             'USER': 'swiftride_user',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```
   - Configure Stripe Keys:
    - Open `settings.py` and add your Stripe API keys. Locate the following section and replace the placeholders with your actual keys:
     ```python
     # STRIPE
     STRIPE_SECRET_KEY = 'your_stripe_secret_key'
     STRIPE_PUBLISHABLE_KEY = 'your_stripe_publishable_key'
     STRIPE_WEBHOOK_SECRET = 'your_stripe_webhook_secret'
     ```
    - You can find your Stripe API keys in your Stripe Dashboard under the Developers section.

### 4. **Apply Migrations:**
   - Run the following commands to apply migrations and set up your database schema:
     ```bash
     cd SwiftRide
     python manage.py makemigrations
     python manage.py migrate
     
  
### 5. **Create a Superuser:**
  - Create an admin (superuser) account to access the Django admin panel:  
     ```bash
     python manage.py createsuperuser
     ```

### 6. **Run the Server:**
   - Start your Django development server to ensure that everything is configured correctly:
     ```bash
     python manage.py runserver
     ```

## Contact

For more information, please contact:

**Waleed Darwesh**  
**Email:** Waleeddarwesh2002@gmail.com 
**LinkedIn:** [Waleed Darwesh](https://www.linkedin.com/in/waleeddarwesh?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app) 

