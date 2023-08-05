import secrets
import time
from treepoem import generate_barcode
from PIL import Image as PILImage

BASE62 = 'A1234567890BCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwyzx'


class MUID:
    """
    Instances of the MUID (Micro Unique ID) class represent MUIDs.
    MUID objects are immutable, hashable, and usable as dictionary keys.
    Converting a MUID to a string with str() yields something in the form
    '8OV50-Qalh-x6ygB'.
    """

    __slots__ = ('id', 'int', '__weakref__')

    def __init__(self, value=None):
        if value is None:
            value = self.__generate__()
        else:
            value = self.__validate__(value)

        object.__setattr__(self, 'id', value)
        object.__setattr__(self, 'int', self.get_int())

    @staticmethod
    def id_to_simple(value):
        value = value.replace('-', '')
        return value

    @staticmethod
    def simple_to_id(value):
        base62 = value
        pretty = base62[:4] + '-' + base62[4:8] + '-' + base62[8:12]
        return pretty

    @staticmethod
    def __generate__():
        timestamp = int(time.time() * 1000)
        base62 = ''
        while timestamp > 0:
            timestamp, remainder = divmod(timestamp, 62)
            base62 = BASE62[remainder] + base62
        base62 = base62.rjust(8, secrets.choice(BASE62))[0:8]
        base62 = base62 + ''.join(secrets.choice(BASE62) for _ in range(4))
        return base62[:4] + '-' + base62[4:8] + '-' + base62[8:12]

    @staticmethod
    def encode_base62(n):
        """Encode an integer into a base62 string."""
        if n == 0:
            return BASE62[0]
        arr = []
        base = len(BASE62)
        while n:
            rem = n % base
            n = n // base
            arr.append(BASE62[rem])
        arr.reverse()
        return ''.join(arr)

    def from_int(self, n):
        s = self.encode_base62(n)
        s = self.from_string(s)
        return s

    def from_string(self, s):
        if s.isdigit():
            s = self.encode_base62(int(s))
        else:
            s = s.replace('-', '')
        if len(s) > 12:
            raise ValueError('Invalid MUID length. you need 12 characters and you have {}'.format(len(s)))
        for char in s:
            if char not in BASE62:
                raise ValueError('Invalid MUID.')
        if len(s) < 12:
            s = s.rjust(12, 'A')[0:12]
        return s[:4] + '-' + s[4:8] + '-' + s[8:12]

    def from_hex(self, s):
        bytes_object = bytes.fromhex(s)
        intiger = int.from_bytes(bytes_object, 'big')
        s = self.encode_base62(intiger)
        s = self.from_string(s)
        return s

    def from_bytes(self, s):
        intiger = int.from_bytes(s, 'big')
        s = self.encode_base62(intiger)
        s = self.from_string(s)
        return s

    def __validate__(self, value):
        """instance validation
        :param value: str or int or hex or bytes
        :return: muid
        """
        if isinstance(value, MUID):
            return value.id
        if isinstance(value, int):
            return self.from_int(value)
        if isinstance(value, str):
            value = value.replace('-', '')
            if value.isdigit():
                return self.from_int(int(value))
            if len(value) == 12:
                return self.from_string(value)
            if len(value) == 18:
                return self.from_hex(value)
        if isinstance(value, bytes):
            if len(value) == 9:
                return self.from_bytes(value)
        raise ValueError('Invalid MUID.')

    def __getstate__(self):
        d = {'id': self.id, 'int': self.int}
        return d

    def __setstate__(self, state):
        object.__setattr__(self, 'id', state['id'])
        object.__setattr__(self, 'int', state['int'])

    def __eq__(self, other):
        if isinstance(other, MUID):
            return self.int == other.int
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, MUID):
            return self.int < other.int
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, MUID):
            return self.int > other.int
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, MUID):
            return self.int <= other.int
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, MUID):
            return self.int >= other.int
        return NotImplemented

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __setattr__(self, name, value):
        raise TypeError('MUID objects are immutable')

    def __str__(self):
        return self.id

    @property
    def simple(self):
        return self.id.replace('-', '')

    @property
    def bytes(self):
        return self.int.to_bytes(9, 'big')

    @property
    def hex(self):
        return self.int.to_bytes(9, 'big').hex()

    def get_int(self):
        intiger = 0
        for char in self.id.replace('-', ''):
            intiger = intiger * 62 + BASE62.index(char)
        return intiger

    def image_code(self, class_name, scale=1):
        img = generate_barcode(class_name, self.simple)
        img = img.convert('RGB')
        img = img.resize((img.width * scale, img.height * scale))
        return img

    def composed_code(self, ct, h=100):
        img2 = generate_barcode('azteccode', self.id)
        img = generate_barcode('datamatrixrectangularextension', ct)
        """resize proportionally"""
        img2 = img2.resize((h, int(img2.height * h / img2.width)))
        img = img.resize((h, int(img.height * h / img.width)))
        """rotate img"""
        img = img.rotate(90, expand=True)
        """resize img width plus img2 width"""
        image = PILImage.new('RGB', (img2.width + img.width, img.height))
        """paste img"""
        image.paste(img, (0, 0))
        """paste img2"""
        image.paste(img2, (img.width, 0))
        return image

    @property
    def qr_code(self):
        return self.image_code('microqrcode')
