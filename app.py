import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
import joblib
import pandas as pd
import io

app = FastAPI()

# Path to the HTML template file
template_path = "index.html"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/", response_class=HTMLResponse)
async def home():
    # Read the HTML template from the specified path
    try:
        with open(template_path, "r") as template_file:
            html_content = template_file.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        logger.error(f"HTML template file not found at: {template_path}")
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        
        # Convert the bytes into a file-like object using io.BytesIO
        file_like_object = io.BytesIO(contents)
        
        # Read the CSV from the file-like object
        df = pd.read_csv(file_like_object)
        
        df = data_validation(df)
        with open("model.pkl", 'rb') as model_file:
            classifier = joblib.load(model_file)
        predictions = classifier.predict(df)

        df['Predicted Flower Type'] = predictions
        return JSONResponse(content=df.to_dict(orient="split"))
    except Exception as e:
        logger.exception("Error processing prediction request")
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)

def data_validation(df):
    # some logic
    return df

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)