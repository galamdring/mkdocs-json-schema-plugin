import json

from mkdocs import plugins, config


class JsonSchema(plugins.BasePlugin):
    config_scheme = (
        ('json_schema', config.config_options.Type(str, default='')),
    )

    def __init__(self):
        super().__init__()

    def safe_get_value(self, data, key):
        try:
            output = data[key]
            return output, True
        except KeyError:
            return None, False

    def on_page_markdown(self, markdown, **kwargs):
        # we can assume the file was set, or it throws a validation error
        file = self.config['json_schema']
        new_markdown = ""
        with open(file) as json_file:
            data = json.load(json_file)
            if data["type"] == "object":
                new_markdown += '???+ jssobject "' + data["description"] + '"\n'
            for name, item in data["properties"].items():
                format_data, has_format = self.safe_get_value(item, "format")
                enum, has_enum = self.safe_get_value(item, "enum")

                new_markdown += '\t??? jssprop ""{name}" ({type}'.format(name=name, type=item["type"])
                if has_format:
                    new_markdown += ':{}'.format(format_data)
                new_markdown += ')"\n\t\t{description}\n\t\t```\n\t\tType: {type}\n\t\t'\
                                'Required: {req}\n'.format(type=item["type"],
                                                               req=name in data["required"],
                                                               description=item['description'])
                if has_format:
                    new_markdown += '\t\tFormat: {}\n'.format(format_data)

                if has_enum:
                    new_markdown += '\t\tValid Values:\n'
                    for enum_item in enum:
                        new_markdown += '\t\t\t"'+enum_item+'"\n'

                new_markdown += '\t\t```\n'

        if "#JsonSchema#" in markdown:
            index = markdown.find("#JsonSchema#")
            if index == -1:
                return
            before = markdown[0:index]
            after = markdown[index+12:-1]
            markdown = before + new_markdown + after
            print(markdown)
            return markdown
