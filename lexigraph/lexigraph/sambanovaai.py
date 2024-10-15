import os
import openai
from io import BytesIO
from PIL import Image
import base64

DEFAULT_MODEL = 'Meta-Llama-3.1-8B-Instruct'
DEFAULT_MODEL = 'Meta-Llama-3.1-405B-Instruct'
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant. You reply with short, accurate answers."

class SambanovaAI:
    def __init__(self, model=DEFAULT_MODEL, system_prompt=None, max_tokens=3000, temperature=0.1, top_p=0.1):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.system = self.set_system(system_prompt)
        self.llm = openai.OpenAI(
            api_key=os.environ.get("SAMBANOVA_API_KEY"),
            base_url="https://api.sambanova.ai/v1",
        )

    def set_system(self, system):
        if system:
            return system
        return DEFAULT_SYSTEM_PROMPT

    def says(self, prompt, PathUrlBase64=None):
        if PathUrlBase64:
            # Load and encode the image
            image = self.load_image(PathUrlBase64)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            # Add image to the message
            response = self.llm.chat.completions.create(
                model=self.model,
                messages=[{"role":"system","content":self.system},{"role":"user","content":prompt}],
                image_embeddings=[img_str],
                temperature=self.temperature,
                top_p = self.top_p
            )
            return response.choices[0].message.content


        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[{"role":"system","content":self.system},{"role":"user","content":prompt}],
            temperature =  self.temperature,
            top_p = self.top_p
        )
        return response.choices[0].message.content

    def load_image(self, PathUrlBase64):
        """
        Returns an image object from a path, URL or base64 encoded image data.
        """
        if PathUrlBase64.startswith(('http://', 'https://')):
            response = requests.get(PathUrlBase64)
            img = Image.open(BytesIO(response.content))
        elif PathUrlBase64.startswith('data:image'):
            img_data = PathUrlBase64.split(',')[1]
            img = Image.open(BytesIO(base64.b64decode(img_data)))
        else:
            img = Image.open(PathUrlBase64)
        return img


# -----

def main(prompt, system_prompt=None):
    if not prompt:
        raise ValueError("Please provide a prompt.")
    if system_prompt:
        with open(system_prompt, 'r') as file:
            system = file.read().strip()
            llm = SambanovaAI(system=system)
    else:
        llm = SambanovaAI()

    response = llm.says(prompt)
    print(response)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
