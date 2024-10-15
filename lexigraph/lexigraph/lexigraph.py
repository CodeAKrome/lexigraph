import graphviz
from io import StringIO
import base64
import sys
from rich.markdown import Markdown, Console
import subprocess
import os

IMGCAT = "/Users/kyle/.iterm2/imgcat"
DEFAULT_LLM = "ollama"
DEFAULT_SYSTEM_PROMPT = "You are a star news reporter. You pay attention to what, where, why, who, when and how to answer questions."
DEFAULT_GRAPH_PROMPT = """
Use the following to answer questions:
Object Graphs: In computer science, object graphs represent a network of objects connected through their relationships, either directly or indirectly. These relationships are modeled as edges between nodes (objects) in a directed graph, which may be cyclic.
Knowledge Graphs: Knowledge graphs are a type of graph data structure that represents entities (nodes) and their relationships (edges) as triples (subject-predicate-object). This allows for the storage and querying of semantic facts and schema models.
RDF Triplestore: RDF triplestores are a specific type of graph database that stores semantic facts as subject-predicate-object triples. This format enables the representation of relationships between entities using Universal Resource Identifiers (URIs) as unique identifiers.
Subject-Verb Agreement: In grammar, subject-verb agreement refers to the rule that the verb should agree with the subject (singular or plural) in number. This applies to sentences with compound subjects connected by “or” or “nor”.
Subject-Verb-Object Word Order: In linguistic typology, the subject-verb-object (SVO) word order is a common sentence structure where the subject comes first, followed by the verb, and then the object.

Graph relationships can be represented as directed edges between nodes (objects) or as subject-predicate-object triples.
Knowledge graphs and RDF triplestores are specific types of graph databases designed for storing and querying semantic facts.
Subject-verb agreement in grammar ensures that the verb agrees with the subject in number.
The subject-verb-object word order is a common sentence structure in many languages.

Entity Meaning Example
CARDINAL cardinal value 1, 2, 3, ...
DATE date value 2023-12-25, January 1st
EVENT event name Super Bowl, Olympics
FAC building name Empire State Building, Eiffel Tower
GPE geo-political entity United States, France
LANGUAGE language name English, Spanish
LAW law name Constitution, Copyright Act
LOC location name New York City, Paris
MONEY money name dollar, euro
NORP affiliation Republican, Democrat
ORDINAL ordinal value first, second, third
ORG organization name NASA, Google
PERCENT percent value 50%, 75%
PERSON person name John Doe, Jane Smith
PRODUCT product name iPhone, MacBook
QUANTITY quantity value 10, 20
TIME time value 12:00 PM, 5:30 AM
WORK_OF_ART name of work of art Mona Lisa, Star Wars
Using those rules, create a Knowledge Graph using a graphviz dotfile to represent the relationships and entities in the following news article:
"""


