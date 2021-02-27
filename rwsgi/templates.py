from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
import os

def render(template_name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    tmpl = env.get_template(template_name)
    return tmpl.render(**kwargs)