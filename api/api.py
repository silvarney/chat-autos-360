from fastapi.responses import PlainTextResponse
from fastapi import FastAPI
from pydantic import BaseModel
from .toqan import ToqanBot        # agora é import relativo
from fastapi.middleware.cors import CORSMiddleware
from .logs.log_config import setup_logging  # import relativo
from typing import Optional

# Configura logging
setup_logging()

app = FastAPI()
bot = ToqanBot()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

@app.post("/create_conversation")
def new_conversation(req: MessageRequest):
    response = bot.create_conversation(req.message)
    return {"status": "ok", "response": response}

@app.post("/continue_conversation")
def continue_conversation(req: MessageRequest):
    response = bot.continue_conversation(req.message, req.conversation_id)
    return {"status": "ok", "response": response}

@app.get("/logs", response_class=PlainTextResponse)
def get_logs():
    log_file = '/tmp/logs/history.log'
    try:
        return open(log_file, "r", encoding="utf-8").read()
    except Exception as e:
        return f"Error reading log file: {e}"

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Vercel espera o app aqui
handler = app
