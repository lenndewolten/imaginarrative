from flask import Flask, request, jsonify
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import requests
import warnings
from dotenv import load_dotenv
import os

load_dotenv()
model_path = os.getenv('CACHED_MODEL_PATH', 'Salesforce/blip-image-captioning-large')

def get_model():
    model = BlipForConditionalGeneration.from_pretrained(model_path)
    processor = BlipProcessor.from_pretrained(model_path)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    return model, processor, device

model, processor, device = get_model()

app = Flask(__name__)

allowed_generate_options = {
    "max_new_tokens": {"type": int, "min": 50, "max": 300},
    "num_beams": {"type": int, "min": 1, "max": 10},
    "num_return_sequences": {"type": int, "min": 1, "max": 10},
    "early_stopping ": {"type": bool},
    "temperature": {"type": float, "min": 0.0, "max": 1.0},
    "do_sample": {"type": bool}
}

def validate_generate_options(key, value):
    if key not in allowed_generate_options:
        return f"Invalid option: '{key}'"

    option_info = allowed_generate_options[key]
    option_type = option_info.get("type", None)

    if option_type is not None and not isinstance(value, option_type):
        return f"{key} must be of type {option_type}"

    if "min" in option_info and value < option_info["min"]:
        return f"{key} must be greater than or equal to {option_info['min']}"

    if "max" in option_info and value > option_info["max"]:
        return f"{key} must be less than or equal to {option_info['max']}"

    return None


def get_options(json):
    image_url = json.get('image_url')

    if image_url is None:
        return None, "Image URL not provided"

    image_text_input = json.get('image_text_input')
    generate_options = json.get("generate_options", {})

    kwargs = {}

    for key, value in generate_options.items():
        validation_error = validate_generate_options(key, value)
        if validation_error:
            return None, validation_error
        kwargs[key] = value

    return {"image_url": image_url, "image_text_input": image_text_input, "kwargs": kwargs}, None


def download_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return Image.open(response.raw)
    else:
        raise Exception(f"Error downloading image from {url}. Status code: {response.status_code}")

def generate_captions(image_url, image_text_input, **kwargs):
    try:
        image = download_image(image_url)
        if image.mode != "RGB":
            image = image.convert(mode="RGB")
        
        inputs = processor(image, image_text_input, return_tensors="pt").to(device)
        outputs = model.generate(**inputs, **kwargs)
       
        captions = []
        for sequence in outputs:
            caption = processor.decode(sequence, skip_special_tokens=True)
            captions.append({"generated_text": caption})
        
        return captions, None
    except ValueError as error:
        return None, error
    except Exception as error:
        app.logger.error(error)
        return None, error

@app.route('/image-captioning', methods=['POST'])
def image_captioning_endpoint():

    captured_warnings = []
    try:
        options, error = get_options(request.json)
        if error is not None:
            return jsonify({'error': str(error)}), 400
        
        def capture_warnings(message, category, filename, lineno, file=None, line=None):
            warning_message = f"{message}"
            captured_warnings.append(warning_message)

        warnings.showwarning = capture_warnings
        warnings.simplefilter("always", UserWarning)

        captions, error  = generate_captions(options["image_url"],  options["image_text_input"], **options["kwargs"])
        if error is not None:
            return jsonify({'error': str(error)}), 500
        return jsonify({'result': 'success', 'captions': captions, 'warnings': captured_warnings}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        captured_warnings.clear()
        warnings.resetwarnings()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
