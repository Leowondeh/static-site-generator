import os, sys, platform, logging, shutil

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

os_type = platform.system()
static_path = 'static'
public_path = 'public'

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
def main():
    logging.info('Static site generator v0.0.1 | https://github.com/Leowondeh/static-site-generator')

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
    
    logging.info('Finished, shutting down. Running HTTP server on localhost...')
    full_shutdown()

def full_shutdown():
    logging.shutdown()
    sys.exit()

if __name__ == '__main__':
    main()