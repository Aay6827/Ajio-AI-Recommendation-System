# 🛍️ Ajio AI Recommendation System

A production-grade AI-powered product recommendation engine.

## 🚀 Live Demo
http://65.0.110.75:8000

## 🏗️ Architecture
```
GitHub Push → Jenkins → Docker Build → AWS ECR → AWS ECS → Live App
```

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| AI Model | TF-IDF + Cosine Similarity |
| Backend | FastAPI + Python |
| Database | PostgreSQL + AWS RDS |
| Container | Docker + AWS ECR |
| Deployment | AWS ECS Fargate |
| CI/CD | Jenkins + GitHub Webhooks |
| Frontend | HTML/CSS/JS |

## 📦 Features
- 120 products across 8 brands
- Real-time product recommendations
- RESTful API with FastAPI
- Automated CI/CD pipeline
- Cloud-native AWS deployment

## 🔧 Local Setup
```bash
git clone https://github.com/Aay6827/Ajio-AI-Recommendation-System.git
cd Ajio-AI-Recommendation-System/models/recommendation_model
docker-compose up --build
```

## 📡 API Endpoints
| Endpoint | Description |
|---|---|
| GET / | Frontend UI |
| GET /products | List all products |
| GET /recommend/{product} | Get recommendations |
| GET /docs | API documentation |

## 🏛️ Project Structure
```
Ajio-AI-Recommendation-System/
├── models/
│   └── recommendation_model/
│       ├── main.py          # FastAPI app
│       ├── recommender.py   # AI model
│       ├── products.csv     # Product data
│       ├── Dockerfile       # Container config
│       ├── docker-compose.yml
│       └── static/
│           └── index.html   # Frontend
├── Jenkinsfile              # CI/CD pipeline
└── README.md
```

## 👨‍💻 Author
Aayush Tiwari