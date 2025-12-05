import io

import openai
import pdfplumber

from src.config import settings


class OpenAIAnalyzer:

    def __init__(self):
        if settings.openai_api_key is None:
            raise ValueError("OpenAI API key is not configured. Please set OPENAI_API_KEY in .env file.")
        self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def analyze(self, file_content: bytes, file_name: str) -> str:
        try:
            extracted_text = self._extract_text_from_pdf(file_content)
            
            if not extracted_text.strip():
                return "Unable to extract text from the PDF file. The file may be empty or contain only images."
            
            max_chars = 15000
            if len(extracted_text) > max_chars:
                extracted_text = extracted_text[:max_chars] + "\n\n[...текст был сокращен...]"
            
            system_prompt = "You are an expert document analyst. Your task is to provide a concise, one-paragraph summary of the provided text."
            user_prompt = f"Analyze the following text from the document '{file_name}':\n\n{extracted_text}"
            
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            return result if result else "No analysis result returned from OpenAI."
            
        except openai.APIError as e:
            return f"OpenAI API error: {str(e)}. Please check your API key and try again."
        except Exception as e:
            return f"Error analyzing file: {str(e)}"
    
    @staticmethod
    def _extract_text_from_pdf(file_content: bytes) -> str:
        text_parts = []
        
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
