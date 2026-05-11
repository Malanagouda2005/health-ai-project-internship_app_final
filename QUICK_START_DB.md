# 🗄️ Database Connection - Quick Start Guide

## ✅ What's Been Set Up

Your Health AI project now has a complete database system for:
- ✓ **User Authentication** - Secure login/registration
- ✓ **User Profiles** - Store patient information
- ✓ **Medical History** - Track health records and AI predictions
- ✓ **Session Management** - JWT-based authentication

## 🚀 Quick Start

### 1. Start the Backend Server

```bash
cd backend
python app.py
```

You should see:
```
✓ Database tables initialized successfully
🚀 Starting Health AI Backend Server...
 * Running on http://0.0.0.0:5000
```

### 2. Test User Credentials (for development)

```
Username: testuser
Password: password123
Email: testuser@example.com
```

## 📋 API Endpoints

### Authentication

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register` | Create new user account |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/profile` | Get user profile |
| PUT | `/api/auth/profile` | Update profile |
| POST | `/api/auth/change-password` | Change password |
| DELETE | `/api/auth/delete-account` | Delete account |
| POST | `/api/auth/logout` | Logout |

### Medical History

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/auth/medical-history` | Get all medical records |
| POST | `/api/auth/medical-history` | Add new record |
| GET | `/api/auth/medical-history/{id}` | Get specific record |
| PUT | `/api/auth/medical-history/{id}` | Update record |
| DELETE | `/api/auth/medical-history/{id}` | Delete record |

## 🧪 Test the API

### Register New User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "Password123!",
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "gender": "M"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "Password123!"
  }'
```

Response will include a `token`. Use it for authenticated requests:

```bash
TOKEN="<token_from_login>"
```

### Get User Profile
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Add Medical Record
```bash
curl -X POST http://localhost:5000/api/auth/medical-history \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "record_type": "general",
    "blood_type": "O+",
    "allergies": "Penicillin",
    "blood_pressure": "120/80",
    "heart_rate": 72,
    "temperature": 98.6,
    "weight": 70.5,
    "height": 175.0,
    "consultation_notes": "Annual checkup"
  }'
```

### Get Medical History
```bash
curl -X GET http://localhost:5000/api/auth/medical-history \
  -H "Authorization: Bearer $TOKEN"
```

## 🗂️ Database Files

**Location:** `backend/health_ai.db` (SQLite database)

### Database Tables
1. **users** - User accounts and profiles
2. **medical_histories** - Medical records
3. **sessions** - Session tokens and tracking

## 🔑 Features

### Automatic Password Hashing
- Passwords are never stored in plain text
- Uses bcrypt-like hashing via Werkzeug
- Verified on login

### JWT Authentication
- 24-hour token expiration (configurable)
- Stateless authentication
- Secure token validation

### Medical Record Storage
- Symptoms and predictions
- Medical images (skin/X-ray)
- Vital signs tracking
- Doctor notes
- Health conditions history
- Medication tracking
- Allergy records

## 📝 Integration Steps

### 1. Update Frontend Login Form
Send credentials to `/api/auth/login`:
```javascript
fetch('/api/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username, password})
})
.then(r => r.json())
.then(data => localStorage.setItem('token', data.token))
```

### 2. Use Token in Authenticated Requests
```javascript
const token = localStorage.getItem('token');
fetch('/api/auth/medical-history', {
  headers: {'Authorization': `Bearer ${token}`}
})
```

### 3. Save Predictions to Medical History
After AI model prediction, save results:
```javascript
fetch('/api/auth/medical-history', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    record_type: 'symptom_check',
    symptoms: ['cough', 'fever'],
    symptom_predictions: prediction_result
  })
})
```

## ⚙️ Configuration

### Environment Variables (.env)
```
DATABASE_URL=sqlite:///health_ai.db
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
```

### Production Checklist
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Switch to PostgreSQL/MySQL database
- [ ] Enable HTTPS only
- [ ] Set `FLASK_DEBUG=False`
- [ ] Add CORS domain restrictions
- [ ] Enable rate limiting
- [ ] Set up database backups
- [ ] Add email verification
- [ ] Implement password reset

## 🐛 Troubleshooting

### Database Locked Error
```bash
# Delete the database and reinitialize
rm backend/health_ai.db
python backend/init_db.py
```

### Token Expired Error
- Tokens expire after 24 hours
- User needs to login again to get new token

### Permission Denied on API
- Check if token is included in `Authorization` header
- Token format should be: `Bearer <token>`

## 📚 Files Reference

| File | Purpose |
|------|---------|
| `models.py` | Database models (User, MedicalHistory, Session) |
| `auth.py` | Authentication utilities and decorators |
| `auth_routes.py` | All auth and medical history endpoints |
| `init_db.py` | Database initialization script |
| `test_database.py` | API testing script |
| `.env.example` | Environment variable template |
| `DATABASE_SETUP.md` | Detailed setup documentation |

## 🎯 Next Steps

1. ✅ Start Flask backend: `python app.py`
2. ✅ Test API endpoints with provided curl commands
3. ✅ Integrate authentication into React frontend
4. ✅ Connect medical record storage to AI prediction endpoints
5. ✅ Add user dashboard to display medical history
6. ✅ Implement medical record visualization

## 📞 Support

For detailed documentation, see: `DATABASE_SETUP.md`

For API testing: `python backend/test_database.py` (requires running Flask server)
