# image-captioning

This FastAPI application efficiently generates captions from input images using the pre-trained model 'Salesforce/blip-image-captioning-large'. The application processes input, with a maximum text limit of 600 characters, using a dedicated processor. Upon completion, it delivers the synthesized captions as a JSON response.

## Getting started

### Requirements

- Docker

### Creating an .env file

Create a file containing the following environment variables

```
CACHED_MODEL_PATH=ai/models/Salesforce/blip-image-captioning-large
LOG_LEVEL=DEBUG (optional)
ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000  (optional)
```

### Running the app

#### Using Docker

With using the volumn mount, make sure you use the same path as the env variable `CACHED_MODEL_PATH`. This way, the models are not downloaded each time you run the image: `<host_full_path>:app/ai/models`

```bash
docker run -it --rm -p 8000:8000 --env-file .env -v .\ai\models:/app/ai/models lenndewolten/imaginarrative_image_captioning:salesforce-blip-image-captioning-large-v3
```

#### Using uvicorn

Create a python environment:

```bash
python -m venv venv
```

Activate environment:
Windows

```bash
venv\scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app:app --reload --port 8000
```

### Explore!

See [requests.http](./requests.http) for request examples or simply navigate to: `http://localhost:8000` and explore the swagger docs!
