# Callus SEO Keyword Research AI Agent - Project Plan

## 🎯 Project Overview
**Objective**: Build an AI-powered SEO keyword research agent that takes a seed keyword and returns 50 candidate keywords sorted by lowest competition and highest monthly search volume.

**Deadline**: October 5, 2025, 7PM IST
**Status**: MVP Functional ✅

## 🏗️ Architecture & Implementation

### Frontend
- **Technology**: Streamlit (Python web framework)
- **Choice Rationale**: Rapid prototyping, built-in UI components, easy deployment
- **Features**: 
  - Seed keyword input
  - Real-time analysis progress
  - Interactive results table
  - CSV export functionality
  - API key configuration

### Core Engine
- **Keyword Expansion**: OpenAI GPT-3.5-turbo + fallback rule-based generator
- **Metrics Analysis**: 
  - Search Volume: Characteristic-based estimation
  - Competition: SERP analysis heuristics
- **Scoring Algorithm**: 
  `composite_score = α × normalized_volume - β × competition_score`
  - Default: α=0.6, β=0.4 (configurable)

### Data Sources
- **Primary**: SerpApi (SERP data), Google Ads Keyword Planner (volumes)
- **Current Fallback**: Simulated metrics with realistic heuristics
- **Production Ready**: API integration points implemented

## 📊 Key Features Delivered

### ✅ MVP Complete
- [x] Seed keyword input and processing
- [x] LLM-powered keyword expansion (100+ variations)
- [x] Competition and volume estimation
- [x] Composite scoring and ranking
- [x] Top 50 keyword recommendations
- [x] Interactive web interface
- [x] CSV export functionality
- [x] Real-time progress tracking

### 🔄 n8n Integration Ready
- Workflow skeleton prepared for:
  - HTTP request handling
  - LLM API integration
  - SerpApi data processing
  - Scoring and filtering logic

## 🚀 Technical Implementation

### Code Structure

callus-seo-agent/
├── web/streamlit_app.py # Main UI application
├── backend/keyword_engine.py # Core analysis engine
├── n8n-workflows/ # Orchestration workflows
├── tests/test_pipeline.py # Unit tests
└── docs/1page_plan.pdf # This document


### Key Algorithms
1. **Keyword Expansion**: LLM prompt engineering for diverse variations
2. **Deduplication**: Normalization and exact matching
3. **Competition Scoring**: Domain authority analysis + SERP features
4. **Opportunity Ranking**: Weighted composite scoring

## 📈 Validation & Metrics

### Scoring Methodology
- **Volume Normalization**: 0-1 scale based on estimated search volume
- **Competition Scale**: 0-1 (0 = low competition, 1 = high competition)
- **Opportunity Score**: Balanced tradeoff between volume and competition

### Quality Assurance
- Fallback systems for API failures
- Input validation and error handling
- Progressive enhancement approach

## 🔧 API Integrations

### Current Implementation
- **OpenAI GPT-3.5-turbo**: Keyword expansion and intent classification
- **SerpApi**: SERP data for competition analysis
- **Modular Design**: Easy integration with additional APIs

### Ready for Production
- Google Ads Keyword Planner API
- SEMrush/Ahrefs APIs
- Custom SERP scraping solutions

## 💡 Innovation & Differentiation

1. **Intelligent Fallback System**: Continues operation even with API limitations
2. **Configurable Scoring**: Adjustable α/β parameters for different SEO strategies
3. **Real-time Processing**: Live progress updates during analysis
4. **Export-Ready Outputs**: CSV format for immediate use in SEO tools

## 📋 Deliverables Status

- [x] **1-page PDF Plan**: This document
- [x] **Working Demo (MVP)**: Streamlit app functional
- [ ] **n8n Workflow**: JSON structure prepared (integration ready)
- [x] **Public GitHub Repo**: Structure complete, ready for publication
- [ ] **Video Demo**: Script prepared, ready for recording
- [x] **Code Quality**: Modular, documented, tested

## 🎯 Next Steps for Submission

1. **Finalize n8n workflow integration**
2. **Record video demonstration**
3. **Prepare GitHub repository for public access**
4. **Document API setup instructions**
5. **Create deployment guide**

## ⚠️ Notes & Limitations

- **Current**: Uses simulated data when APIs unavailable
- **Production**: Requires API keys for full functionality
- **Scale**: Designed for individual keyword research projects
- **Extension**: Architecture supports team collaboration features

---

*Built with Python, Streamlit, OpenAI, and SerpApi • Ready for n8n orchestration*