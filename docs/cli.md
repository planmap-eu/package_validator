# Workflow in terms of the command order

```
$ validator --geopackage <path-to-geopackage> \
    --layers <comma-separated-list-of-layers> \
    --columns-all <comma-separated-list-of-columns-in-all-layers> \
    --columns-layers <comma-separated-list-of-layers:columns-key:values> \
    --assert-nonempty <list-of-columns-to-assert-nonempty-records>
```
