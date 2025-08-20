# HR Resource Query Chatbot

## Overview

The HR Resource Query Chatbot is an intelligent employee search system that allows HR professionals to find suitable candidates using natural language queries. The system uses semantic similarity matching powered by SentenceTransformers to understand queries like "Find Python developers with 3+ years experience" and returns relevant employee profiles from the database.

## Features

- **Natural Language Processing**: Query employees using conversational language
- **Semantic Search**: Advanced similarity matching using SentenceTransformers
- **Fallback Text Matching**: Simple keyword matching when AI model unavailable
- **Interactive Web Interface**: Clean, responsive chat-like UI
- **RESTful API**: Well-documented endpoints for integration
- **Real-time Results**: Instant employee profile display with skills, experience, and availability
- **Example Queries**: Pre-built examples for quick testing
- **CORS Enabled**: Cross-origin requests supported

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Data Layer    │
│   (HTML/JS)     │◄──►│   Backend       │◄──►│   JSON File     │
│                 │    │                 │    │                 │
│ - Chat UI       │    │ - /chat         │    │ - Employee      │
│ - Employee Cards│    │ - /search       │    │   Profiles      │
│ - Examples      │    │ - CORS          │    │ - Skills        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │ SentenceTransf. │
                       │ (all-MiniLM-L6) │
                       │ - Embeddings    │
                       │ - Similarity    │
                       └─────────────────┘
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- Internet connection (for initial model download)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "CHATBOT FOR HR's"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   uvicorn app:app --reload
   ```

4. **Access the application**
   - Web Interface: `http://127.0.0.1:8000`
   - API Documentation: `http://127.0.0.1:8000/docs`

### Dependencies
```
fastapi
uvicorn
sentence-transformers
pydantic
```

## API Documentation

### Endpoints

#### `POST /chat`
Natural language employee search
```json
Request:
{
  "text": "Find Python developers with 3+ years experience"
}

Response:
{
  "query": "Find Python developers with 3+ years experience",
  "results": [
    {
      "name": "John Doe",
      "skills": ["Python", "AWS", "Docker"],
      "experience_years": 5,
      "past_projects": ["E-commerce Platform", "Healthcare Dashboard"],
      "availability": "available"
    }
  ],
  "count": 1
}
```

#### `GET /employees/search`
Filtered employee search
```
/employees/search?skill=Python&min_experience=3&project=Healthcare

Response:
{
  "filters": {
    "skill": "Python",
    "min_experience": 3,
    "project": "Healthcare"
  },
  "results": [...],
  "count": 2
}
```

## AI Development Process

### AI Tools Used
- **Amazon Q Developer**: Primary AI coding assistant (95% of development)
- **Role**: Code generation, debugging, architecture decisions, documentation

### AI Assistance Breakdown
- **Code Generation**: 
  - FastAPI endpoint structure
  - Frontend HTML/CSS/JavaScript
  - Error handling patterns
- **Debugging**: 
  - CORS issues resolution
  - Static file serving problems
  - JavaScript error fixes
- **Architecture Decisions**: 
  - Technology stack selection
  - API design patterns
  - File structure organization

### Manual Problem Solving
- **Data Structure Mismatch**: Manually identified and fixed `projects` vs `past_projects` field inconsistency
- **Port Configuration**: Manual debugging of localhost port conflicts
- **Browser Cache Issues**: Manual identification of cached resource problems

### Development Efficiency
- **Time Saved**: Estimated 60-70% faster development with AI assistance
- **Code Quality**: AI helped maintain consistent patterns and best practices
- **Learning**: AI explanations improved understanding of FastAPI and modern web development

## Technical Decisions

### Model Selection: SentenceTransformers vs OpenAI
**Chosen**: SentenceTransformers (all-MiniLM-L6-v2)
- **Pros**: Free, runs locally, good performance for similarity tasks, no API costs
- **Cons**: Requires initial download, limited to similarity matching
- **Alternative**: OpenAI Embeddings API would provide better accuracy but with ongoing costs

### Local vs Cloud Deployment
**Chosen**: Local development with embedded model
- **Pros**: No external dependencies, faster response times, privacy-friendly
- **Cons**: Initial setup complexity, model download required
- **Trade-off**: Prioritized simplicity and cost over advanced NLP capabilities

### Frontend Architecture
**Chosen**: Embedded HTML/CSS/JS in single file
- **Pros**: Simple deployment, no build process, self-contained
- **Cons**: Less maintainable for larger applications
- **Alternative**: React/Vue.js would be better for complex UIs but adds complexity

### Data Storage
**Chosen**: JSON file
- **Pros**: Simple, human-readable, version controllable
- **Cons**: Not scalable, no query optimization
- **Future**: Database (PostgreSQL/MongoDB) for production use

## Future Improvements

### Short-term (1-2 weeks)
- [ ] Add employee filtering by availability status
- [ ] Implement fuzzy matching for skill names
- [ ] Add employee profile images
- [ ] Export search results to CSV/PDF

### Medium-term (1-2 months)
- [ ] Database integration (PostgreSQL)
- [ ] User authentication and role-based access
- [ ] Advanced search filters (location, salary range)
- [ ] Search history and saved queries
- [ ] Email notifications for new matches

### Long-term (3-6 months)
- [ ] Integration with HR management systems
- [ ] Machine learning for query intent recognition
- [ ] Multi-language support
- [ ] Advanced analytics and reporting
- [ ] Mobile application
- [ ] Real-time chat with HR representatives

### Technical Enhancements
- [ ] Implement caching for faster responses
- [ ] Add comprehensive test suite
- [ ] Set up CI/CD pipeline
- [ ] Add monitoring and logging
- [ ] Implement rate limiting
- [ ] Add API versioning

## Project Structure
```
CHATBOT FOR HR's/
├── app.py                 # FastAPI backend
├── employees_dataset.json # Employee data
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── Frontend/
    ├── index.html        # Web interface
    ├── style.css         # Styling (embedded)
    └── script.js         # JavaScript (embedded)
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License
This project is licensed under the MIT License.