from fastapi.responses import PlainTextResponse
from fastapi import FastAPI
from pydantic import BaseModel
from toqan import ToqanBot
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
bot = ToqanBot()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique o domínio correto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    
# Endpoint para iniciar uma nova conversa
@app.post("/create_conversation")
def new_conversation(req: MessageRequest):
    response = bot.create_conversation(req.message)
    return {
        "status": "ok",
        "response": response
        }

# Endpoint para continuar uma conversa existente
@app.post("/continue_conversation")
def continue_conversation(req: MessageRequest):
    response = bot.continue_conversation(req.message, req.conversation_id)
    return {"status": "ok",
        "response": response
        }

# Endpoint para consultar os logs
@app.get("/logs", response_class=PlainTextResponse)
def get_logs():
    try:
        with open("logs/history.log", "r", encoding="utf-8") as log_file:
            return log_file.read()
    except Exception as e:
        return f"Error reading log file: {e}"
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)