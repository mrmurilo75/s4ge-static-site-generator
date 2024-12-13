from s4ge import utils, app, config


def task_render_md_to_html():
    return {
        "file_dep": [*utils.get_all_files(config.SOURCE_PATH, utils.is_markdown)],
        "targets": [config.Configured["rendered"]],
        "actions": [
            (app.render_md_to_html, (config.SOURCE_PATH, config.Configured["rendered"]))
        ],
    }


def task_render_to_template():
    return {
        "file_dep": [*utils.get_all_files(config.Configured["rendered"])],
        "targets": [config.DESTINATION_PATH],
        "actions": [
            (
                app.render_to_template,
                (config.Configured["rendered"], config.DESTINATION_PATH, "index.html"),
            )
        ],
    }


def task_copy_resources():  # Task 'cp resources'
    return {
        "file_dep": [
            *utils.get_all_files(
                config.Configured["rendered"], lambda s: not utils.is_markdown(s)
            )
        ],
        # "targets": [config.DESTINATION_PATH],  # ERROR: Two different tasks can't have a common target
        "actions": [
            f'rsync -a --checksum --exclude="*.md" --delete {config.SOURCE_PATH}/* {config.DESTINATION_PATH}/'
        ],
    }
