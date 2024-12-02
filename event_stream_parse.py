import re

def parse(content):
    content = re.sub('<!DOCTYPE html>','', content)
    content = re.sub('<html.+','', content)
    content = re.sub('</html>','', content)
    content = re.sub('\n', '\ndata: ', content)
    return content