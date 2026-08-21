from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

MODEL_NAME = "mistral-small-latest"
MAX_STEPS = 8

model = ChatMistralAI(
    model=MODEL_NAME,
    temperature=0,
)