from fastapi import FastAPI
from pydantic import BaseModel,Field
from app.qa import answer_question

app = FastAPI()

# class QuestionRequest(BaseModel):
#     question: str
class QuestionRequest(BaseModel):
    question: str = Field(..., example="When is Layla going to London?", description="The natural language question to answer.")


@app.post("/ask")
async def ask(request: QuestionRequest):
    answer = answer_question(request.question)
    return {"answer": answer}

@app.get("/")
def health_check():
    return {"status": "healthy"}