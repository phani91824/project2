"""
ClauseWise Legal Document Analyzer - Hackathon Prototype
FastAPI Backend with IBM Watson NLU and Granite Model Integration
"""

from fastapi import FastAPI, File, UploadFile, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import json
import PyPDF2
import docx
from datetime import datetime
import io
import re
from typing import Dict, List, Optional
import asyncio

# Initialize FastAPI app
app = FastAPI(
    title="ClauseWise Legal Document Analyzer",
    description="AI-powered legal document analysis with clause simplification and entity extraction",
    version="1.0.0"
)

# Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Mock IBM Watson NLU and Granite Model Integration
# In production, replace with actual IBM Watson API calls
class MockWatsonNLU:
    def analyze_entities(self, text: str) -> Dict:
        """Mock entity extraction using Watson NLU"""
        # Simulate entity extraction
        entities = []

        # Extract parties (organizations/persons)
        parties = re.findall(r'\b[A-Z][a-z]+ (?:Corp|Inc|LLC|Ltd|Company|Corporation)\b', text)
        parties.extend(re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text))

        for party in set(parties[:3]):  # Limit to top 3
            entities.append({
                "text": party,
                "type": "ORGANIZATION" if any(suffix in party for suffix in ["Corp", "Inc", "LLC", "Ltd", "Company"]) else "PERSON",
                "confidence": 0.85
            })

        # Extract dates
        dates = re.findall(r'\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{4}-\d{2}-\d{2}\b', text)
        for date in set(dates[:3]):
            entities.append({
                "text": date,
                "type": "DATE",
                "confidence": 0.90
            })

        # Extract monetary amounts
        amounts = re.findall(r'\$[\d,]+(?:\.\d{2})?', text)
        for amount in set(amounts[:3]):
            entities.append({
                "text": amount,
                "type": "MONEY",
                "confidence": 0.88
            })

        return {"entities": entities}

    def classify_document(self, text: str) -> Dict:
        """Mock document classification"""
        text_lower = text.lower()

        if "non-disclosure" in text_lower or "confidential" in text_lower:
            return {"classification": "NDA", "confidence": 0.92}
        elif "lease" in text_lower or "rental" in text_lower:
            return {"classification": "Lease Agreement", "confidence": 0.89}
        elif "employment" in text_lower or "employee" in text_lower:
            return {"classification": "Employment Contract", "confidence": 0.87}
        elif "service" in text_lower or "services" in text_lower:
            return {"classification": "Service Agreement", "confidence": 0.85}
        else:
            return {"classification": "General Contract", "confidence": 0.70}

class MockGraniteModel:
    def simplify_clause(self, clause: str) -> str:
        """Mock clause simplification using Granite model"""
        # Simple rule-based simplification for demo
        simplified = clause

        # Replace complex legal terms
        replacements = {
            "whereas": "while",
            "heretofore": "before now",
            "hereinafter": "from now on", 
            "party of the first part": "first party",
            "party of the second part": "second party",
            "shall": "will",
            "pursuant to": "according to",
            "notwithstanding": "despite",
            "aforementioned": "mentioned above"
        }

        for legal_term, simple_term in replacements.items():
            simplified = re.sub(legal_term, simple_term, simplified, flags=re.IGNORECASE)

        # Add plain language explanation
        if len(simplified) > 200:
            return f"In simple terms: {simplified}"
        return simplified

# Initialize AI models
watson_nlu = MockWatsonNLU()
granite_model = MockGraniteModel()

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """Extract text from uploaded file"""
    try:
        if filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

        elif filename.endswith('.docx'):
            doc = docx.Document(io.BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text

        elif filename.endswith('.txt'):
            return file_content.decode('utf-8')

        else:
            raise ValueError("Unsupported file format")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting text: {str(e)}")

def extract_clauses(text: str) -> List[str]:
    """Extract individual clauses from legal document"""
    # Split by common clause indicators
    clauses = []

    # Split by numbered sections
    sections = re.split(r'\n\s*\d+\.\s*', text)
    if len(sections) > 1:
        clauses.extend([section.strip() for section in sections[1:] if len(section.strip()) > 50])

    # Split by paragraph breaks if no numbered sections
    if not clauses:
        paragraphs = text.split('\n\n')
        clauses = [p.strip() for p in paragraphs if len(p.strip()) > 100]

    # Limit to top 6 clauses for demo
    return clauses[:6]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with file upload interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """Main API endpoint for document analysis"""
    try:
        # Validate file type
        if not file.filename.endswith(('.pdf', '.docx', '.txt')):
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Read file content
        file_content = await file.read()

        # Extract text
        text = extract_text_from_file(file_content, file.filename)

        if len(text.strip()) < 100:
            raise HTTPException(status_code=400, detail="Document too short for analysis")

        # Extract clauses
        clauses = extract_clauses(text)

        # Analyze with AI models
        document_classification = watson_nlu.classify_document(text)
        entities = watson_nlu.analyze_entities(text)

        # Simplify clauses
        simplified_clauses = []
        for i, clause in enumerate(clauses, 1):
            simplified = granite_model.simplify_clause(clause)
            simplified_clauses.append({
                "clause_number": i,
                "original": clause[:200] + "..." if len(clause) > 200 else clause,
                "simplified": simplified,
                "risk_level": "Medium" if i % 2 == 0 else "Low",  # Mock risk assessment
                "category": f"Clause Type {i}"
            })

        # Calculate overall risk
        risk_levels = {"Low": 1, "Medium": 2, "High": 3}
        avg_risk = sum(risk_levels.get(clause["risk_level"], 1) for clause in simplified_clauses) / len(simplified_clauses)
        overall_risk = "Low" if avg_risk < 1.5 else "Medium" if avg_risk < 2.5 else "High"

        # Prepare response
        analysis_result = {
            "document_info": {
                "filename": file.filename,
                "document_type": document_classification["classification"],
                "confidence": document_classification["confidence"],
                "total_clauses": len(simplified_clauses),
                "overall_risk": overall_risk,
                "analysis_time": "2.3s"
            },
            "entities": entities["entities"],
            "clauses": simplified_clauses,
            "recommendations": [
                "Review high-risk clauses with legal counsel",
                "Consider adding specific performance metrics", 
                "Ensure all terms are clearly defined",
                "Verify compliance with local regulations"
            ]
        }

        return JSONResponse(content=analysis_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/simplify")
async def simplify_clause_endpoint(clause: str):
    """API endpoint for individual clause simplification"""
    if not clause:
        raise HTTPException(status_code=400, detail="Clause text required")

    simplified = granite_model.simplify_clause(clause)
    return {"original": clause, "simplified": simplified}

@app.get("/api/extract-entities")
async def extract_entities_endpoint(text: str):
    """API endpoint for entity extraction"""
    if not text:
        raise HTTPException(status_code=400, detail="Text required")

    entities = watson_nlu.analyze_entities(text)
    return entities

@app.get("/api/classify")
async def classify_document_endpoint(text: str):
    """API endpoint for document classification"""
    if not text:
        raise HTTPException(status_code=400, detail="Text required")

    classification = watson_nlu.classify_document(text)
    return classification