class Lexigraph:
    def __init__(
        self,
        graph_type="dotfile",
        llm=DEFAULT_LLM,
        model=None,
        system_prompt=None,
        graph_prompt=None,
        graph_file=None,
    ):
        self.graph = None
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        if not system_prompt:
            system_prompt = f"{self.file_dir}/prompts/system.txt"
        self.system_prompt = self._system_prompt(system_prompt)
        self.graph_type = graph_type
        self.graph_file = f"{graph_type}.txt"
        if graph_prompt:
            self.graph_file = graph_prompt
        self.graph_prompt = self.set_graph_prompt(self.graph_file)
        self.console = Console()
        self.llm = self._llm(llm, model)
        # sys.stderr.write(f"SYS: {self.system_prompt}\n")

        try:
            self.llm.set_system(self.system_prompt)
        except Exception as e:
            sys.stderr.write(f"Error setting system prompt: {e}\n")

    def _llm(self, llm, model):
        # bug
        # sys.stderr.write(f"LLM: {llm} Model: {model}\nPROMPT: {self.system_prompt}\n")
        sys.stderr.write(f"LLM: {llm} Model: {model}\n")

        if llm == "gemini":
            from geminiai import GeminiAI

            if model:
                return GeminiAI(system_prompt=self.system_prompt, model=model)
            return GeminiAI(system_prompt=self.system_prompt)
        elif llm == "ollama":
            from ollamaai import OllamaAI

            if model:
                return OllamaAI(system_prompt=self.system_prompt, model=model)
            return OllamaAI(system_prompt=self.system_prompt)
        elif llm == "sambanova":
            from sambanovaai import SambanovaAI

            if model:
                return SambanovaAI(system_prompt=self.system_prompt, model=model)
            return SambanovaAI(system_prompt=self.system_prompt)
        else:
            raise ValueError(f"Invalid LLM: {llm}")

    def set_graph_prompt(self, graph_file):
        try:
            with open(graph_file, "r") as f:
                return f.read()
        except FileNotFoundError:
            sys.stderr.write(
                f"Graph prompt file not found: {graph_file}. Using default graph prompt.\n"
            )
            return DEFAULT_GRAPH_PROMPT

    def _system_prompt(self, system):
        try:
            with open(system, "r") as f:
                return f.read()
        except FileNotFoundError:
            sys.stderr.write(
                f"System prompt file not found: {system}. Using default system prompt.\n"
            )
            return DEFAULT_SYSTEM_PROMPT

    def set_system(self, system):
        self.llm.set_system(system)
        self.system_prompt = system

    def imagine(self, prompt, rag=[], output_file=None, format="png"):
        """
        Create a dotfile using an LLM and render it to an image.

        :param input_data: File path, list of strings, or dot content string
        :param format: Output format (e.g., 'png', 'svg', 'pdf')
        :return: Path to the rendered image
        """
        # dot_content, base64_image = self.imagine_for_llm(prompt, format=format)

        # bug
        # sys.stderr.write(f"\nRAG: {rag[0]} output_file: {output_file} format: {format}\n")

        graph_content, base64_image = self.create_image(
            rag, output_file=output_file, format=format
        )
        if not graph_content or not base64_image:
            sys.stderr.write(f"\nNO IMAGE OUTPUT\n")
            exit(1)
            return None, None
        meh_prompt = rag[0] + "\n" + prompt

        meh = self.llm.says(meh_prompt)

        # bug
        sys.stderr.write(f"RAW MEH:\n{meh}\n")

        # graph_system = self.system_prompt + "\nThe image shows a digraph of the relationships between the entities in the article.\nDo not refer to the image in your answer, it is for reference only.\n"
        graph_system = self.system_prompt

        # bug
        # sys.stderr.write(f"\nGRAPH_SYSTEM: {graph_system}\n")

        # This should get restored after the image is rendered
        self.llm.set_system(graph_system)

        # RECS 32 35 46 48 59 87
        # unrelated 92

        # bug
        sys.stderr.write(f"\nIMG: {base64_image[:16]}\n")

        ans = self.llm.says(meh_prompt, base64_image)

        # bug
        sys.stderr.write(f"RAW ANS:\n{ans}\n")

        return meh, ans

    def create_image(self, rag, output_file=None, format="png"):
        """
        Create dot or cypher statements using an LLM and render it to an image for LLM inference.

        :param input_data: File path, list of strings, or dot content string
        :param format:
        """

        if not output_file:
            output_file = f"{self.file_dir}/output"

        # bug
        # output_file = 'output'
        sys.stderr.write(f"\nOUTPUT_FILE: ->{output_file}<-\n")

        # graph_prompt = self.graph_prompt + rag[0] + "\n"
        # foo = "Show relationships in dot file like:\nHossein_Daghighi -> advisor_to [label=\"advisor to\"];\n"
        foo = 'Example:\nIsrael wants war with Iran.\n"Israel" -> "Iran" [label="wants war"];\n'
        foo += "You will represent all the marked entities, leaving none out, in relationships in a graphviz dot file.\n"
        foo += "Create a Knowledge Graph using a graphviz dot file to represent the relationships and entities in the following news article(s):\n"

        # HACK swapping prompts
        graph_prompt = self.system_prompt + rag[0] + "\n"
        self.set_system(foo)
        # graph_prompt = foo + rag[0] + "\n"

        # bug
        sys.stderr.write(
            f"\n---\nGRAPH\nSYSTEM: {self.system_prompt}\nGRAPH PROMPT: {graph_prompt}\n===\n"
        )

        graph_content = self.llm.says(graph_prompt)

        if not graph_content:
            sys.stderr.write(f"ERROR: LLM gave no response\n")
            return None, None

        # bug
        # sys.stderr.write(f"\nGRAPH:==\n{graph_content}\n==\n")

        recs = graph_content.split("\n")
        out = []
        oneshot = False
        b = "{"
        e = "}"

        for rec in recs:
            if b in rec:
                # sys.stderr.write(f"START: {rec}\n")
                oneshot = "Begin"

            if oneshot:
                out.append(rec)
                sys.stderr.write(f"{rec}\n")
            else:
                sys.stderr.write(f"=> {rec}\n")

            if e in rec:
                oneshot = "End"
                # sys.stderr.write(f"END: {rec}\n")

                break

        graph_content = "\n".join(out)

        # If oneshot wasn't closed properly, this is a brken graph.
        # This is probably because max_tokens killed th output. Try setting it higher.
        if oneshot != "End":
            sys.stderr.write(
                f"ERROR: Graph not closed properly, oneshot={oneshot}\nINCOMPLETE GRAPH:\n{graph_content}\n"
            )
            exit(1)

        # bug
        # sys.stderr.write(f"\nOUT -> GRAPH:==>>\n{graph_content}\n==\n")

        # # Extract dot content
        # start_marker = "```dot"
        # start_marker = "{"
        # end_marker = "```"
        # start_index = graph_content.find(start_marker)
        # end_index = graph_content.find(end_marker, start_index + len(start_marker))

        # if start_index != -1 and end_index != -1:
        #     graph_content = graph_content[start_index + len(start_marker):end_index].strip()
        # else:

        #     # bug
        #     sys.stderr.write("No dots\n")
        #     # raise ValueError("Graph content not found between ```dot and ``` markers")

        base64_image = self.render_for_llm(graph_content, format=format)

        # bug
        # sys.stderr.write(f"\nRENDER GRAPH_CONTENT: {graph_content}\n")

        try:
            self.outfile = self.render_to_file(graph_content, output_file=output_file)
        except Exception as e:
            sys.stderr.write(f"Error rendering image: {e}\n")

        # Print pretty picture
        try:
            subprocess.run([IMGCAT, self.outfile])
        except Exception as e:
            sys.stderr.write(f"Error running imgcat at path: {IMGCAT}\n")
        return graph_content, base64_image

    def _create_graph(self, input_data):
        """
        Create a graphviz.Source object from input data.

        :param input_data: Either a file path, list of strings, or a single string
        :return: graphviz.Source object
        """
        if isinstance(input_data, str):
            # Check if it's a file path
            if input_data.endswith(".dot") or input_data.endswith(".gv"):
                with open(input_data, "r") as f:
                    dot_content = f.read()
            else:
                # Treat it as dot content string
                dot_content = input_data
        elif isinstance(input_data, list):
            # Join lines into a single string
            dot_content = "\n".join(input_data)
        else:
            raise ValueError(
                "Input must be a file path, list of strings, or a dot content string"
            )

        return graphviz.Source(dot_content)

    def render_to_file(self, input_data, output_file=None, format="png"):
        """
        Render a GraphViz image and save to a file.

        :param input_data: File path, list of strings, or dot content string
        :param output_file: Name of the output file (without extension)
        :param format: Output format (e.g., 'png', 'svg', 'pdf')
        :return: Path to the rendered image
        """
        self.graph = self._create_graph(input_data)
        if not output_file:
            output_file = f"{self.file_dir}/output"
        try:
            # Render the graph
            rendered_path = self.graph.render(
                filename=output_file, format=format, cleanup=True
            )
            print(f"Image rendered successfully: {rendered_path}")
            return rendered_path
        except graphviz.ExecutableNotFound:
            print("Error: Graphviz executable not found. Please install Graphviz.")
        except Exception as e:
            print(f"An error occurred while rendering the image: {str(e)}")

    def render_to_bytes(self, input_data, format="png"):
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

    def render_for_llm(self, input_data, format="png"):
        """
        Render a GraphViz image and return as a base64 encoded string for LLM inference.

        :param input_data: File path, list of strings, or dot content string
        :param format: Output format (e.g., 'png', 'svg', 'pdf')
        :return: Base64 encoded string of the rendered image
        """
        image_bytes = self.render_to_bytes(input_data, format)
        if image_bytes:
            base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
            return f"data:image/{format};base64,{base64_encoded}"
        return None


