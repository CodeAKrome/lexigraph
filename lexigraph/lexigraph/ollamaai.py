import ollama
from json import loads
import sys
import base64
from PIL import Image
from io import BytesIO
import requests

DEFAULT_MODEL = "llama3.1:70b"


# add print method to show llm data like model etc
class OllamaAI:
    def __init__(
        self, system_prompt=None, model=DEFAULT_MODEL, max_tokens=3000, temperature=0.1
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.set_system(system_prompt)

    def set_system(self, prompt):
        self.system = (
            prompt
            or "You are a helpful assistant. You reply with short, accurate answers."
        )

    def load_image(self, PathUrlBase64):
        """
        Returns an image object from a path, URL or base64 encoded image data.
        """
        if PathUrlBase64.startswith(("http://", "https://")):
            response = requests.get(PathUrlBase64)
            img = Image.open(BytesIO(response.content))
        elif PathUrlBase64.startswith("data:image"):
            img_data = PathUrlBase64.split(",")[1]
            img = Image.open(BytesIO(base64.b64decode(img_data)))
        else:
            img = Image.open(PathUrlBase64)
        return img

    def says(self, prompt, image_path_or_url=None):
        message = {"role": "user", "content": prompt}

        if image_path_or_url:
            # Load and encode the image
            image = self.load_image(image_path_or_url)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            # Add image to the message
            message["images"] = [img_str]
        # bug
        # sys.stderr.write(f"\n===\nSYS:\n{self.system}\nPROM:\n{prompt}\n---\n")

        try:
            response = ollama.chat(
                model=self.model,
                messages=[message],
                stream=False,
                options={
                    "temperature": self.temperature,
                    "system": self.system,
                    "num_predict": self.max_tokens,
                },
            )
            return response["message"]["content"]
        except Exception as e:
            sys.stderr.write(f"Error generating content: {e}\n")
            return None


def load_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()


def main(
    prompt=None,
    prompt_file=None,
    image=None,
    system_prompt=None,
    system_prompt_file=None,
):
    """
    Interact with OllamaAI.

    Args:
        prompt (str, optional): The main prompt for the AI.
        prompt_file (str, optional): Path to a file containing the main prompt.
        image (str, optional): Path or URL to an image.
        system_prompt (str, optional): System prompt for the AI.
        system_prompt_file (str, optional): Path to a file containing the system prompt.
    """
    if prompt_file:
        prompt = load_from_file(prompt_file)
    elif not prompt:
        raise ValueError("Either 'prompt' or 'prompt_file' must be provided.")

    if system_prompt_file:
        system_prompt = load_from_file(system_prompt_file)

    ollama_ai = OllamaAI(system_prompt=system_prompt)
    response = ollama_ai.says(prompt, image)
    print(response)


if __name__ == "__main__":
    import fire

    fire.Fire(main)
