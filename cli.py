from __future__ import print_function, unicode_literals
from datetime import datetime
import time
from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError
from src.components.extraction import extract
from src.components import summarizer
from rich.console import Console
import os


class link_validate(Validator):
    def validate(self, document):
        ok = os.path.exists(document.text) or document.text.startswith("http")
        if not ok:
            raise ValidationError(
                message="Please provide link to a valid file",
                cursor_position=len(document.text),
            )


if __name__ == "__main__":
    os.system("cls")
    questions = [
        {
            "type": "list",
            "name": "type_of_input",
            "message": "Select the type of input",
            "choices": ["Website URL", "Image", "PDF", "Docx"],
        }
    ]
    answers = prompt(questions)
    input_type = answers["type_of_input"]
    if input_type == "Website URL":
        type = 1
    elif input_type == "Image":
        type = 2
    elif input_type == "PDF":
        type = 3
    elif input_type == "Docx":
        type = 4

    questions = [
        {
            "type": "input",
            "name": "link",
            "message": "Enter the link to {} >".format(input_type),
            "validate": link_validate,
        }
    ]
    answers = prompt(questions)
    link = answers["link"]

    console = Console()
    current_time = datetime.now()
    start_time = time.time()
    with console.status("[bold green]Working on tasks...") as status:
        while True:
            data = extract(int(type), link)
            console.log("Extraction completed")
            extraction_time = time.time() - start_time

            result = summarizer.summarize(data)

            console.log("Summarization completed")
            summarizer_time = time.time() - start_time - extraction_time
            break
    result["start_time"] = current_time
    result["extraction_time"] = round(extraction_time, 3)
    result["summarizer_time"] = round(summarizer_time, 3)

    os.system("cls")
    console.print("\nRESULT GENERATED:\n", style="bold green")
    console.print("Extraction Time : ", end="", style="bold red")
    console.print(result["extraction_time"])
    console.print("Summarization Time : ", end="", style="bold red")
    console.print(result["summarizer_time"])
    console.print("Link : ", end="", style="bold red")
    console.print(result["link"])
    console.print("Type : ", end="", style="bold red")
    console.print(result["type"])
    console.print("Summarized Result : ", end="", style="bold red")
    console.print(result["summary"])
    console.print("\n====xxxxxxxxxxxx====\n", style="bold blue")
