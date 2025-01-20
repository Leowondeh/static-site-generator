import os, sys, platform, logging, shutil

from block_markdown_parsers import markdown_to_html_node
from inline_markdown_parsers import extract_title

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

os_type = platform.system()

# paths are relative to executor (main.sh in this case)
static_path = 'static'
public_path = 'public'

content_path = 'content'
template_path = 'template.html'

def main():
    logging.info('Static site generator v0.1.0 | https://github.com/Leowondeh/static-site-generator')

    # Check static/public path existence
    if not os.path.exists(static_path):
        os.mkdir(static_path)
        logging.info('Static path does not exist! Move your .md and image files into the static folder and re-run the program')
        full_shutdown()

    if not os.path.exists(public_path):
        logging.info("Creating public path, since it doesn't exist")
        os.mkdir(public_path)
    
    # Copy static/ to public/
    shutil.rmtree(public_path)
    static_copy_to_public()
    logging.info('Succesfully moved tree to public/')

    generate_pages_recursive(template_path, content_path)
    
    logging.info('Finished, shutting down. Running HTTP server on localhost...')
    full_shutdown()

def generate_pages_recursive(template_path: str, current_path='content'):
    path_content = os.listdir(current_path)

    for item in path_content:
        full_from_path = os.path.join(current_path, item)
        full_destination_path = os.path.join('public', os.path.relpath(full_from_path, content_path))
        # if file is a Markdown file generate an HTML in its exact location in public/
        if item.endswith('.md'):
            full_destination_path = full_destination_path.replace('.md', '.html')
            generate_page(full_from_path, full_destination_path, template_path)
        elif os.path.isdir(full_from_path):
            if not os.path.exists(full_destination_path):
                os.makedirs(full_destination_path)
            generate_pages_recursive(template_path, full_from_path)
    
def generate_page(from_path: str, destination_path: str, template_path: str):
    logging.info(f'Generating page for {from_path} using {template_path}, sending to {destination_path}')

    try:
        md = open(from_path, 'r').read()
        template = open(template_path, 'r').read()
    except OSError:
        logging.error('Page generation error! Either the template or source file is missing.')
    
    # get the converted HTML text and get the first h1 from it
    converted_md = markdown_to_html_node(md).to_html()
    page_title = extract_title(md)

    # replace content markers with actual content
    generated_page = template.replace('{{ Title Marker }}', page_title)
    generated_page = generated_page.replace('{{ Content Marker }}', converted_md)

    # make sure all dirs exist and write the file
    try:
        os.makedirs(destination_path[:destination_path.rindex('/')])
    except OSError:
        pass

    open(destination_path, 'w+').write(generated_page)

def static_copy_to_public(current_path=''):
    full_static_path = os.path.join(static_path, current_path)
    full_public_path = os.path.join(public_path, current_path)

    if not os.path.exists(full_public_path):
        os.makedirs(full_public_path)

    tree = os.listdir(full_static_path)

    for item in tree:
        item_static_path = os.path.join(full_static_path, item)
        item_public_path = os.path.join(full_public_path, item)
        
        if os.path.isfile(item_static_path):
            shutil.copy(item_static_path, item_public_path)
            logging.info(f'Copied {item_static_path} to {item_public_path}.')
        else:
            if not os.path.exists(item_public_path):
                os.mkdir(item_public_path)
            static_copy_to_public(os.path.join(current_path, item))

def full_shutdown():
    logging.shutdown()
    sys.exit()

if __name__ == '__main__':
    main()