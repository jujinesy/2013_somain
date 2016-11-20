#-*- coding: utf-8 -*-
@register.simple_tag
def active(request, pattern):
    import re
    path = request.path.replace("/admin", "")
    if re.search(pattern, request.path):
        return ' class="active"'
    return ""