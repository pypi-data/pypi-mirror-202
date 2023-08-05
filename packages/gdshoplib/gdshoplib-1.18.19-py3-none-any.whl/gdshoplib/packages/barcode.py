class BaseCodeManager:
    CODE = None

    def read(self, image):
        raise NotImplementedError

    def generate(self, code):
        raise NotImplementedError


class EAN13(BaseCodeManager):
    ...


class Barcode:
    def __init__(self, key, code_type=EAN13):
        self.type = code_type
        self.key = key

    @classmethod
    def read(cls, image, /, code_type):
        ...

    def generate(self):
        ...
