import base64
from odoo import http
from odoo.http import request
import barcode
from barcode.writer import ImageWriter
import os


class BarcodeController(http.Controller):
    @http.route('/generate_barcode', type='http', auth="public")
    def generate_barcode(self, barcode_value):
        if barcode_value:
            barcode_class = barcode.get_barcode_class('code128')
            barcode_obj = barcode_class(barcode_value, writer=ImageWriter())
            barcode_obj.save('/tmp/barcode')
            with open('/tmp/barcode.png', 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read())
            try:
                os.remove('/tmp/barcode.png')
            except OSError:
                pass
            return request.make_response(encoded_string,
                                         [('Content-Type', 'image/png')])
        return request.not_found()
