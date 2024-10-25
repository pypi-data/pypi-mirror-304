# dafdo/compiler.py

from dafdo.parser import DafdoParser

class DafdoCompiler:
    def __init__(self, file_path):
        self.file_path = file_path

    def compile(self):
        with open(self.file_path, 'r') as file:
            code = file.read()

        parser = DafdoParser(code)
        parsed_code = parser.parse()

        output_path = self.file_path.replace('.dfd', '.html')
        with open(output_path, 'w') as output_file:
            output_file.write(parsed_code)

        print(f"Compilation complete! Output saved to {output_path}")
