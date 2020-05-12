# MkDocs Json Schema Plugin

MkDocs Plugin to parse json schema files.

To use this plugin, install it with pip in the same environment as MkDocs:

```
pip install MkDocsJsonSchemaPlugin
```

Then add the following entry to the MkDocs config file:

```yml
plugins:
  - json-schema:
      json_schema: "docs/item.schema.json"
```

In your target file, add a tag to be replaced
```
#JsonSchema#
```
