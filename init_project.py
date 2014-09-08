__author__ = 'Shane Bammel'

import sys, os, random

def _generate_secret_key():
    return ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

def _file_replace_all(file_name, find_string, repl_string):
    file_contents = None

    try:
        # Read the entire file into memory
        with open(file_name, 'r') as in_file:
            file_contents = in_file.read()

        file_contents = file_contents.replace(find_string, repl_string)

        with open(file_name, 'w') as out_file:
            out_file.write(file_contents)
    except Exception:
        print '\tFATAL ERROR: error modifying file %s' % (file_name)
        sys.exit(1)


# RUN CODE
if len(sys.argv) < 2:
    print 'Error: Must provide project name!'
    print 'Usage: python init_project.py [project_name]'
    sys.exit(1)

project_name = sys.argv[1]

print 'Beginning project setup...'

print '\t...generating secret key'
secret_key = _generate_secret_key()

print '\t...injecting secret key'
_file_replace_all('project_name/settings/common.py', '{{ secret_key }}', secret_key)

print '\t...renaming project directory'
os.rename('project_name', project_name)

print '\t...fixing manage.py references'
_file_replace_all('manage.py', '{{ project_name }}', project_name)

print '\t...fixing manage_prod.py references'
_file_replace_all('manage_prod.py', '{{ project_name }}', project_name)

print '\t...fixing wsgi.py references'
_file_replace_all('wsgi.py', '{{ project_name }}', project_name)

print '\t...attempting to add changes to git'
os.system('git add --all')

print 'Project setup complete!'
