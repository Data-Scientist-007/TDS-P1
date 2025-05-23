import fitz  # PyMuPDF
from pydiscourse import DiscourseClient
from typing import List, Dict

class DataExtractor:
    def __init__(self, discourse_domain: str, discourse_api_key: str, discourse_username: str):
        self.discourse_client = DiscourseClient(
            discourse_domain,
            api_username=discourse_username,
            api_key=discourse_api_key
        )

    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from course PDF materials"""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def fetch_discourse_posts(self) -> List[Dict]:
        """Retrieve Discourse posts within date range"""
        posts = []
        for topic in self.discourse_client.topics.list():
            for post in topic.posts:
                if post.created_at >= "2025-01-01" and post.created_at <= "2025-04-14":
                    posts.append({
                        "content": post.raw,
                        "source_url": topic.url,
                        "date": post.created_at
                    })
        return posts
