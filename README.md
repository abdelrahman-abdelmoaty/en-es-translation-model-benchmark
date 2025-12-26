# Machine Translation Experiments

This repository contains experiments and evaluations for multiple machine translation models.  
The focus is on comparing different architectures using **BLEU score** as the primary evaluation metric.

---

## 🔗 Important Links

- 🌐 **Live Application**: [English to Spanish Translator](https://translation-app-production-0d36.up.railway.app/)
- 🔌 **Live API**: [API Base URL](https://translation-app-production-0d36.up.railway.app/api)
- 📄 **Reference**: [TF Tutorial](https://www.tensorflow.org/text/tutorials/nmt_with_attention)
- 💻 **Model Weights**:
  - **Transformer**: [Transformer (Hilsenki) Weights](https://www.kaggle.com/models/yassienwasfy/transformer/)
  - **RNN / LSTM / GRU**: [RNN/ LSTM/ GRU](https://www.kaggle.com/models/yassienwasfy/translation-weights/)

---

## 📊 BLEU Score Comparison

The following table summarizes the BLEU scores obtained by three different models on the same test set.

| Model   | Architecture       | BLEU Score |
| ------- | ------------------ | ---------- |
| Model 1 | (RNN + Attention)  | **20.67**  |
| Model 2 | (LSTM + Attention) | **21.47**  |
| Model 3 | (LSTM + Attention) | **24.06**  |

---

## 🧪 Evaluation Details

- **Metric**: BLEU (SacreBLEU)

---

## 🚀 Dockerized Translation Web Application

This repository includes a Dockerized FastAPI backend with a web frontend for English-to-Spanish translation using the Helsinki-NLP transformer model.

### Running Locally

**Prerequisites:**

- Docker installed

To run the application locally:

```bash
# Clone the repository
git clone https://github.com/abdelrahman-abdelmoaty/en-es-translation-model-benchmark.git
cd en-es-translation-model-benchmark/app

# Build and start the application
docker compose up --build
```

The application will be available at `http://localhost:8000`

To stop the application:

```bash
docker compose down
```

**Note:** The model files (~300 MB) are stored using Git LFS and will be automatically downloaded when you clone the repository.

### Project Structure

```
en-es-translation-model-benchmark/
├── app/                  # Web application directory
│   ├── backend/
│   │   ├── app/         # FastAPI application
│   │   ├── Dockerfile   # Backend container definition
│   │   └── requirements.txt
│   ├── frontend/        # HTML/CSS/JS frontend
│   ├── transformer-model/        # Transformer model files
│   ├── docker-compose.yml
│   └── Dockerfile       # Railway deployment Dockerfile
├── *.ipynb              # Jupyter notebooks (experiments)
└── README.md
```

### API Endpoints

The API and frontend are served directly by FastAPI:

- `GET http://localhost:8000/api/health` - Health check endpoint
- `POST http://localhost:8000/api/translate` - Translate English text to Spanish
- `GET http://localhost:8000/` - Frontend web interface

**Example API request (local):**

```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?"}'
```

**Example API request (live/production):**

```bash
# Health check
curl https://translation-app-production-0d36.up.railway.app/api/health

# Translation
curl -X POST https://translation-app-production-0d36.up.railway.app/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?"}'

# Translation with pretty output (requires jq)
curl -X POST https://translation-app-production-0d36.up.railway.app/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "The weather is nice today."}' | jq
```
