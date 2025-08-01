# ClauseWise Legal Document Analyzer - Hackathon Prototype

🏆 **AI-Powered Legal Document Analysis System**

## Overview
ClauseWise is an advanced legal document analyzer that uses IBM Watson NLU and Granite models to simplify complex legal clauses, extract entities, and classify documents automatically.

## Key Features
✅ **Clause Simplification** - Converts legal jargon to plain language using Granite-13b-Instruct  
✅ **Entity Extraction** - Identifies parties, dates, amounts using Watson NLU  
✅ **Document Classification** - Auto-detects NDAs, employment contracts, leases  
✅ **Risk Assessment** - Multi-level risk analysis for each clause  
✅ **Interactive UI** - Responsive web interface with drag-and-drop upload  

## Technical Stack
- **Backend**: FastAPI (Python)
- **AI Models**: IBM Watson NLU, IBM Granite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **File Processing**: PDF, DOCX, TXT support

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
cd clausewise_hackathon
python main.py
```

### 3. Access the Application
Open your browser and navigate to: `http://localhost:8000`

## API Endpoints

### Main Analysis Endpoint
- **POST** `/api/analyze` - Upload and analyze legal documents
  - Input: Form data with file upload
  - Output: Complete analysis with clauses, entities, and recommendations

### Individual Feature Endpoints
- **GET** `/api/simplify?clause=<text>` - Simplify individual clauses
- **GET** `/api/extract-entities?text=<text>` - Extract entities from text
- **GET** `/api/classify?text=<text>` - Classify document type

## Project Structure
```
clausewise_hackathon/
├── main.py                 # FastAPI application
├── templates/
│   └── index.html         # Frontend interface
├── static/                # Static assets (if needed)
├── uploads/               # Uploaded files storage
├── sample_documents/      # Test documents
│   ├── sample_nda.txt
│   └── sample_employment.txt
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Usage Instructions

1. **Upload Document**: Drag and drop or click to upload PDF/DOCX/TXT files
2. **Analyze**: Click "Analyze Document" to process with AI
3. **Review Results**: 
   - Document classification and risk assessment
   - Extracted entities (parties, dates, amounts)
   - Clause-by-clause analysis with simplifications
   - Actionable recommendations

## IBM Cloud Integration

**For Production Setup:**

1. **Create IBM Cloud Account**
2. **Provision Services**:
   - Watson Natural Language Understanding
   - Granite Model Access
3. **Configure API Keys**:
   ```python
   # Replace mock classes in main.py with actual IBM SDK calls
   from ibm_watson import NaturalLanguageUnderstandingV1
   from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
   ```

## Demo Features

- **Mock AI Integration**: Uses rule-based processing for demonstration
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Analysis**: Fast processing with loading indicators
- **Professional UI**: Modern, clean interface suitable for legal professionals

## Hackathon Deliverables

✅ **FastAPI Backend** with all required endpoints  
✅ **Responsive Frontend** with file upload and results display  
✅ **AI Model Integration** (mock implementation ready for IBM APIs)  
✅ **Document Processing** for PDF, DOCX, TXT formats  
✅ **Sample Documents** for testing and demonstration  
✅ **Complete Documentation** with setup and usage instructions  

## Deployment Options

### Local Development
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Deployment
- **Railway**: `railway deploy`
- **Render**: Connect GitHub repository
- **Heroku**: `git push heroku main`
- **Docker**: Containerized deployment ready

## Future Enhancements

- Real IBM Watson NLU and Granite model integration
- User authentication and document history
- Advanced risk scoring algorithms
- Export functionality (PDF reports)
- Multi-language support
- Batch document processing

## Contact
For questions about this hackathon prototype, please refer to the documentation or create an issue.

---
**Built for Legal Tech Hackathon 2025** 🚀
