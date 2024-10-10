import graphviz
from io import StringIO
import base64
import sys

class Lexigraph:
    def __init__(self, llm='gemini', system='system.txt'):
        self.graph = None
        try:
            with open(system, 'r') as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            sys.stderr.write(f"System prompt file not found: {system}\n")
            self.system_prompt = 'You are a star news reporter. You pay attention to what, where, why, who, when and how to answer questions.'
        if llm == 'gemini':
            from geminiai import GeminiAI
            self.llm = GeminiAI()
        else:
            raise ValueError(f"Invalid LLM: {llm}")
        self.llm.set_system(self.system_prompt)

    def imagine(self, prompt, format='png'):
        """
        Create a dotfile using an LLM and render it to an image.

        :param input_data: File path, list of strings, or dot content string
        :param format: Output format (e.g., 'png', 'svg', 'pdf')
        :return: Path to the rendered image
        """
        # dot_content, base64_image = self.imagine_for_llm(prompt, format=format)
        dot_content, image_path = self.imagine_for_llm(prompt, format='png')
        meh = self.llm.says(prompt)
        ans = self.llm.says(prompt, image_path)
        return meh, ans

    def imagine_for_llm(self, prompt, format='png'):
        """
        Create a dotfile using an LLM and render it to an image for LLM inference.

        :param input_data: File path, list of strings, or dot content string
        :param format:
        """
        dot_content = self.llm.says(prompt)

        # Extract dot content
        start_marker = "```dot"
        end_marker = "```"
        start_index = dot_content.find(start_marker)
        end_index = dot_content.find(end_marker, start_index + len(start_marker))

        if start_index != -1 and end_index != -1:
            dot_content = dot_content[start_index + len(start_marker):end_index].strip()
        else:
            raise ValueError("Dot content not found between ```dot and ``` markers")


        # base64_image = self.render_for_llm(dot_content, format=format)
        base64_image = self.render_to_file(dot_content, format=format)
        return dot_content, base64_image

    def _create_graph(self, input_data):
        """
        Create a graphviz.Source object from input data.

        :param input_data: Either a file path, list of strings, or a single string
        :return: graphviz.Source object
        """
        if isinstance(input_data, str):
            # Check if it's a file path
            if input_data.endswith('.dot') or input_data.endswith('.gv'):
                with open(input_data, 'r') as f:
                    dot_content = f.read()
            else:
                # Treat it as dot content string
                dot_content = input_data
        elif isinstance(input_data, list):
            # Join lines into a single string
            dot_content = '\n'.join(input_data)
        else:
            raise ValueError("Input must be a file path, list of strings, or a dot content string")

        return graphviz.Source(dot_content)

    def render_to_file(self, input_data, output_file='output', format='png'):
        """
        Render a GraphViz image and save to a file.

        :param input_data: File path, list of strings, or dot content string
        :param output_file: Name of the output file (without extension)
        :param format: Output format (e.g., 'png', 'svg', 'pdf')
        :return: Path to the rendered image
        """
        self.graph = self._create_graph(input_data)

        try:
            # Render the graph
            rendered_path = self.graph.render(filename=output_file, format=format, cleanup=True)
            print(f"Image rendered successfully: {rendered_path}")
            return rendered_path
        except graphviz.ExecutableNotFound:
            print("Error: Graphviz executable not found. Please install Graphviz.")
        except Exception as e:
            print(f"An error occurred while rendering the image: {str(e)}")

    def render_to_bytes(self, input_data, format='png'):
        """
        Render a GraphViz image and return as bytes.

        :param input_data: File path, list of strings, or dot content string
        :param format: Output format (e.g., 'png', 'svg', 'pdf')
        :return: Bytes of the rendered image
        """
        self.graph = self._create_graph(input_data)

        try:
            # Render the graph to bytes
            image_bytes = self.graph.pipe(format=format)
            print(f"Image rendered successfully as bytes")
            return image_bytes
        except graphviz.ExecutableNotFound:
            print("Error: Graphviz executable not found. Please install Graphviz.")
        except Exception as e:
            print(f"An error occurred while rendering the image: {str(e)}")

    def render_for_llm(self, input_data, format='png'):
        """
        Render a GraphViz image and return as a base64 encoded string for LLM inference.

        :param input_data: File path, list of strings, or dot content string
        :param format: Output format (e.g., 'png', 'svg', 'pdf')
        :return: Base64 encoded string of the rendered image
        """
        image_bytes = self.render_to_bytes(input_data, format)
        if image_bytes:
            base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
            return f"data:image/{format};base64,{base64_encoded}"
        return None

# Example usage
if __name__ == "__main__":
    renderer = Lexigraph()

    # Example dot file content
    dot_content = """
    digraph G {
        A -> B;
        B -> C;
        C -> A;
    }
    """

    salt = "sample"
    with open('preamble.txt', 'r') as f:
        preamble = f.read()
    with open('article.txt', 'r') as f:
        article = f.read()
    prompt = preamble + article
    meh, ans = renderer.imagine(prompt)

    print(f"LLM says:\nMEH:\n<{meh}>\n\nANS:\n<{ans}>\n")

    # # Render from string to file
    # renderer.render_to_file(dot_content, output_file=salt, format='png')

    # with open(f"{salt}.dot", 'w') as f:
    #     f.write(dot_content)

    # # Render from file
    # renderer.render_to_file(f"{salt}.dot", output_file=salt, format='svg')

    # # Render to bytes
    # image_bytes = renderer.render_to_bytes(dot_content, format='png')
    # if image_bytes:
    #     print(f"Image size: {len(image_bytes)} bytes")

    # # Render for LLM inference
    # llm_encoded = renderer.render_for_llm(dot_content, format='png')
    # if llm_encoded:
    #     print(f"LLM encoded image (truncated): {llm_encoded[:50]}...")
