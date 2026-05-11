<<<<<<< HEAD
# Health AI Prediction System

A comprehensive machine learning-based health diagnostic system that provides predictions for skin diseases, chest X-ray analysis, and symptom-based disease detection.

## Features

- **Login System**: Secure authentication before accessing the system
- **Skin Disease Detection**: Upload skin images to identify 22 different skin conditions
- **Chest X-Ray Analysis**: Analyze X-ray images for pneumonia detection
- **Symptom-based Disease Prediction**: Predict diseases based on reported symptoms from 41 possible conditions
- **Modern React Frontend**: User-friendly interface with tabbed navigation
- **REST API Backend**: Flask-based API with ML model integration
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
health-ai-project-internship/
├── backend/                 # Flask API backend
│   ├── app.py              # Main Flask application
│   ├── train_symptoms.py   # Symptom model training script
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment configuration
│   ├── README.md          # Backend documentation
│   ├── symptom_model.pkl  # Trained symptom prediction model
│   ├── symptom_encoder.pkl # Label encoder for diseases
│   └── symptom_features.pkl # Feature names
├── frontend/               # React frontend
│   ├── public/
│   │   ├── index.html     # Main HTML template
│   │   └── manifest.json  # PWA manifest
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js   # Login component
│   │   │   ├── Login.css  # Login styles
│   │   │   ├── HealthForm.js # Main form component
│   │   │   └── HealthForm.css # Form styles
│   │   ├── App.js         # Main app component
│   │   ├── App.css        # App styles
│   │   ├── index.js       # App entry point
│   │   └── index.css      # Global styles
│   ├── package.json       # React dependencies
│   ├── README.md          # Frontend documentation
│   └── start_frontend.bat # Windows startup script
├── model/                  # ML models and training scripts
│   ├── app.py             # Original skin model API
│   ├── skin_model.py      # Skin model training
│   ├── xray_model.py      # X-ray model training
│   ├── skin_model.h5      # Trained skin disease model
│   └── xray_model.h5      # Trained X-ray model
├── data/                   # Datasets and raw data
│   ├── raw/
│   │   ├── Training.csv   # Symptom training data
│   │   └── Testing.csv    # Symptom testing data
│   └── datasets/          # Image datasets
│       ├── chest_xray/    # X-ray images
│       └── SkinDisease/   # Skin disease images
├── Symtom2Disease.csv     # Additional symptom data
├── Flow-chart.*           # Project flowcharts
├── start_frontend.bat     # Frontend startup script
└── README.md             # This file
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Virtual environment (recommended)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The backend API will be available at `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 3. Alternative Startup (Windows)

You can also use the provided batch files:

```bash
# Start backend
backend\run_server.bat

