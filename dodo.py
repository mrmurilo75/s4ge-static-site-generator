def task_render_site(): # Task 'render_site'
    return {
        'actions': ['python3 app.py'],
    }

def task_cp_resources(): # Task 'cp resources'
    source_dir = '_source/'
    destination_dir = '_site/'
    return {
        'actions': [f'rsync -a --exclude="*.md" --delete {source_dir}* {destination_dir}'],
    }
