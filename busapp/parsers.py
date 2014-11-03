from django.utils import six

from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
from rest_framework import renderers

import json


class JSONLatinParser(BaseParser):
    """
    Parses JSON-serialized data encoded in iso-8859-1.
    """
    media_type = 'application/json'
    renderer_class = renderers.UnicodeJSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as JSON and returns the resulting data.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', 'iso-8859-1')

        try:
            data = stream.read().decode(encoding)
            return json.loads(data)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))
