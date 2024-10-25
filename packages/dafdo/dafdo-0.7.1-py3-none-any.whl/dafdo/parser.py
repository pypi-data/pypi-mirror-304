# dafdo/parser.py

class DafdoParser:
    def __init__(self, code):
        self.code = code
        self.parsed_code = []

    def parse(self):
        inside_dfd = False
        for line in self.code.splitlines():
            line = line.strip()

            if line == "<dfd>":
                inside_dfd = True
                self.parsed_code.append("<html><body>")
            elif line == "</jawa>":
                inside_dfd = False
                self.parsed_code.append("</body></html>")
            elif inside_dfd:
                if "Tulis iki" in line:
                    text = line.replace("Tulis iki", "").strip()
                    self.parsed_code.append(f"<p>{text}</p>")
                elif "Gambar iki" in line:
                    src = line.replace("Gambar iki", "").strip()
                    self.parsed_code.append(f"<img src='{src}' />")
        return "\n".join(self.parsed_code)
