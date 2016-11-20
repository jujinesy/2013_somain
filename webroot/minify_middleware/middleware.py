#-*- coding: utf-8 -*-
import re

class MinifyMiddleware(object):
    spaces = re.compile(r'^\s+', re.MULTILINE)
    comments = re.compile(r'(\<!--\s*.*?((--\>)|$))', re.MULTILINE)
    blank_attrs = re.compile(r'(\s\w+\=[\'|"]{2})', re.MULTILINE)
    tag_types = re.compile(r'(\stype\=[\'|"]text\/[^template]\w+[\'|"])', re.MULTILINE)

    def process_response(self, request, response):
        if response['content-type'][:9] == 'text/html':
            response.content = self.spaces.sub('', response.content.strip())
            response.content = self.comments.sub('', response.content)
            response.content = self.blank_attrs.sub('', response.content)
            response.content = self.tag_types.sub('', response.content)
        elif response['content-type'][:8] == 'text/css':
            response.content = self.spaces.sub('', response.content.strip())
            response.content = response.content.replace('\n', '')

        response.content = response.content.replace('language="javascript"', 'type="text/javascript"')

        return response