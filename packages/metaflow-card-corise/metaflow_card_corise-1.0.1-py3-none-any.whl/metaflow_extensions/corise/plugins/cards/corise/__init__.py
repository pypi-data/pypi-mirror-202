import os
import base64
import json
import uuid
from metaflow.cards import MetaflowCard
from metaflow.plugins.cards.card_modules.basic import read_file, PageComponent

ABS_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
RENDER_TEMPLATE_PATH = os.path.join(ABS_DIR_PATH, "base.html")
JS_PATH = os.path.join(ABS_DIR_PATH, "main.js")
CSS_PATH = os.path.join(ABS_DIR_PATH, "bundle.css")

# Copied from metaflow.plugins.cards.card_modules.basic.BlankCard
class CoriseCard(MetaflowCard):

    ALLOW_USER_COMPONENTS = True

    type = "corise"

    def __init__(self, options=dict(title=""), components=[], graph=None):
        self._title = ""
        if "title" in options:
            self._title = options["title"]
        self._components = components

    def render(self, task, components=[]):
        RENDER_TEMPLATE = read_file(RENDER_TEMPLATE_PATH)
        JS_DATA = read_file(JS_PATH)
        CSS_DATA = read_file(CSS_PATH)
        if type(components) != list:
            components = []
        page_component = PageComponent(
            title=self._title,
            contents=components + self._components,
        ).render()
        final_component_dict = dict(
            metadata={
                "pathspec": task.pathspec,
            },
            components=[page_component],
        )
        pt = self._get_mustache()
        data_dict = dict(
            task_data=base64.b64encode(
                json.dumps(final_component_dict).encode("utf-8")
            ).decode("utf-8"),
            javascript=JS_DATA,
            title=task.pathspec,
            css=CSS_DATA,
            card_data_id=uuid.uuid4(),
        )
        return pt.render(RENDER_TEMPLATE, data_dict)

CARDS = [CoriseCard]
