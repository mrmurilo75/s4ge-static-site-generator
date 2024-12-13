from config import *
from app import render_md_to_html, render_to_template


def task_render_md_to_html():
    return {
        "actions": [(render_md_to_html, (SOURCE_PATH, Configured["rendered"]))],
    }


def task_render_to_template():
    return {
        "actions": [(render_to_template, (Configured["rendered"], DESTINATION_PATH, "index.html"))],
    }


def task_copy_resources(): # Task 'cp resources'
    return {
        'actions': [f'rsync -a --checksum --exclude="*.md" --delete {SOURCE_PATH}* {DESTINATION_PATH}'],
    }
