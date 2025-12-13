from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import utils


class AIProcessor:
    """Handles AI processing of files"""

    def __init__(self, inference_host, model='qwen3-vl:2b'):
        self.client = ChatOllama(model=model, base_url=inference_host)

    def process_file(self, file_path):
        """Process a file based on its type"""
        if utils.is_image(file_path):
            return self._process_image(file_path)
        elif utils.is_pdf(file_path):
            return self._process_pdf(file_path)
        else:
            return f"Unsupported file type: {utils.get_mime_type(file_path)}"

    def _process_image(self, file_path):
        """Process image file with AI"""
        try:
            image_data = utils.encode_image(file_path)
            mime_type = utils.get_mime_type(file_path)

            messages = [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": """
                                    What's in this image?
                                    Describe it briefly and simply in one sentence.
                                    """
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:{mime_type};base64,{image_data}"
                        }
                    ]
                )
            ]

            ai_msg = self.client.invoke(messages)
            return ai_msg.content
        except Exception as e:
            return f"Error processing image: {str(e)}"

    def _process_pdf(self, file_path):
        """Process PDF file with AI"""
        try:
            # Extract text from PDF
            pdf_text = utils.extract_text_from_pdf(file_path)

            if not pdf_text.strip():
                return "PDF appears to be empty or contains no extractable text."

            # Limit text length to avoid context window issues
            if len(pdf_text) > 4000:
                pdf_text = pdf_text[:4000] + "...[truncated]"

            messages = [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": f"""
                                    Analyze this PDF content and provide a brief summary in one sentence:

                                    {pdf_text}
                                    """
                        }
                    ]
                )
            ]

            ai_msg = self.client.invoke(messages)
            return ai_msg.content
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
