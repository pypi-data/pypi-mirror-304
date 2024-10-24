from dotenv import load_dotenv
from pdf2image import convert_from_path
import base64
import requests
import os
import anthropic

load_dotenv()



## encode image
def encode_image(image_path: str) -> str:
    '''
    Encode an image file into a base64 string.
    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64 encoded image.
    '''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def openai_read(pdf_path: str, image_quality: int = 60, limit: int = 10, model: str = 'gpt-4o-mini') -> list[str]:
    '''
    Read a pdf using OpenAI's models and turn it into text.
    Default model is gpt-4o-mini.

    Args:
        pdf_path (str): The path to the pdf file.
        image_quality (int): The quality of the image to convert from the pdf. (greatly affects quality/cost, default 60)
        limit (int): The number of pages to process. (default 10 pages)
        model (str): The model to use. (default: gpt-4o-mini)

    Returns:
        str: The text from the pdf.
    '''
    ## get openai api key
    api_key = os.getenv("OPENAI_API_KEY")

    responses = []

    ## turn pdf into images
    images = convert_from_path(pdf_path, dpi=image_quality)
    for i, image in enumerate(images):
        print(f"Processing page {i + 1}")

        ## limit the number of pages processed
        if limit:
            if i+1 > limit:
                break
        
        image.save(f'page_{i + 1}.png', 'PNG')
        image_path = f"page_{i + 1}.png"

        ## encode image
        base64_image = encode_image(image_path)

        ## call openai
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": "Turn this image into text. Return the text in JSON format."
                        },
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                        }
                    ]
                }
            ]
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        text = response.json()["choices"][0]["message"]["content"]
        clean_text = text.replace('```', '').replace('json', '').strip()

        responses.append(clean_text)

        ## get rid of created images
        os.remove(image_path)

    ## combine responses and clean up the text
    return responses

def anthropic_read(pdf_path: str, image_quality: int = 60, limit: int = 10, model: str = 'claude-3-haiku-20240307') -> list[str]:
    '''
    Read a pdf using Anthropic's models and turn it into text.
    Default model is claude-3-haiku-20240307.

    Args:
        pdf_path (str): The path to the pdf file.
        image_quality (int): The quality of the image to convert from the pdf. (greatly affects quality/cost, default 60)
        limit (int): The number of pages to process. (default 10 pages)
        model (str): The model to use. (default: claude-3-haiku-20240307)
    '''
    responses = []

    images = convert_from_path(pdf_path, dpi=image_quality)
    for i, image in enumerate(images):
        print(f"Processing page {i + 1}")

        ## limit the number of pages processed
        if limit:
            if i+1 > limit:
                break
        
        image.save(f'page_{i + 1}.png', 'PNG')
        image_path = f"page_{i + 1}.png"

        ## encode image
        base64_image = encode_image(image_path)
    
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Turn this image into text. Return the text in JSON format."
                        }
                    ],
                }
            ],
        )

        text = message.content[0].text
        clean_text = text.replace('```', '').replace('json', '').strip()

        responses.append(clean_text)

        ## get rid of created images
        os.remove(image_path)
    
    return responses