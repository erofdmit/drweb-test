import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db import init_db
from app.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    debug=False,
    title='API',
    openapi_url="/api/v2/openapi.json",
    docs_url='/docs',
    swagger_ui_parameters={'syntaxHighlight': False}
)

@app.on_event("startup")
async def startup_event():
    await init_db()
    
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(api_router, prefix='')