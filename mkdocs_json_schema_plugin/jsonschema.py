import json

from mkdocs import plugins, config


class JsonSchema(plugins.BasePlugin):
    config_scheme = (
        ('json_schema', config.config_options.Type(str, default='')),
    )

    def __init__(self):
        super().__init__()

    def safe_get_value(self, data, key):
        if data is None:
            return None, False
        try:
            output = data[key]
            return output, True
        except KeyError:
            return None, False

    def on_page_markdown(self, markdown, **kwargs):
        # we can assume the file was set, or it throws a validation error

        if "#JsonSchema#" in markdown:
            file = self.config['json_schema']
            with open(file) as json_file:
                data = json.load(json_file)

            new_markdown = self.markdown_for_items(data, "\t")
            index = markdown.find("#JsonSchema#")
            if index == -1:
                return
            before = markdown[0:index]
            after = markdown[index+12:-1]
            markdown = before + new_markdown + after
            print(markdown)
            return markdown

    def markdown_for_items(self, items, indent):
#        if items["type"] == "array":
#            new_markdown += self.markdown_for_item(items["items"]["required"], items["items"], "items", new_markdown, indent)
#        else:
        new_markdown = ""
        new_markdown += '{indent}???+ jssobject "{description}"\n'.format(indent=indent,
                                                                          description=items["description"])
        props, has_props = self.safe_get_value(items, "properties")
        if has_props:
            for name, item in props.items():
                new_markdown += self.markdown_for_item(items["required"], item, name, indent+"\t")
        return new_markdown

    def markdown_for_item(self, required, item, name, indent):
        new_markdown = ""
        new_markdown += self.markdown_string_for_item(item, name, required, indent)

        sub_required, has_required = self.safe_get_value(item, "required")
        props, has_props = self.safe_get_value(item, "properties")
        items, has_items = self.safe_get_value(item, "items")
        items_props, has_item_props = self.safe_get_value(items, "properties")
        if sub_required is None:
            sub_required = []

        if has_props:
            for sub_name, sub_item in props.items():
                new_markdown += self.markdown_for_item(sub_required, sub_item, sub_name, indent+"\t")
        if has_items and has_item_props:
            new_markdown += self.markdown_for_items(items, indent+"\t")
        if has_items and not has_item_props:
            new_markdown += self.markdown_for_item([], items, "items", indent+"\t")
        return new_markdown

    def markdown_string_for_item(self, item, name, required, indent):
        my_string = ""
        item_type = item["type"]
        format_data, has_format = self.safe_get_value(item, "format")
        nullable, has_nullable = self.safe_get_value(item, "nullable")

        enum, has_enum = self.safe_get_value(item, "enum")

        if item_type == "array":
            my_string += '{indent}??? jssarray'.format(indent=indent)
        else:
            my_string += '{indent}??? jssprop'.format(indent=indent)

        my_string += ' ""{name}" ({type}'.format(indent=indent, name=name, type=item_type)
        if has_format:
            my_string += ':{}'.format(format_data)

        my_string += ')"\n{indent}\t{description}\n{indent}\t```\n{indent}\tType: {type}\n{indent}\t' \
                        'Required: {req}\n'.format(indent=indent,
                                                   type=item_type,
                                                   req=name in required,
                                                   description=item['description'])
        if has_format:
            my_string += '{indent}\tFormat: {format}\n'.format(format=format_data, indent=indent)
        if has_nullable:
            my_string += '{indent}\tNullable: {nullable}\n'.format(nullable=nullable, indent=indent)
        if has_enum:
            my_string += '{indent}\tValid Values:\n'.format(indent=indent)
            for enum_item in enum:
                my_string += '{indent}\t\t"{item}"\n'.format(item=enum_item, indent=indent)
        my_string += '{}\t```\n'.format(indent)
        return my_string
