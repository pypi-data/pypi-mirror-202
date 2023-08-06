import io
from pathlib import Path


class Writer:
    def __init__(self):
        self.WRITER = io.StringIO()

    def append(self,md: str):
        self.WRITER.write(md+'\n')

    def clear(self,):
        self.WRITER.seek(0)
        self.WRITER.truncate(0)

    def store(self,path:str, overwrite = True):
        path_ = Path(path)
        if path_.exists():
            if not overwrite:
                raise RuntimeError("The path already exists.")

        path_.write_text(self.WRITER.getvalue(),encoding="utf-8")
    def getValue(self):
        return self.WRITER.getvalue()