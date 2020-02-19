# Workflow in terms of the json

{
    "filename": <path-to-geopackage>,
    "type": geopackage,
    tasks: {
        "check-layers": [list-of-layers],
        "check-layer-columns": {
            <layer-name> : [list-of-columns-in-layer-name]
        },
        "check-all-columns": [list-of-columns-in-all-layers],
        "check-nonempty": [list-of-columns-to-assert-nonemty]
    }
}
