# WasteNot

WasteNot is a full-stack web application that facilitates community-based item sharing and waste reduction. The platform enables users to give away items they no longer need, helping reduce landfill waste while fostering community connections.


![Landing page](./wastenot_backend/assets/Screenshot%202025-09-28%20at%202.16.47 PM.png)

## Features

### User Management
- **-->User registration and authentication**: Users can easily create new accounts and securely log in to access personalized features. The system supports robust authentication mechanisms to protect user data.
- **Personalized user dashboard**: Each user gets a dedicated dashboard to manage their posted items, view exchange history, track messages, and update their profile settings.
- **Profile management**: Users can update their personal information, contact details, and preferences, ensuring their profile accurately reflects their current status.

### Item Management
- **Post items with multiple images**: Users can list items they wish to give away, including the ability to upload multiple images to provide a comprehensive visual representation of the item's condition.
- **Automatic item condition analysis using Google Cloud Vision API**: Leveraging the Google Cloud Vision API, the platform automatically analyzes uploaded item images to assess their condition, providing objective insights to potential recipients.
- **QR code generation for item pickup verification**: For each posted item, a unique QR code is generated. This QR code serves as a secure verification method for item pickups, ensuring that only the intended recipient can claim the item.
- **Browse available items with search and filtering**: Users can easily discover items through a comprehensive browsing interface, enhanced with powerful search capabilities and various filtering options (e.g., category, condition, distance).
- **Location-based item discovery**: Integrated with mapping services, users can find items available in their vicinity or within a specified radius, making local exchanges convenient and efficient.

### Communication
- **In-app messaging system between users**: A secure and intuitive in-app messaging system allows users to communicate directly with each other regarding items, exchange details, and any other relevant inquiries.
- **Email notifications for new messages**: Users receive real-time email notifications for new messages, ensuring they stay informed and can respond promptly to inquiries.
- **File attachment support in messages**: The messaging system supports file attachments, enabling users to share additional images, documents, or other relevant files during their conversations.

### Exchange Management
- **Schedule item pickups**: Users can coordinate and schedule convenient pickup times and locations for items they wish to exchange, streamlining the handover process.
- **Confirm exchanges using QR codes**: Upon pickup, both parties can use the generated QR code to confirm the exchange, providing a secure and verifiable record of the transaction.
- **Exchange history tracking**: The platform maintains a detailed history of all past exchanges, allowing users to review their giving and receiving activities.
- **Real-time status updates**: Users receive real-time updates on the status of their exchanges, from initial scheduling to successful completion, ensuring transparency and clarity throughout the process.

### Location Services
- **Interactive map interface**: An interactive map interface allows users to visually explore available items based on their geographical location, enhancing the discovery experience.
- **Location-based item search**: Users can search for items within specific geographical areas, making it easy to find items close to their home, work, or any other preferred location.
- **Automatic geolocation detection**: The application can automatically detect the user's current location, providing a personalized and relevant item browsing experience.
- **Custom location input**: Users have the flexibility to manually input custom locations, allowing them to search for items in areas beyond their current geolocation.

## Tech Stack

### Frontend
- **HTML5/CSS3**: Modern web standards for structuring and styling the user interface, ensuring a responsive and visually appealing experience across devices.
- **JavaScript**: Powers the interactive elements and dynamic functionalities of the frontend, providing a rich user experience.
- **Tailwind CSS**: A utility-first CSS framework that enables rapid UI development with highly customizable and efficient styling.
- **GSAP Animations**: GreenSock Animation Platform (GSAP) is used for creating high-performance and complex animations, enhancing the visual appeal and user engagement.
- **MapBox for mapping**: Integrated for robust and interactive mapping functionalities, enabling location-based features and item discovery.
- **Swiper.js for carousels**: A modern touch slider that provides smooth and responsive image carousels for displaying multiple item images.

### Backend
- **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design, forming the core of the backend.
- **Django REST Framework**: A powerful and flexible toolkit for building Web APIs, used to create the RESTful endpoints for the WasteNot application.
- **MySQL Database**: A robust and widely used relational database management system for storing all application data, including user profiles, item details, and exchange records.
- **Python**: The primary programming language for the backend, known for its readability, versatility, and extensive libraries.

### APIs and Services
- **Google Cloud Vision API for image analysis**: Utilized for advanced image processing, specifically for automatically analyzing and determining the condition of posted items.
- **MapBox API for location services**: Provides comprehensive mapping and geolocation services, powering the interactive map, location-based search, and automatic geolocation detection.
- **QR Code generation**: Integrated service for generating unique QR codes for item pickup verification, enhancing security and streamlining the exchange process.
- **Email service integration**: Enables the sending of automated email notifications for new messages, password resets, and other important system alerts.

### Authentication
- **Django Authentication System**: Leverages Django's built-in, secure authentication system for managing user accounts, sessions, and permissions.
- **Session-based authentication**: Implements session-based authentication to maintain user login status and provide a seamless user experience.
- **Password reset functionality**: Provides a secure and user-friendly mechanism for users to reset forgotten passwords.

## Security Features
- **CSRF protection**: Cross-Site Request Forgery (CSRF) protection is implemented to safeguard against malicious attacks that attempt to trick authenticated users into submitting requests they did not intend.
- **Secure password handling**: User passwords are securely hashed and stored using industry-standard cryptographic techniques, preventing unauthorized access.
- **Protected user data**: All sensitive user data is encrypted and protected, ensuring privacy and compliance with data protection regulations.
- **Secure file uploads**: File upload mechanisms are designed with security in mind, including validation and sanitization to prevent malicious file injections.

## Requirements
- **Python 3.x**: The application requires Python version 3.x to run the backend services and scripts.
- **Django 4.2+**: The backend framework is built on Django 4.2 or a later version.
- **MySQL**: A MySQL database instance is required for data storage.
- **Google Cloud Vision API credentials**: Valid API credentials for Google Cloud Vision are necessary for the item condition analysis feature.
- **MapBox API key**: A valid MapBox API key is required for all location-based services and interactive maps.


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

1.  **Clone the repository**: Begin by cloning the WasteNot project repository to your local machine using Git.
    ```sh
    git clone https://github.com/your-username/wastenot.git
    cd wastenot
    ```
2.  **Install dependencies**: Navigate to the `wastenot_backend` directory and install all required Python packages using pip.
    ```sh
    cd wastenot_backend
    pip install -r requirements.txt
    ```
3.  **Configure environment variables**: Create a `.env` file in the `wastenot_backend` directory based on the `.env.example` file. Populate it with your database credentials, Google Cloud Vision API key, MapBox API key, and email service configurations.
4.  **Set up the database**: Apply database migrations to create the necessary tables and schema in your MySQL database.
    ```sh
    python manage.py migrate
    ```
5.  **Run the development server**: Start the Django development server to access the application locally.
    ```sh
    python manage.py runserver
    ```

## Contributing

For contributions, please submit a pull request to the `main` branch. Ensure your code adheres to the project's established coding standards, includes comprehensive tests for new features or bug fixes, and passes all existing tests. Detailed guidelines for contributing can be found in `CONTRIBUTING.md` (if available).
