import re

def parse(content):
    content = re.sub('.*html.*','', content)
    content = re.sub("'''", '', content)
    content = re.sub("```", '', content)
    content = re.sub( r'src=[\'\"]([\w/]*.[\w]*)[\'\"]' , r'src="{{url_for("static", filename="\1")}}"' ,content)
    return content

def event_streamify(content):
    content = re.sub('\n', '\ndata: ', content)
    return f'data: <div>{content}\ndata:</div>\n\n'