# dafdo/compiler.py

from dafdo.parser import DafdoParser

class DafdoCompiler:
    def __init__(self, file_path):
        self.file_path = file_path

    def compile(self):
        # Baca isi file .dfd
        with open(self.file_path, 'r') as file:
            code = file.read()

        # Parsing konten dengan DafdoParser
        parser = DafdoParser(code)
        parsed_code = parser.parse()

        # Tentukan nama file output
        output_path = self.file_path.replace('.dfd', '.html')
        # Simpan hasil parsing sebagai file HTML
        with open(output_path, 'w') as output_file:
            output_file.write(parsed_code)

        print(f"Compilation complete! Output saved to {output_path}")