# Start frontend (in another terminal)
frontend\start_frontend.bat
```

## Usage

1. **Login**: Use any username and password to log in
2. **Personal Information**: Fill in your basic details
3. **Medical History**: Provide your medical background
4. **Symptoms**: Select symptoms from the comprehensive checklist
5. **Image Analysis**: Upload skin images or X-rays for analysis
6. **Results**: View predictions from all analyses

## API Endpoints

### GET /
Returns API information and available endpoints.

### POST /predict/skin
Predict skin diseases from images.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `image` (file)

**Response:**
```json
{
  "prediction": "Psoriasis",
  "confidence": 0.95,
  "all_probabilities": [0.01, 0.02, ..., 0.95]
}
```

### POST /predict/xray
Analyze chest X-rays for pneumonia.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `image` (file)

**Response:**
```json
{
  "prediction": "PNEUMONIA",
  "confidence": 0.87,
  "all_probabilities": [0.13, 0.87]
}
```

### POST /predict/symptoms
Predict diseases based on symptoms.

**Request:**
- Method: POST
- Content-Type: application/json
- Body:
```json
{
  "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions"]
}
```

**Response:**
```json
{
  "prediction": "Fungal infection",
  "top_predictions": [
    {"disease": "Fungal infection", "probability": 0.85},
    {"disease": "Allergy", "probability": 0.12},
    {"disease": "Drug Reaction", "probability": 0.03}
  ]
}
```

### POST /train/symptoms
Retrain the symptom prediction model.

## Model Details

### Skin Disease Model
- **Type**: Convolutional Neural Network (CNN)
- **Framework**: TensorFlow/Keras
- **Input**: RGB images (224x224)
- **Classes**: 22 skin conditions
- **Accuracy**: High (depends on training data)

### Chest X-Ray Model
- **Type**: Convolutional Neural Network (CNN)
- **Framework**: TensorFlow/Keras
- **Input**: RGB images (224x224)
- **Classes**: NORMAL, PNEUMONIA
- **Accuracy**: High (depends on training data)

### Symptom Prediction Model
- **Type**: Random Forest Classifier
- **Framework**: scikit-learn
- **Features**: 132 binary symptom features
- **Classes**: 41 diseases
- **Accuracy**: 100% on training data

## Configuration

### Environment Variables (.env)

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# API Keys (add your keys here)
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here

# Database Configuration (if needed)
DATABASE_URL=sqlite:///health_ai.db

# Model Configuration
MODEL_DIR=../model
DATA_DIR=../data

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

## Development

### Backend Development
- The backend is built with Flask and TensorFlow
- Models are loaded on startup for fast inference
- CORS is enabled for frontend communication
- Error handling and logging included

### Frontend Development
- Built with React 18 and modern hooks
- Responsive design with CSS Grid and Flexbox
- Real-time API integration
- Component-based architecture

## Security Notes

- This is a demonstration system and should not be used for actual medical diagnosis
- Always consult healthcare professionals for medical advice
- The models may have limitations and biases based on training data
- In production, implement proper authentication and authorization
- Use HTTPS for secure communication
- Validate all user inputs on both frontend and backend

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please check individual model licenses and data usage rights.
=======
# intership-project-health-risk-pridiction
A machine learning-based web application that predicts potential health risks based on user input data. The system uses trained models to analyze patterns and provide insights, helping users make informed health decisions.
# 🏥 Health AI Prediction System

A full-stack healthcare application that predicts diseases using **medical images** and **patient symptoms/reports**.

---

## 🚀 Features

* 🧠 Disease prediction from **medical images (X-ray/MRI)**
* 📝 Prediction based on **symptoms / medical reports**
* 🔗 Combined result for better accuracy
* 💻 Modern React-based user interface
* ⚙️ Flask backend API
* 🚀 GPU-supported model training (TensorFlow)

---

## 🛠️ Tech Stack

### Frontend

* React.js
* HTML, CSS, JavaScript

### Backend

* Python
* Flask

### Machine Learning

* TensorFlow / Keras (CNN for images)
* Scikit-learn (NLP model for text)

---

## 📂 Project Structure

health-ai-project/
│
├── frontend/        # React app
├── backend/         # Flask API
├── model/           # Training scripts
├── dataset/         # Data (not uploaded)
├── README.md

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Malanagouda2005/intership-project-health-risk-pridiction.git
cd intership-project-health-risk-pridiction
```

---

### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## 🧪 How It Works

1. User uploads a medical image
2. User enters symptoms
3. Image model predicts disease
4. Text model predicts disease
5. Backend combines results
6. Final prediction is displayed

---

## 📊 Example Output

* Disease: Pneumonia
* Confidence: 75%
* Risk Level: High

---

## 👥 Collaboration

Contributors can:

* Fork the repository
* Create a new branch
* Submit a pull request
>>>>>>> 52f6b9a4ad6da758be7148daf4b2635896479880

---

## ⚠️ Note

* Datasets are not included in the repository
* Models must be trained before running

---

## 📌 Future Improvements

* Use advanced models (ResNet, BERT)
* Improve UI/UX
* Add real-time doctor recommendations
* Deploy to cloud

---

## 🙌 Author

**Mallanagouda Hosamani**<br>
**vinay kumabar**<br>
**shaskank mk**<br>

---

## ⭐ Support

If you like this project, please ⭐ the repository!
