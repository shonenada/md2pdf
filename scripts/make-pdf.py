#!/bin/env python3

import os
from datetime import datetime

import mistune
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.join(SCRIPT_PATH, '../')
TEMPLATE_PATH = os.path.join(SCRIPT_PATH, 'templates')
TARGET_FOLDER = os.path.join(SCRIPT_PATH, 'target')
NAME_PREFIX = "pdf"

styles = ('base.css', 'custom.css')

jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

markdowns = ('docs/chap1.md',
             'docs/chap2.md',)


def render_markdown(filename):
    content = None
    path = os.path.join(ROOT_PATH, filename)
    with open(path, 'r') as infile:
        content = infile.read()
    if content is not None:
        return mistune.markdown(content)


def render_template(tpl_path, **kwargs):
    tpl = jinja_env.get_template(tpl_path)
    return tpl.render(**kwargs)


def ensure_folder(folder):
    if os.path.isfile(folder):
        raise RuntimeError('%s: File exists' % folder)

    if not os.path.isdir(folder):
        os.mkdir(folder)


def main():
    pages = [render_markdown(md) for md in markdowns]
    date = datetime.now().strftime('%Y-%m')
    title = '%s-%s.pdf' % (NAME_PREFIX, date)
    pdf_content = render_template('pdf.html', title=title, date=date, pages=pages)
    ensure_folder(TARGET_FOLDER)
    target = os.path.join(TARGET_FOLDER, title)
    stylesheets = [os.path.join(SCRIPT_PATH, 'styles', p) for p in styles]
    HTML(string=pdf_content, base_url=SCRIPT_PATH).write_pdf(
        target, stylesheets=stylesheets)
    print('Genreated PDF: %s' % target)


if __name__ == '__main__':
    main()
