# Machine Translation Experiments

This repository contains experiments and evaluations for multiple machine translation models.  
The focus is on comparing different architectures using **BLEU score** as the primary evaluation metric.

---

## 🔗 Important Links

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

This repository now includes a Dockerized FastAPI backend with a web frontend for English-to-Spanish translation using the Helsinki-NLP transformer model.

### Prerequisites

- Docker and Docker Compose installed
- The `app/transformer-model/` directory with extracted model files

### Getting the Model Files

The transformer model files (~300 MB) are required to run the application. Choose one of the following options:

#### Option 1: Extract from Local Tar File (If you have it)

If you have the `Transformer TensorFlow 2 Default v1.tar.gz` file:

```bash
# Extract the model to the app directory
tar -xzf "Transformer TensorFlow 2 Default v1.tar.gz" -C app/
mv app/my-model app/transformer-model
```

#### Option 2: Download from Kaggle

The model weights are available on Kaggle:

- **Transformer Model**: [Kaggle Models - Transformer (Helsinki)](https://www.kaggle.com/models/yassienwasfy/transformer/)

After downloading, extract to `app/transformer-model/`

#### Option 3: Use Git LFS (For Repository Maintainers)

If you want to include model files in the repository using Git LFS:

```bash
# Install Git LFS
brew install git-lfs  # macOS
# or
sudo apt install git-lfs  # Linux

# Initialize Git LFS
git lfs install

# Track model files
git lfs track "app/transformer-model/*.h5"
git lfs track "app/transformer-model/**"

# Add and commit
git add .gitattributes
git add app/transformer-model/
git commit -m "Add model files via Git LFS"
```

**Note:** Git LFS has storage quotas on free GitHub accounts (1 GB storage, 1 GB bandwidth/month).

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
│   └── nginx.conf
├── *.ipynb              # Jupyter notebooks (experiments)
└── README.md
```

### API Endpoints

The API can be accessed in two ways:

**Via Nginx (recommended for frontend):**

- `GET http://localhost/api/health` - Health check endpoint
- `POST http://localhost/api/translate` - Translate English text to Spanish

**Direct API access (bypassing nginx):**

- `GET http://localhost:8000/health` - Health check endpoint
- `POST http://localhost:8000/translate` - Translate English text to Spanish

**Example API request:**

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?"}'
```

Or via nginx:

```bash
curl -X POST http://localhost/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?"}'
```

## 📦 Running the Application

This is the easiest way to run the application with all dependencies containerized.

#### Step 1: Navigate to the app directory

```bash
cd app
```

#### Step 2: Build and start the application

```bash
docker-compose up --build
```

This will:

- Build the backend Docker image (includes model files)
- Start the FastAPI backend container
- Start the Nginx frontend container
- Set up networking between services

#### Step 3: Access the application

- Open your browser and navigate to `http://localhost`
- The frontend will be served on port 80
- The API backend runs on port 8000 (internal, proxied through Nginx)

#### Step 4: Stop the application

```bash
# Press Ctrl+C in the terminal, or in a new terminal:
docker-compose down
```

#### Additional Docker Commands

```bash
# Run in detached mode (background)
docker-compose up -d --build

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f nginx

# Stop and remove containers
docker-compose down

# Stop and remove containers, volumes, and images
docker-compose down -v --rmi all

# Rebuild without cache
docker-compose build --no-cache
```
