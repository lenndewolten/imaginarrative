# Imaginarrative

Turn an image into a story! Imaginarrative is an innovative application that transforms ordinary images into captivating stories. Using the power of AI, it employs three distinct AI models to craft narratives that bring your images to life.

https://github.com/lenndewolten/imaginarrative/assets/48725857/c80485f5-709b-4163-96ec-a7e0752b8468



## Key features

- Image Captioning: A FastAPI application that generates captions from input images using the pre-trained model 'Salesforce/blip-image-captioning-large' hosted on _HuggingFace_.

- Story Generation: A _LangChain_ based tool that leverages the power of OpenAI's `GPT-3.5-turbo` model to craft engaging short stories based on user-provided prompts.

- Story Teller: A FastAPI application that generates audio from input text using the pre-trained model 'microsoft/speecht5*tts', speaker embeddings, and a vocoder hosted on \_HuggingFace*.

- Single Page Application: A `VueJS + vite` webapp powered by the component framework [Vuetify](https://vuetifyjs.com/en/). It brings all the three AI applications together.

## Getting started

**Please Note**: The applications utilizes advanced AI models for image recognition, story generation, and narration. These AI models are computationally and GPU intensive, requiring significant processing power to function optimally. Therfore machines with higher computational capabilities and GPU specifications will generally experience smoother and faster performance compared to those with lower specifications.

### Requirements

- Docker + Compose
- OPENAI api key with ChatGPT 3.5-tubo read access

### Creating an .env file

Create a file containing the following environment variables in the root folder:

```bash
OPENAI_API_KEY=sk-.....
```

Also create an .env file in the **front-app** folder containing the following environment variables:

```bash
VITE_IMAGE_CAPTIONING_BASE_URL=http://localhost:7000
VITE_STORY_GENERATOR_BASE_URL=http://localhost:8000
VITE_STORY_TELLER_BASE_URL=http://localhost:9000
```

Make sure the ports are matching the ports exposed in the compose file.

### RUN DOCKER COMPOSE

```bash
docker compose up --build
```

This Docker Compose configuration orchestrates a multi-container environment, seamlessly integrating the image captioning, story generation, storytelling, and web application components. The backend services dynamically handle the retrieval of AI models, automatically downloading them if not found in the cache. Meanwhile, the web application is built and containerized, linking its ports with those of the backend services.

Navigate to [http://localhost:8080/](http://localhost:8080/) and bring your images to life!
