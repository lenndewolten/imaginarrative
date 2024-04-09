# story-generator

The Story Generator API is a creative tool that leverages the power of OpenAI's GPT-3.5-turbo model to craft engaging short stories based on user-provided prompts. Whether you're looking for a quick narrative or seeking inspiration, this API transforms your ideas into captivating tales.

## Getting started

### Requirements

- Docker

### Creating an .env file

Create a file containing the following environment variables

```
OPENAI_API_KEY=<open_api_key>
ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000 (optional)
```

### Running the app

#### Using Docker

```bash
docker run -it --rm -p 8000:8000 --env-file .env lenndewolten/imaginarrative_story_generating:chat3.5-turbo-v2
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
