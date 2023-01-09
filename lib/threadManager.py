import os


for d,fo,fi in os.walk('/Users/barhaymovich/tools/dev/albert'):
    if '.git' not in d:
        for i in fi:
            if '.git' not in i:
                p = os.path.join(d,i)
                _com = f'echo "" >> {p}'
                os.system(_com)

