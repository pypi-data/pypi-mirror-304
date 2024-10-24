The purpose of this is to create a multitude of implementations to parse PDFs into text.
Specifically, these implementations will be using VLMs (hence the name VLM-OCR).

Currently only supports OpenAI and Anthropic models, more to come.

I have uploaded this to PyPi for quick usage: https://pypi.org/project/vlm-ocr/

Usage:
1. pip install vlm-ocr (venv or conda env recommended)
2. create a .env file with the key for your chosen API (Must be in default format, such as OPENAI_API_KEY=sk-... or ANTHROPIC_API_KEY=sk-... )
3. pick the function corresponding to the LLM provider you're using (ex. openai_read or anthropic_read)