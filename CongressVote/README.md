# CongressVote

A comprehensive web application for tracking and managing congressional voting records. Built with FastAPI (backend) and React (frontend).

## Features

- **User Authentication**: Secure login and registration system
- **Congress Member Management**: Track all members of Congress with detailed profiles
- **Bill Tracking**: Monitor bills through their legislative journey
- **Vote Recording**: Record and analyze voting patterns
- **Interactive Dashboard**: Visualize voting statistics and trends
- **Real-time Updates**: Track voting as it happens
- **Party Analysis**: See voting patterns by party affiliation
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- PostgreSQL - Database
- JWT Authentication - Secure user authentication
- Alembic - Database migrations

### Frontend
- React 18 - UI library
- Material-UI - Component library
- Redux Toolkit - State management
- Recharts - Data visualization
- Axios - HTTP client

## Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- Redis (optional, for caching)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/CongressVote.git
cd CongressVote
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Edit .env file with your database credentials
# Update DATABASE_URL and SECRET_KEY
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb congressvote

# Run database migrations
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
```

## Running the Application

### Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### Start Frontend Development Server

```bash
cd frontend
npm start
```

The application will be available at: http://localhost:3000

## Default Admin User

To create an admin user, you can use the API or run this Python script:

```python
from app.database import SessionLocal
from app.models import User
from app.services.auth import get_password_hash

db = SessionLocal()
admin_user = User(
    username="admin",
    email="admin@congressvote.com",
    hashed_password=get_password_hash("admin123"),
    is_superuser=True
)
db.add(admin_user)
db.commit()
db.close()
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Users
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update current user

### Congress Members
- `GET /api/congress-members` - List all members
- `GET /api/congress-members/{id}` - Get member details
- `POST /api/congress-members` - Create member (admin only)
- `PUT /api/congress-members/{id}` - Update member (admin only)
- `DELETE /api/congress-members/{id}` - Delete member (admin only)

### Bills
- `GET /api/bills` - List all bills
- `GET /api/bills/{id}` - Get bill details
- `POST /api/bills` - Create bill (admin only)
- `PUT /api/bills/{id}` - Update bill (admin only)
- `DELETE /api/bills/{id}` - Delete bill (admin only)

### Votes
- `GET /api/votes` - List all votes
- `GET /api/votes/stats/{bill_id}` - Get voting statistics for a bill
- `POST /api/votes` - Record vote (admin only)
- `PUT /api/votes/{id}` - Update vote (admin only)
- `DELETE /api/votes/{id}` - Delete vote (admin only)

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/congressvote
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Production Deployment

### Backend
1. Use production database (PostgreSQL)
2. Set secure SECRET_KEY
3. Enable HTTPS
4. Use production WSGI server (Gunicorn)
5. Set up reverse proxy (Nginx)

### Frontend
1. Build production bundle: `npm run build`
2. Serve static files with web server
3. Configure environment variables
4. Enable gzip compression
5. Set up CDN for assets

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI documentation
- React documentation
- Material-UI components
- Congressional data sources