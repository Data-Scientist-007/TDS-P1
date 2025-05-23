from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import base64
import pytesseract
from io import BytesIO
from PIL import Image
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from data_extractor import DataExtractor
from vector_store import VectorStoreManager

app = FastAPI()
vector_mgr = VectorStoreManager()

class QueryRequest(BaseModel):
    question: str
    image: Optional[str] = None

def process_image(base64_image: str) -> str:
    """Extract text from base64 encoded image"""
    try:
        image_data = base64.b64decode(base64_image)
        img = Image.open(BytesIO(image_data))
        return pytesseract.image_to_string(img)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")

@app.post("/api")
async def answer_question(request: QueryRequest):
    # Process image if present
    image_text = process_image(request.image) if request.image else ""
    
    # Combine question and image text
    full_query = f"{request.question} {image_text}".strip()
    
    # Retrieve relevant documents
    retriever = vector_mgr.get_retriever()
    docs = await retriever.aget_relevant_documents(full_query)
    
    # Generate answer
    llm = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")
    prompt = PromptTemplate.from_template("""
        Answer the student's question using the provided context.
        Question: {question}
        Context: {context}
        Format your answer clearly and cite sources using [source] markers.
    """)
    
    chain = prompt | llm
    response = await chain.ainvoke({
        "question": request.question,
        "context": "\n\n".join([d.page_content for d in docs])
    })
    
    # Format response
    return {
        "answer": response.content,
        "links": [{"url": d.metadata["source"], "text": d.page_content} for d in docs[:3]]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
