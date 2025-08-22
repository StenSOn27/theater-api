# 🎭 Theater API
**Theater API** is a RESTful API service for managing theaters, built with **Django REST Framework (DRF)**.

## 📌 Key Features
- 🔐 JWT Authentication
- 🛠️ Admin Panel: `/admin/`
- 📄 API Documentation: `/api/theater/doc/swagger/`
- 🎟️ Manage reservations and tickets
- 🎬 Create plays with genres and actors
- 🏛️ Manage theater halls
- 🕒 Add performance sessions
- 🔍 Filter plays and performances by: title, genre, actor, date

## 🧩 Architecture Overview

### ▶️ PlayViewSet
Filter plays by title, genres, and actors:
?title=hamlet&genres=1,2&actors=3

Upload an image to a play:
/api/theater/plays/{id}/upload-image/

Uses serializers:
- `PlayListSerializer`
- `PlayDetailSerializer`
- `PlayImageSerializer`

### 🎭 PerformanceViewSet
Annotates available tickets using:
F("theater_hall__rows") * F("theater_hall__seats_in_row") - Count("tickets")

Filter by:
?play=1&date=2025-08-22

### 🧾 ReservationViewSet
- Accessible only to authenticated users  
- Supports: `create`, `list`, `retrieve`, `delete`  
- Results are paginated (10 per page)

### 📚 Other ViewSets
- `GenreViewSet`  
- `ActorViewSet`  
- `TheaterHallViewSet`  

## 🛠️ Installation via GitHub
⚠️ **PostgreSQL is required**. Create a database before running the app.
```bash
# Clone the repo
git clone https://github.com/StenSOn27/theater-api.git
cd theater-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>

# Apply database migrations
python manage.py migrate

# Run the server
python manage.py runserver

🐳 Run with Docker
Docker should be installed.

docker-compose build
docker-compose up

Obtain JWT tokens:
POST /api/user/token/
{
  "username": "your_username",
  "password": "your_password"
}
Add to request headers:
Authorization: Bearer <your_token>

📫 Contact
Author: StenSOn27