# Example usage
if __name__ == "__main__":
    file_dir = os.path.dirname(os.path.abspath(__file__))
    prompt = "Summarize the news article below:\n\n"

    # renderer = Lexigraph(model='bespoke-minicheck:latest')
    # renderer = Lexigraph(llm='gemini')
    if len(sys.argv) > 1:
        llm = sys.argv[1]
        model = sys.argv[2]
        ragfile = sys.argv[3]
        prompt = sys.argv[4]
        # renderer = Lexigraph(llm=llm, model=model
        # renderer = Lexigraph(llm=llm, model=model)
        dot2 = f"{file_dir}/prompts/dotfile2.txt"
        # renderer = Lexigraph(llm=llm, model=model, graph_prompt=dot2, prompt=dot2)
        renderer = Lexigraph(
            llm=llm, model=model, graph_prompt=dot2, system_prompt=dot2
        )
    else:
        renderer = Lexigraph(llm="ollama")

    # Example dot file content
    # dot_content = """
    # digraph G {
    #     A -> B;
    #     B -> C;
    #     C -> A;
    # }
    # """

    # salt = "sample"

    with open(f"{file_dir}/rag/{ragfile}", "r") as f:
        article = f.read()

    # prompt = "When is the best time to see an aurora in New Jersey?"
    # prompt = "Wat are the chances of a peace treaty between Russia and Ukraine?"

    print(f"===> Prompt: {prompt}<=====\n\n")
    meh, ans = renderer.imagine(prompt, [article])

    # print("\n========\n")
    # print(f"RAW MEH:\n{meh}\n\nRAW ANS:\n{ans}\n")

    # print("\n========\n\n\n")

    # Pretty print
    mdmeh = Markdown(meh)
    mdans = Markdown(ans)

    console = Console()

    console.print(mdmeh)
    print("\n========\n")
    console.print(mdans)

    # print(f"LLM says:\nMEH:\n<{mdmeh}>\n\nANS:\n<{mdans}>\n")

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
