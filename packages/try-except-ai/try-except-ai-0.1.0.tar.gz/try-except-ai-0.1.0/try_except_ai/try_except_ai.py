import os
import traceback

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class TryExceptAI:
    code_snippet_lines_limit = 5

    def handle_exception(self, exception: BaseException):
        """
        This method will catch the exception information and provide a suggestion
        for resolution based on the error type.
        """
        exc_type = type(exception)
        exc_value = exception
        exc_traceback = exception.__traceback__

        file_path, line_number, function_name, _ = traceback.extract_tb(exc_traceback)[
            -1
        ]
        error_message = f"{exc_type.__name__}: {exc_value}"

        code_snippet = self.get_code_snippet(file_path, line_number)

        print(f"Error caught in file: {file_path}")
        print(f"Line number: {line_number}")
        print(f"Function name: {function_name}")
        print(f"Error message: {error_message}")

        self.suggest_resolution(error_message, code_snippet)

    @staticmethod
    def suggest_resolution(error_message, code_snippet: str):
        """
        Ask ChatGPT API suggestions to resolve the error
        """
        prompt = (
            f"I encountered this error: {error_message}"
            f"\n\nCode snippet: {code_snippet}"
            "\n\nHow can I resolve this issue?"
        )

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0,
        )

        suggestion = response.choices[0].text.strip()
        print(f"Suggested resolution: {suggestion}")

    def get_code_snippet(self, file_path: str, line_number: int):
        """
        This method extracts the code snippet from the file content.
        """
        start_line = max(line_number - self.code_snippet_lines_limit - 1, 0)
        end_line = line_number + self.code_snippet_lines_limit

        with open(file_path) as f:
            lines = f.readlines()

        code_snippet = "".join(
            line.rstrip() + "\n" for line in lines[start_line:end_line]
        )

        return code_snippet
