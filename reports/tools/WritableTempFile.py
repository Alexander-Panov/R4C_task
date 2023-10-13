import os
import tempfile


class WritableTempFile:
    """
    Avoid "Permission denied error" on Windows:
      with tempfile.NamedTemporaryFile("w", suffix=".gv") as temp_file:
        # Not writable on Windows:
        # https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile
        # https://stackoverflow.com/questions/66744497/python-tempfile-namedtemporaryfile-cant-use-generated-tempfile

    Example:
        with WritableTempFile("w", suffix=".gv") as temp_file:
            tree.to_dotfile(temp_file.name)
    """

    def __init__(self, mode="w+b", *, encoding=None, suffix=None):
        self.mode = mode
        self.encoding = encoding
        self.suffix = suffix

    def __enter__(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            self.mode, encoding=self.encoding, suffix=self.suffix, delete=False
        )
        return self.temp_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temp_file.close()
        os.unlink(self.temp_file.name)  # manually clearing tempfile - because of delete=False
