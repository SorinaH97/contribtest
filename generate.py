import os
import logging
import jinja2
import sys
import json

log = logging.getLogger(__name__)

#checks all files in the folder_path and yields all .rst files
def list_files(folder_path):
    
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)

#Reads the content of file_path and extract the data
#Content starts where metadata ends (with '---')
def read_file(file_path):
    
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line
    return json.loads(raw_metadata), content

#Write the output in test folder
def write_output(name, html):
    with open(os.path.join('test', name+'.html'), 'w') as f:
        f.write(html)

def generate_site(input_folder):
    # generates the site from the layout of the page by creating a jinga environment
    log.info("Generating site from %r", input_folder)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(input_folder + '/layout'))

    for file_path in list_files(input_folder):
        #for every file in the input_folder, we extract the metadata and content
        metadata, content = read_file(file_path)
        
        #extract and load the template
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        
        #render the date using the template
        data = dict(metadata, content=content)
        html = template.render(data)

        #create the .html file
        name = os.path.splitext(os.path.basename(file_path))[0]
        write_output(name, html)
        log.info("Writing %r with template %r", name, template_name)


def main():
    generate_site(sys.argv[1])


if __name__ == '__main__':
    logging.basicConfig() 
    main()
