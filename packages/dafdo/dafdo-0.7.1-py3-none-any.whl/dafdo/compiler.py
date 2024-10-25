# dafdo/compiler.py

class DafdoParser:
    def __init__(self, content):
        self.content = content

    def parse(self):
        # Logika parsing sederhana; ubah sesuai kebutuhan
        # Mengganti sintaks Tulis iki menjadi HTML
        parsed_content = self.content.replace("Tulis iki", "<p>").replace("</jawa>", "</p>")
        return parsed_content


class DafdoCompiler:
    def __init__(self, file_content):
        self.file_content = file_content

    def compile(self):
        # Buat instance parser
        parser = DafdoParser(self.file_content)
        # Kembalikan hasil parsing
        return parser.parse()
