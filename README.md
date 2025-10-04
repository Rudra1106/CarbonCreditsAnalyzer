# 🌱 TerraCredit AI

> **"From Farmland to Future Income"**

AI-powered carbon credit potential analyzer for Indian farmers. Upload a photo of your land, get instant analysis, revenue projections, and professional reports - all in minutes.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Cost Analysis](#cost-analysis)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

TerraCredit AI democratizes access to carbon credit markets by providing instant, AI-powered assessments of farmland's carbon sequestration potential. Traditional carbon credit analysis requires expensive consultants and months of waiting. We deliver preliminary assessments in 30 seconds.

### Problem We Solve

- **High Entry Barriers**: Professional carbon credit assessments cost ₹5-20 lakhs
- **Information Gap**: Farmers don't know if their land qualifies
- **Complex Process**: Understanding carbon credits requires technical expertise
- **Regional Variations**: Climate zones affect earning potential significantly

### Our Solution

Upload a farmland image + location → Get instant analysis with:
- CO2 sequestration estimates
- Revenue projections (1, 5, 10 years)
- Location-adjusted calculations
- Professional reports
- AI chatbot for questions

---

## ✨ Features

### 1. **Image Analysis** (Llama 3.2 Vision)
- Identifies vegetation type (forest, cropland, grassland, mixed)
- Measures vegetation density (0-100%)
- Assesses land condition (excellent to poor)
- Counts visible trees
- Estimates visible land area

### 2. **Location Intelligence**
- Real-time weather integration (OpenWeatherMap)
- 28 Indian states with climate zone multipliers
- Temperature and humidity adjustments
- Regional carbon sequestration rate variations

### 3. **Carbon Calculations**
- Annual CO2 sequestration (tons/year)
- Carbon credit generation estimates
- Revenue projections in INR (conservative/mid/optimistic)
- Confidence scoring (high/medium/low)
- Detailed calculation breakdown

### 4. **Professional Reports** (GPT-4o)
- Executive summary
- Full analysis report (Markdown)
- WhatsApp-ready text summary
- Recommendations and next steps
- Indian carbon program guidance (CAMPA, Verra, Gold Standard)

### 5. **AI Chatbot** (Mistral 8x7B)
- Full report context awareness
- Answers questions about user's specific analysis
- Web search for latest information (SerpApi)
- Multi-turn conversations
- Personalized suggestions

---

## 🛠 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | REST API server |
| **Vision AI** | Llama 3.2 11B Vision (OpenRouter) | Image analysis |
| **Report Generation** | GPT-4o (OpenAI) | Professional reports |
| **Chatbot** | Mistral 8x7B (OpenRouter) | Q&A assistant |
| **Weather API** | OpenWeatherMap | Climate data |
| **Web Search** | SerpApi | Current information |
| **Image Processing** | Pillow | Image optimization |
| **HTTP Client** | httpx | Async API calls |

---

## 📁 Project Structure

```
carbon-credit-analyzer/
├── backend/
│   ├── main.py                      # FastAPI application
│   ├── .env                         # Environment variables (DO NOT COMMIT)
│   ├── requirements.txt             # Python dependencies
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_processor.py       # Image handling & validation
│   │   ├── ai_client.py             # Llama Vision integration
│   │   ├── carbon_calculator.py     # Carbon calculations
│   │   ├── location_service.py      # Weather & climate data
│   │   ├── report_generator.py      # GPT-4o report generation
│   │   └── chatbot_service.py       # Mistral chatbot
│   └── models/
│       ├── __init__.py
│       └── schemas.py               # Pydantic data models
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- pip
- API Keys (see Configuration section)

### Steps

1. **Clone Repository**
```bash
git clone <your-repo-url>
cd carbon-credit-analyzer/backend
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Run Server**
```bash
uvicorn main:app --reload
```

Server runs at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

---

## 🔑 Configuration

Create `.env` file with the following:

```env
# Required - Vision & Chatbot
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Required - Report Generation
OPENAI_API_KEY=sk-proj-your-key-here

# Optional - Location Features (recommended)
OPENWEATHER_API_KEY=your-key-here

# Optional - Web Search in Chatbot
SERPAPI_KEY=your-key-here
```

### Getting API Keys

| Service | URL | Free Tier |
|---------|-----|-----------|
| OpenRouter | https://openrouter.ai/ | $1 free credits |
| OpenAI | https://platform.openai.com/ | Pay as you go |
| OpenWeatherMap | https://openweathermap.org/api | 1000 calls/day |
| SerpApi | https://serpapi.com/ | 100 searches/month |

---

## 📡 API Endpoints

### Main Endpoint

**POST `/analyze`**

Complete analysis pipeline.

**Parameters:**
- `file` (File): Farmland image (JPEG/PNG/WebP, max 10MB)
- `city` (Optional, Text): City name
- `state` (Optional, Text): State name
- `include_report` (Optional, Boolean): Generate reports (default: true)

**Response:**
```json
{
  "analysis_id": "uuid",
  "status": "success",
  "timestamp": "ISO-8601",
  "image_metadata": { ... },
  "location_data": { ... },
  "vision_analysis": {
    "vegetation_type": "forest",
    "density_percentage": 80.0,
    "land_condition": "good",
    ...
  },
  "carbon_analysis": {
    "carbon_estimate": {
      "annual_sequestration_tons": 27.88,
      "potential_revenue_inr": { ... }
    },
    "recommendations": [ ... ],
    "next_steps": [ ... ]
  },
  "reports": {
    "full_report_markdown": "...",
    "executive_summary": "...",
    "text_summary": "..."
  },
  "summary": { ... }
}
```

---

### Chat Endpoint

**POST `/chat`**

Interact with AI assistant.

**Body:**
```json
{
  "message": "How was my revenue calculated?",
  "conversation_history": [ ... ],
  "user_analysis": { ... }
}
```

**Response:**
```json
{
  "status": "success",
  "response": "Your revenue of ₹74,775/year is calculated...",
  "tokens": { ... },
  "model": "mistralai/mixtral-8x7b-instruct",
  "search_performed": false
}
```

---

### Utility Endpoints

- **GET `/states`** - List of Indian states
- **GET `/health`** - API health check
- **POST `/chat/suggestions`** - Get suggested questions
- **GET `/test-chatbot`** - Test chatbot connection

---

## 💡 Usage Examples

### Example 1: Basic Analysis

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@farmland.jpg" \
  -F "city=Surat" \
  -F "state=Gujarat"
```

### Example 2: Chat with Context

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Why is my confidence level medium?",
    "user_analysis": { ... }
  }'
```

### Example 3: Python Client

```python
import requests

# Analyze farmland
with open('farmland.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/analyze',
        files={'file': f},
        data={'city': 'Surat', 'state': 'Gujarat'}
    )

analysis = response.json()
print(f"Revenue: ₹{analysis['summary']['estimated_annual_revenue_inr']['mid_range']}")
```

---

## 💰 Cost Analysis

### Per Analysis Breakdown

| Component | Model | Cost (INR) |
|-----------|-------|------------|
| Image Analysis | Llama 3.2 Vision | ₹8 |
| Report Generation | GPT-4o | ₹4 |
| Location Data | OpenWeatherMap | Free |
| **Total per analysis** | | **₹12** |

### Chatbot Costs

| Model | Cost per message | 100 messages |
|-------|-----------------|--------------|
| Mistral 8x7B | ₹0.02 | ₹2 |

### Monthly Estimates (100 users)

- 100 analyses = ₹1,200
- 500 chat messages = ₹10
- **Total: ₹1,210/month**

---

## ⚠️ Limitations

### Technical Limitations

1. **Area Estimation**: Rough estimates from images (±30% accuracy)
2. **Single Image**: Can't assess multiple angles or seasonal changes
3. **No Soil Data**: Carbon calculations don't include soil carbon
4. **Weather Dependency**: Location features require API availability

### Use Case Limitations

1. **Preliminary Only**: Not a substitute for professional survey
2. **Indian Context**: Optimized for Indian climate zones and programs
3. **Market Volatility**: Revenue estimates based on current prices
4. **Verification Required**: Official carbon credit enrollment needs certified assessment

### Disclaimers

All reports include:
- This is a preliminary estimate
- Professional land survey required
- Revenue depends on market conditions
- 20-30 year commitments typical
- Verification costs ₹4-17 lakhs

---

## 🔮 Future Enhancements

### Short-term (1-3 months)

- [ ] Frontend web application
- [ ] User authentication & saved analyses
- [ ] PDF report export
- [ ] Multiple image upload
- [ ] Soil carbon estimation

### Mid-term (3-6 months)

- [ ] Mobile app (React Native)
- [ ] Historical data tracking
- [ ] Program matching (auto-suggest best programs)
- [ ] Satellite imagery integration
- [ ] Multi-language support (Hindi, Tamil, Telugu)

### Long-term (6-12 months)

- [ ] Direct program applications
- [ ] Marketplace for carbon credits
- [ ] Community features (farmer groups)
- [ ] IoT sensor integration
- [ ] Blockchain verification

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Write tests for new features
- Update README for API changes

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- Anthropic (Claude for development assistance)
- OpenRouter (AI model access)
- OpenAI (GPT-4o)
- Meta (Llama models)
- Indian farmers (inspiration)

---

## 📞 Contact & Support

- **Issues**: GitHub Issues
- **Email**: support@terracredit.ai (placeholder)
- **Documentation**: http://localhost:8000/docs

---

## 🌟 Star History

If this project helps you, please star it on GitHub!

---

**Built with ❤️ for Indian seeking sustainable income opportunities.**
