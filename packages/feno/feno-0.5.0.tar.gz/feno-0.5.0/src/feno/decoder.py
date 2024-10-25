import chardet

class Decoder:

    @staticmethod
    def load(file_path: str) -> str:
        with open(file_path, "rb") as file:
            raw_data = file.read()
            encoding = chardet.detect(raw_data)["encoding"]
            if encoding is None:
                encoding = "utf-8"
            return raw_data.decode(encoding)

    @staticmethod
    def save(file_path: str, content: str):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
