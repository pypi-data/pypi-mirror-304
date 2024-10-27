# pip install js2py requests

import os
import re

import requests
import js2py

VERSION = "4.7.8"

# using min: 427 kb py file, else 507 kb
handlebars_js_url = f"https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/{VERSION}/handlebars.js"

# set paths
build_dir_path = os.path.dirname(__file__)
src_dir_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "src", "handlebars"
)
handlebars_js_path = os.path.join(build_dir_path, "handlebars.js")
handlebars_py_path = os.path.join(src_dir_path, "handlebars_js.py")

# download handlebars.js
r = requests.get(handlebars_js_url, allow_redirects=True)
with open(handlebars_js_path, 'wt') as f:
    f.write(r.text)

# transpile handlebars.js to handlebars.py
js2py.translate_file(handlebars_js_path, handlebars_py_path)

# cleanup
os.remove(handlebars_js_path)

# patch

patch = """
# mustache.js uses a 'hack' to specify globalThis -> not supported by js2py
# see: https://mathiasbynens.be/notes/globalthis
# see: https://github.com/PiotrDabkowski/Js2Py/issues?q=is%3Aissue+__defineGetter__
# workaround: define the missing variables
@Js
def __defineGetter__(key, func):
    var.get('Object').get('prototype').put(str(key), func)
__defineGetter__._set_name('__defineGetter__')
var.get('Object').get('prototype').put('__defineGetter__', __defineGetter__)
var.put('__magic__', var.get(u"this"))

"""

with open(handlebars_py_path, "rt") as f:
    py_code = f.read()

# add path after 'set_global_object' statement
py_code = re.sub(
    r"(set_global_object\(var\)\n)",
    r"\1" + patch,
    py_code,
    1,
)

with open(handlebars_py_path, "wt") as f:
    f.write(py_code)

