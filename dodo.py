from config import *

def task_render_site(): # Task 'render_site'
    return {
        'actions': ['python3 app.py'],
    }

def task_copy_resources(): # Task 'cp resources'


    return {
        'actions': [f'rsync -a --checksum --exclude="*.md" --delete {SOURCE_PATH}* {DESTINATION_PATH}'],
    }
