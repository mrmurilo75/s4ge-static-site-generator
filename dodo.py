from s4ge import utils, app, config

md_source = utils.get_all_files(config.SOURCE_PATH, utils.is_markdown)
other_source = utils.get_all_files(
    config.SOURCE_PATH, lambda s: not utils.is_markdown(s)
)

md_templated_root = config.INTERMEDIARY_PATH / "md_templated"
md_templated = utils.replicate(
    md_source, target=md_templated_root, relative_to=config.SOURCE_PATH
)

md_to_html_root = config.INTERMEDIARY_PATH / "md_to_html"
md_to_html = list(
    map(
        lambda s: s.with_suffix(".html"),
        utils.replicate(
            md_source, target=md_to_html_root, relative_to=config.SOURCE_PATH
        ),
    )
)


def task_render_md_templates():
    return {
        "file_dep": md_source,
        "targets": md_templated,
        "actions": [app.render_md_templated],
    }


def task_render_md_to_html():
    return {
        "file_dep": md_templated,
        "targets": md_to_html,
        "actions": [app.render_md_to_html],
    }


def task_render_to_template():
    return {
        "file_dep": md_to_html,
        "targets": utils.replicate(
            md_to_html,
            relative_to=md_to_html_root,
            target=config.DESTINATION_PATH,
        ),
        "actions": [(app.render_to_template, (), {"dep_root": md_to_html_root})],
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
            f'rsync -a --checksum --exclude="*.md" {config.SOURCE_PATH}/* {config.DESTINATION_PATH}/'
        ],
    }
