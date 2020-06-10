import unittest

from mkdocs_json_schema_plugin import jsonschema


class JsonSchemaTests(unittest.TestCase):
    def test_plugin_config_defaults(self):
        expected = {
            'json_schema': ""
        }
        plugin = jsonschema.JsonSchema()
        errors, warnings = plugin.load_config({})
        self.assertEqual(plugin.config, expected)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_plugin_config_file(self):
        expected = {
            'json_schema': "item.schema.json"
        }
        plugin = jsonschema.JsonSchema()
        errors, warnings = plugin.load_config({'json_schema': 'item.schema.json'})
        self.assertEqual(plugin.config, expected)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])


