# image-captioning

This Flask-based Python application leverages a Hugging Face image-text model to analyze images and generate descriptive textual information..

## Prerequisites

Before you begin, ensure you have the following installed:

- Python (version 3.x recommended)
- `virtualenv` (you can install it using `pip install virtualenv`)
- Docker (if you want to build and run the app using Docker)

## Getting started

1. Create a virtual environment:

```pwsh
    python3 -m venv <your_env>
```

2. Activate the virtual environment:

On Windows:

```pwsh
.\<your_env>\Scripts\activate
```

On macOS/Linux:

```bash
source <your_env>/bin/activate
```

3. Install dependencies:

```pwsh
pip install -r requirements.txt
```

4. Create an `.env` file:

```
CACHED_MODEL_PATH=models/Salesforce/blip-image-captioning-large
```

5. Optional: Build the app for docker

```pwsh
    docker build -t <your-docker-image-name> .
```

6. Run the app:

Run the app for development:

```pwsh
   python -m uvicorn app:app --reload
```

Run the app in docker.

```pwsh
docker run -it --rm -p 8000:8000 -e CACHED_MODEL_PATH=<path_to_your_local_models> -v <path_to_your_local_models>:/app/models <your-docker-image-name>
```

example:

```bash
docker run -it --rm -p 8000:8000 --env-file .\.env -v .\models:/app/models  uvicorn-app
```

## Examples

### Conditional captioning

You can set the `image_text_input` parameter to use conditional image captioning:

```http
POST http://127.0.0.1:6000/image-captioning HTTP/1.1
content-type: application/json

{
    "image_url": "https://images.pexels.com/photos/19599971/pexels-photo-19599971/free-photo-of-an-old-man-standing-on-the-shore-near-a-pier.jpeg",
    "image_text_input": "a photograph of",
    "generate_options": {
        "max_new_tokens": 300,
        "temperature": 0.7,
        "do_sample": true
    }
}
```

Example response (depening on set temperature):

```json
{
  "captions": [
    {
      "generated_text": "a photograph of a man standing on a pier looking at a boat"
    }
  ],
  "result": "success",
  "warnings": []
}
```

### Multiple generated text:

You can set the image_text_input parameter to use conditional image captioning:

```http
POST http://127.0.0.1:6000/image-captioning HTTP/1.1
content-type: application/json

{
    "image_url": "https://images.pexels.com/photos/19599971/pexels-photo-19599971/free-photo-of-an-old-man-standing-on-the-shore-near-a-pier.jpeg",
    "generate_options": {
        "max_new_tokens": 300,
        "num_beams": 5,
        "num_return_sequences": 5
    }
}
```

Example response:

```json
{
  "captions": [
    {
      "generated_text": "there is a man that is standing in the water looking at the water"
    },
    {
      "generated_text": "there is a man that is standing by the water looking at the water"
    },
    {
      "generated_text": "there is a man that is standing in the water looking at a boat"
    },
    {
      "generated_text": "there is a man that is standing in the water by the dock"
    },
    {
      "generated_text": "there is a man that is standing by the water looking at something"
    }
  ],
  "result": "success",
  "warnings": []
}
```

### Warnings from the model are exposed:

```http
POST http://127.0.0.1:6000/image-captioning HTTP/1.1
content-type: application/json

{
    "image_url": "https://images.pexels.com/photos/19599971/pexels-photo-19599971/free-photo-of-an-old-man-standing-on-the-shore-near-a-pier.jpeg",
    "image_text_input": "a photograph of",
    "generate_options": {
        "max_new_tokens": 300,
        "temperature": 0.7
    }
}
```

Example response:

```json
{
  "captions": [
    {
      "generated_text": "a photograph of a man standing on a dock looking out at the water"
    }
  ],
  "result": "success",
  "warnings": [
    "`do_sample` is set to `False`. However, `temperature` is set to `0.7` -- this flag is only used in sample-based generation modes. You should set `do_sample=True` or unset `temperature`."
  ]
}
```
