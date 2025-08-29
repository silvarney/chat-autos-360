# Bot Toqan - Exemplo simples
import os

import logging
import time
import requests
from dotenv import load_dotenv
from logs.log_config import setup_logging

# Configuração de logging
setup_logging()

# Classe para interagir com o Toqan
class ToqanBot:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("TOQAN_API_KEY")
        self.api_url = os.getenv("TOQAN_URL")
        self.conversation_id = None
        self.request_id = None
        self.headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "X-Api-Key": self.api_key
        }
        
    def create_conversation(self, user_message: str):
        """
        Inicia uma nova conversa com o Toqan e retorna a resposta do bot.
        Também registra a interação para auditoria.
        """
        logging.info(f"[START CREATE CONVERSATION]: {time.strftime('%Y-%m-%d %H:%M:%S')} ")
        url = f"{self.api_url}/create_conversation"
        payload = {"user_message": user_message}
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            self.conversation_id = data.get("conversation_id")
            self.request_id = data.get("request_id")
            logging.info(f"[SUCCESS IN CREATION]: {time.strftime('%Y-%m-%d %H:%M:%S')} ")
        except Exception as e:
            logging.error(f"[ERROR CREATING CONVERSATION]: {e}")
            return {"error": str(e)}
        return self.get_answer()

    def get_answer(self, max_retries=10, wait_seconds=2):
        """
        Consulta o Toqan pela resposta até que o status seja 'finished' ou o número máximo de tentativas seja atingido.
        Registra a resposta e o tempo de resposta para auditoria.
        """
        logging.info(f"[START IN CHAT]: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        start_time = time.time()
        url = f"{self.api_url}/get_answer?conversation_id={self.conversation_id}&request_id={self.request_id}"
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                data["conversation_id"] = self.conversation_id
            except Exception as e:
                logging.error(f"[ERROR GETTING ANSWER]: {e}")
                return {"error": str(e)}
            if data.get("status") == "finished":
                elapsed = time.time() - start_time
                logging.info(f"[SUCCESS IN CHAT]: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                return data
            time.sleep(wait_seconds)
        logging.warning(f"[TIMEOUT IN CHAT] Max retries reached.")
        return data

    def continue_conversation(self, user_message: str, conversation_id: str, max_retries=10, wait_seconds=2):
        """
        Continua uma conversa existente com o Toqan e retorna a resposta do bot.
        Também registra a interação para auditoria.
        """
        logging.info(f"[STARTING IN CONTINUING THE CONVERSATION]: {time.strftime('%Y-%m-%d %H:%M:%S')} ")
        url = f"{self.api_url}/continue_conversation"
        payload = {
            "conversation_id": conversation_id,
            "user_message": user_message
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            self.request_id = data.get("request_id")
            logging.info(f"[SUCCESS IN CONTINUING THE CONVERSATION]: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            logging.error(f"[ERROR IN CONTINUING THE CONVERSATION]: {e}")
            return {"error": str(e)}
        return self.get_answer(max_retries=max_retries, wait_seconds=wait_seconds)
