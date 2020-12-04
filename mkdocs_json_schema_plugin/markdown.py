import json

class markdown_gen:
    schema_file = ''
    tag = ''
    indent_val = "    "
    def safe_get_value(self, data, key):
        if data is None:
            return None, False
        try:
            output = data[key]
            return output, True
        except KeyError:
            return None, False

    def get_markdown(self, markdown, **kwargs):
        # we can assume the file was set, or it throws a validation error
        if self.tag in markdown and self.tag != "":
            with open(self.schema_file) as json_file:
                data = json.load(json_file)

            new_markdown = self.markdown_for_items(data, self.indent_val)
            index = markdown.find(self.tag)
            tag_length = len(self.tag)
            after_index = index + tag_length
            if index == -1:
                return
            before = markdown[0:index]
            after = markdown[after_index:-1]
            markdown = before + new_markdown + after
            print(markdown)
            return markdown

    def markdown_for_items(self, items, indent):
        new_markdown = "{indent}???+ jssobject ".format(indent=indent)
        description, has_description = self.safe_get_value(items, "description")
        title, has_title = self.safe_get_value(items, "title")
        if has_description:
            new_markdown += '"{description}"\n\n'.format(description=items["description"])
        elif has_title:
            new_markdown += '"{title}"\n\n'.format(title=items["title"])
        else:
            new_markdown += '""\n\n'
        props, has_props = self.safe_get_value(items, "properties")
        if has_props:
            for name, item in props.items():
                new_markdown += self.markdown_for_item(items["required"], item, name, indent+self.indent_val)
        return new_markdown

    def markdown_for_subitems(self, items, indent):
        new_markdown = ""
        props, has_props = self.safe_get_value(items, "properties")
        if has_props:
            for name, item in props.items():
                new_markdown += self.markdown_for_item(items["required"], item, name, indent)
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
                new_markdown += self.markdown_for_item(sub_required, sub_item, sub_name, indent+self.indent_val)
        if has_items and has_item_props:
            new_markdown += self.markdown_for_subitems(items, indent+self.indent_val)
        if has_items and not has_item_props:
            new_markdown += self.markdown_for_item([], items, "items", indent+self.indent_val)
        return new_markdown

    def markdown_string_for_item(self, item, name, required, indent):
        my_string = ""
        item_type, has_type = self.safe_get_value(item, "type")
        format_data, has_format = self.safe_get_value(item, "format")
        nullable, has_nullable = self.safe_get_value(item, "nullable")

        enum, has_enum = self.safe_get_value(item, "enum")

        if item_type == "array":
            my_string += '{indent}??? jssarray'.format(indent=indent)
        else:
            my_string += '{indent}??? jssprop'.format(indent=indent)

        my_string += ' "{name}'.format(indent=indent, name=name)
        if has_type:
            my_string += '({type}'.format(type=item_type)
            if has_format:
                my_string += ':{}'.format(format_data)

            my_string += ')'

        my_string += '"\n'

        description, has_description = self.safe_get_value(item, "description")
        title, has_title = self.safe_get_value(item, "title")
        if has_description:
            title = description
        elif has_title:
            title = title
        else:
            title = name

        my_string += '{indent}{t}{description}\n{indent}{t}```\n{indent}{t}Type: {type}\n{indent}{t}' \
                        'Required: {req}\n'.format(indent=indent,
                                                   type=item_type,
                                                   req=name in required,
                                                   description=title,
                                                   t=self.indent_val)
        if has_format:
            my_string += '{indent}{t}Format: {format}\n'.format(format=format_data, indent=indent,t=self.indent_val)
        if has_nullable:
            my_string += '{indent}{t}Nullable: {nullable}\n'.format(nullable=nullable, indent=indent, t=self.indent_val)
        if has_enum:
            my_string += '{indent}{t}Valid Values:\n'.format(indent=indent, t=self.indent_val)
            for enum_item in enum:
                my_string += '{indent}{t}{t}"{item}"\n'.format(item=enum_item, indent=indent, t=self.indent_val)
        my_string += '{}{}```\n'.format(indent, self.indent_val)
        return my_string

    def set_config(self, config):
        self.schema_file, _ = self.safe_get_value(config, "json_schema")
        self.tag, _ = self.safe_get_value(config, "markdown_tag")
        print("Got config: File: {file} Tag: {tag}".format(file=self.schema_file, tag=self.tag))
