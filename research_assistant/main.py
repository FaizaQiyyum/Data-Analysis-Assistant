from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
import io
import os
from app.analysis.analysis_engine import analyze_dataset, generate_analytical_summary
from app.utils.viz_utils import generate_visualizations

app = FastAPI(title="Research Data Analysis Assistant")

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    return FileResponse("app/static/index.html")

@app.post("/api/analyze")
async def upload_and_analyze(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    
    try:
        # Read file content
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="The uploaded CSV is empty.")
            
        # Perform analysis
        analysis_results = analyze_dataset(df)
        
        # Generate summary
        narrative_summary = generate_analytical_summary(analysis_results)
        
        # Generate visualizations
        visuals = generate_visualizations(df)
        
        return {
            "filename": file.filename,
            "analysis": analysis_results,
            "summary": narrative_summary,
            "visuals": visuals
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
