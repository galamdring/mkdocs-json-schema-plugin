import unittest

from mkdocs_json_schema_plugin import markdown


class JsonSchemaTests(unittest.TestCase):
    # def test_plugin_config_defaults(self):
    #     expected = {
    #         'json_schema': ""
    #     }
    #     plugin = jsonschema.JsonSchema()
    #     errors, warnings = plugin.load_config({})
    #     self.assertEqual(plugin.config, expected)
    #     self.assertEqual(errors, [])
    #     self.assertEqual(warnings, [])
    #
    # def test_plugin_config_file(self):
    #     expected = {
    #         'json_schema': "item.schema.json"
    #     }
    #     plugin = jsonschema.JsonSchema()
    #     errors, warnings = plugin.load_config({'json_schema': 'item.schema.json'})
    #     self.assertEqual(plugin.config, expected)
    #     self.assertEqual(errors, [])
    #     self.assertEqual(warnings, [])

    def test_on_page_markdown(self):
        plugin = markdown.markdown_gen()
        plugin.schema_file = 'ebs-standard.json'
        plugin.tag = '~~STANDARDFORMATSCHEMA~~'
        metadata = plugin.get_markdown("~~STANDARDFORMATSCHEMA~~")
        print(metadata)


if __name__ == '__main__':
    unittest.main()

