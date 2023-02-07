#pip3 install barcode
from barcode import EAN13
from barcode.writer import ImageWriter

codigo_barra = EAN13("123456789", writer=ImageWriter())
codigo_barra.save("codigo_barra")