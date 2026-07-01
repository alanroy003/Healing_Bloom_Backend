# Healing Bloom - Backend

This repository contains the backend code for the **Healing Bloom** app, built using **Django** as the framework and **PostgreSQL** as the database. The backend handles user profile management, skin disease identification, and medicine cure recommendations. It serves the Flutter frontend via RESTful APIs.

## 🔗 Repositories

| Component                     | Repository Link                                                              |
| :---------------------------- | :--------------------------------------------------------------------------- |
| **📱 Frontend (Flutter)**     | [Healing Bloom App](https://github.com/yourusername/healing_bloom)           |
| **🖥️ Backend** | [Healing Bloom Backend](https://github.com/alanroy003/Healing_Bloom_Backend) |

## Features

- **User Profile Management**: Handles user registration, login, and profile management.
- **Skin Disease Identification**: Analyzes images of skin conditions and identifies possible diseases using AI/ML models.
- **Medicine Cure Recommendations**: Provides personalized medicine recommendations based on skin condition identification.
- **API Endpoints**: Exposes RESTful APIs to interact with the frontend.

## Requirements

- **Python**: Version 3.8 or higher  
- **Django**: Version 3.x or higher  
- **PostgreSQL**: Database for storing user data and app information  
- **Django REST Framework**: For creating the APIs

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Alan21303/Healing_Bloom_Backend.git
cd Healing_Bloom_Backend
```

### Step 2: Set Up the Python Environment

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Set Up PostgreSQL Database

1. Install **PostgreSQL** and create a new database.
2. Update the `DATABASES` settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Run migrations:

```bash
python manage.py migrate
```

### Step 4: Start the Development Server

```bash
python manage.py runserver
```

The API will be available at:  
`http://127.0.0.1:8000/`

---

## API Endpoints

### User Profile

- `POST /api/register/`: Register a new user  
- `POST /api/login/`: Login and receive authentication token  
- `GET /api/profile/`: Retrieve user profile  
- `PUT /api/profile/`: Update profile

### Skin Disease Identification

- `POST /api/skin-disease/`: Upload image and receive disease prediction

### Medicine Cure Recommendations

- `POST /api/medicine-recommendation/`: Get medicine suggestions based on disease

---

## Rust Integration

Rust is used to run machine learning models and perform high-performance image processing.

- **Setup**: Rust is integrated into Django using bindings like `PyO3`.
- **Functionality**: Image input is processed in Rust to generate disease predictions, which are returned to Django for further handling.

---

## Future Enhancements

- Improved disease prediction accuracy with better models  
- User history tracking and analytics  
- Secure authentication via JWT or OAuth2  

---

## Contributing

Contributions are welcome!

```bash
git checkout -b feature-branch
git commit -m "Add new feature"
git push origin feature-branch
```

Then open a pull request.

---

