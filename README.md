# WasteNot

WasteNot is a full-stack web application that facilitates community-based item sharing and waste reduction. The platform enables users to give away items they no longer need, helping reduce landfill waste while fostering community connections.


![Landing page](./wastenot_backend/assets/Screenshot%202025-09-28%20at%202.16.47 PM.png)

## Features

### User Management
- User registration and authentication
- Personalized user dashboard
- Profile management

### Item Management
- Post items with multiple images
- Automatic item condition analysis using Google Cloud Vision API
- QR code generation for item pickup verification
- Browse available items with search and filtering
- Location-based item discovery

### Communication
- In-app messaging system between users
- Email notifications for new messages
- File attachment support in messages

### Exchange Management
- Schedule item pickups
- Confirm exchanges using QR codes
- Exchange history tracking
- Real-time status updates

### Location Services
- Interactive map interface
- Location-based item search
- Automatic geolocation detection
- Custom location input

## Tech Stack

### Frontend
- HTML5/CSS3
- JavaScript
- Tailwind CSS
- GSAP Animations
- MapBox for mapping
- Swiper.js for carousels

### Backend
- Django
- Django REST Framework
- MySQL Database
- Python

### APIs and Services
- Google Cloud Vision API for image analysis
- MapBox API for location services
- QR Code generation
- Email service integration

### Authentication
- Django Authentication System
- Session-based authentication
- Password reset functionality

## Security Features
- CSRF protection
- Secure password handling
- Protected user data
- Secure file uploads

## Requirements
- Python 3.x
- Django 4.2+
- MySQL
- Google Cloud Vision API credentials
- MapBox API key


## Project Structure

``` sh
wastenot/
├── wastenot_backend/
│   ├── core/
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
│   ├── templates/
│   │   ├── messages/
│   │   └── registration/
│   ├── wastenot_backend/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── .gitignore
│   ├── manage.py
│   └── requirements.txt
├── .env
├── .gitignore
├── gcloud-key.json
├── key.py
├── README.md
└── w1.html

```

## Installation

1. Clone the repository
2. Install dependencies:
```sh
pip install -r requirements.txt
```
3. Configure environment variables
4. Set up the database:
```sh
python manage.py migrate
```
5. Run the development server:
```sh
python manage.py runserver
```

## Contributing

For contributions, please submit a pull request. Ensure your code follows the project's coding standards and includes appropriate tests.
