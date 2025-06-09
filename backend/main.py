from fastapi import FastAPI
from backend.routes import recommendations
import uvicorn

app = FastAPI(
    title="AI Infra Cost Optimizer",
    description="API for cloud cost optimization using AI agent recommendations",
    version="1.0.0"
)

# Include recommendations routes
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Infra Cost Optimizer API"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
