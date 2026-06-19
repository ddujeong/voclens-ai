from fastapi import FastAPI

app = FastAPI(title="VOCLens AI API")

@app.get("/")
def health_check():
    return {"message": "VOCLens AI backend is running"}