# Scratch

Define a package in terms of a json structure.
```json
{
    "name": "PM_{BODY}_{TYPE}_{TOPONYM}_{SPEC}_{VERSION}",
    "type": "planmap-package",
    "content": {
        "type": "files",
        "meta.json": {
            "type": "json",
            "mandatory": "true",
            "content": {
                # json-schema
            }
        },
        "document": {
            "type": "directory",
            "mandatory": "true",
            "content": {
                # filenames-regex
            }
        },
        "vector": {
            "type": "directory",
            "mandatory": "false",
            "content": {
                "type": "files",
                "*.gpkg": {
                    "type": "geopackage",
                    "mandatory": "true",
                    "content": {
                        "units": {
                            "mandatory": "true",
                            "type": "table",
                            "content": [
                                {
                                    "name": "name",
                                    "type": "string",
                                    "mandatory": "true"
                                },
                                {
                                    "name": "geometry",
                                    "type": "Polygon",
                                    "mandatory": "true"
                                }
                            ]
                        },
                        "contacts": {
                            "mandatory": "true",
                            "type": "table",
                            "content": [
                                {
                                    "name": "geometry",
                                    "type": "Linestring",
                                    "mandatory": "true"
                                }
                            ]
                        }
                    }
                }
                # filenames-regex (e.g., *.gpkg)
            }
        }
    }
}
```
