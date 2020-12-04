from mkdocs import plugins, config
from .markdown import markdown_gen


class JsonSchema(plugins.BasePlugin):

    config_scheme = (
        ('json_schema', config.config_options.Type(str, default='')),
        ('markdown_tag', config.config_options.Type(str, default=''))
    )
    generator = markdown_gen()

    def on_config(self, config):
        self.generator = markdown_gen()
        self.generator.set_config(self.config)

    def __init__(self):
        super().__init__()



    def on_page_markdown(self, markdown, **kwargs):
        return self.generator.get_markdown(markdown, **kwargs)



