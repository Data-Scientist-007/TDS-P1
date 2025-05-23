# TDS Virtual TA API

Automated teaching assistant for IIT Madras Data Science program

## Setup

1. Install dependencies:
pip install -r requirements.txt



2. Set environment variables:
export OPENAI_API_KEY="your_openai_key"
export DISCOURSE_API_KEY="your_discourse_key"
export DISCOURSE_API_USERNAME="your_username"



3. Initialize vector store:
from data_extractor import DataExtractor
from vector_store import VectorStoreManager

Initialize components
extractor = DataExtractor(
discourse_domain="https://your.forum.url",
discourse_api_key="your_key",
discourse_username="username"
)

Extract and process data
pdf_text = extractor.extract_pdf_text("course_materials.pdf")
posts = extractor.fetch_discourse_posts()
all_texts = [pdf_text] + [post["content"] for post in posts]

Create vector store
vector_mgr = VectorStoreManager()
vector_mgr.create_vector_store(all_texts)



## Running the API
docker build -t tds-virtual-ta .
docker run -p 8000:8000 tds-virtual-ta



## API Endpoint
POST /api with JSON body:
{
"question": "Your question here",
"image": "base64_encoded_image_optional"
}


undefined
