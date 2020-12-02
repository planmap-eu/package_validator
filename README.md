# PLANMAP package validator

This tool validates the structure and content of a Planmap package.

The validator gets as input the path to a (PM) package and then
run a series of checks following a package/data model.

## To run the validator

Since I'm trying different methods to have this validator steps running together, there are different ways to run _a_ validator.

* Pytest:

    ```bash
    $ pytest --pkgpath 'path/to/geopackage.gpkg'
    ```
    
* Custom (python pipeline):

    ```bash
    $ python validate.py <path>
    ```

## Where are the models

## How to modify the models
