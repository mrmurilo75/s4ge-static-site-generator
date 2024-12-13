from s4ge import utils, app, config

md_source = utils.get_all_files(config.SOURCE_PATH, utils.is_markdown)
other_source = utils.get_all_files(
    config.SOURCE_PATH, lambda s: not utils.is_markdown(s)
)

md_rendered = list(
    map(
        lambda s: s.with_suffix(".html"),
        utils.replicate(
            md_source, target=config.INTERMEDIARY_PATH, relative_to=config.SOURCE_PATH
        ),
    )
)


def task_render_md_to_html():
    return {
        "file_dep": md_source,
        "targets": md_rendered,
        "actions": [
            (app.render_md_to_html, (config.SOURCE_PATH, config.INTERMEDIARY_PATH))
        ],
    }


def task_render_to_template():
    return {
        "file_dep": md_rendered,
        "targets": utils.replicate(
            md_rendered,
            relative_to=config.INTERMEDIARY_PATH,
            target=config.DESTINATION_PATH,
        ),
        "actions": [
            (
                app.render_to_template,
                (config.INTERMEDIARY_PATH, config.DESTINATION_PATH, "index.html"),
            )
        ],
    }


def task_copy_resources():  # Task 'cp resources'
    return {
        "file_dep": other_source,
        "targets": utils.replicate(
            other_source,
            relative_to=config.SOURCE_PATH,
            target=config.DESTINATION_PATH,
        ),
        "actions": [
            f'rsync -a --checksum --exclude="*.md" --delete {config.SOURCE_PATH}/* {config.DESTINATION_PATH}/'
        ],
    }
