# 🚀 Health AI - Android Setup & Connection Guide

## Issues Fixed ✅

1. **Connection Timeout (net::ERR_CONNECTION_TIMED_OUT)** - Android couldn't reach the backend
2. **Missing Favicon (404)** - Added SVG favicon to frontend
3. **API URL Configuration** - Auto-detect Android and route to correct server address

---
##########
## 🔧 What Was Changed

### 1. Android Network Security Configuration
- **File**: `frontend/android/app/src/main/res/xml/network_security_config.xml` (NEW)
- **Purpose**: Allows cleartext (HTTP) traffic to 10.0.2.2 for development
- **Updated**: `AndroidManifest.xml` to reference this config

### 2. Frontend API URL Detection
- **Updated Files**: 
  - `frontend/src/components/Login.js`
  - `frontend/src/components/HealthDashboard.js`
  - `frontend/src/components/HealthForm.js`
  - `frontend/src/components/HealthForm_Fixed.js`
- **Logic**: Auto-detects Android/mobile and uses `http://10.0.2.2:5000` instead of `localhost:5000`

### 3. Favicon Fix
- **Created**: `frontend/public/favicon.svg` (health heart icon)
- **Updated**: `frontend/public/index.html` to reference SVG favicon

### 4. Backend Configuration
- ✅ Already configured to listen on `0.0.0.0:5000` in:
  - `backend/app.py`
  - `backend/app_production.py`
  - `backend/app_enhanced.py`

---

## 📱 How to Run on Android Studio Emulator

### Step 1: Start the Backend Server
```bash
cd backend
python app.py
# OR use app_production.py for production environment
```
Output should show:
```
🚀 Starting Health AI Backend Server...
📍 Flask Debug Mode: False
* Running on http://0.0.0.0:5000
```

### Step 2: Build Frontend for Android
```bash
cd frontend
npm install  # if needed
npm run build  # creates optimized build
```

### Step 3: Open in Android Studio
```bash
cd frontend
npx cap add android  # if not already added
npx cap copy
npx cap open android
```

### Step 4: Run on Android Emulator
1. Click **Run** button in Android Studio
2. Select your emulator (API 29+ recommended)
3. Wait for app to build and deploy

### Step 5: Test Login
- **URL**: App will automatically use `http://10.0.2.2:5000/api/auth/login`
- **Test Credentials** (if using test_database setup):
  - Username: `testuser`
  - Password: `password123`
  - Email: `testuser@example.com`

---

## 🐛 Troubleshooting

### Connection Still Times Out?

1. **Verify Backend is Running**
   ```bash
   # On Windows (another terminal)
   curl http://localhost:5000/api/status
   # Should return 200 OK with JSON response
   ```

2. **Check Firewall**
   - Windows Defender may block port 5000
   - Add Python to Firewall exceptions:
     - Settings → Firewall → Allow an app through firewall
     - Find Python and enable both Private & Public

3. **Verify Emulator Network**
   ```bash
   # Inside Android emulator terminal (if available)
   ping 10.0.2.2
   ```

4. **Check Backend CORS**
   - Backend has `CORS(app, origins="*")` - all origins allowed ✅

### Favicon Still 404?

- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5 on desktop)
- Rebuild frontend: `npm run build`

### Cannot Find Android Emulator?

```bash
# List available emulators
emulator -list-avds

# Start an emulator
emulator -avd Pixel_4_API_30
```

---

## 📋 Special Notes for Physical Devices

For testing on a physical Android phone:

1. Find your computer's IP address:
   ```bash
   # Windows: Run ipconfig
   ipconfig
   # Look for IPv4 Address (usually 192.168.x.x)
   ```

2. Update `network_security_config.xml`:
   ```xml
   <domain includeSubdomains="true">192.168.x.x</domain>
   ```

3. Update API URL detection (optional, if environment variable approach preferred):
   ```js
   const API_BASE = process.env.REACT_APP_API_URL || 'http://192.168.x.x:5000';
   ```

4. Make sure device and computer are on **same WiFi network**

---

## 🔐 Production Deployment

For real production (HTTPS):

1. Use proper SSL certificates
2. Change `network_security_config.xml` to use HTTPS
3. Update backend to use HTTPS
4. Set `cleartextTrafficPermitted="false"`

---

## ✅ Verification Checklist

- [ ] Backend server running on `0.0.0.0:5000`
- [ ] Android emulator started
- [ ] Frontend built with `npm run build`
- [ ] App deployed to emulator
- [ ] Can see login screen (no 404 for favicon)
- [ ] Can submit login credentials
- [ ] Connection established (no timeout error)
- [ ] Dashboard loads after successful login

---

## 📞 Quick Command Reference

```bash
# Build backend environment
cd backend
pip install -r requirements_complete.txt

# Initialize database
python init_db.py

# Start backend
python app.py

# Build frontend
cd ../frontend
npm install
npm run build

# Open Android project
npx cap open android

# Test API connection
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

---

**Created**: April 24, 2026  
**Last Updated**: April 24, 2026
