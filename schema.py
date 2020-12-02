planmap = {
    'layers': {
        'geologic_units': {
            'columns': ['name','rgb','geo_type','geo_code'],
            'geometry': 'Polygon'
        },
        'geologic_contacts': {
            'columns': ['geo_type'],
            'geometry': 'Linestring'
        },
        'surface_features': {
            'columns': ['geo_type'],
            'geometry': 'Polygon'
        },
        'linear_features': {
            'columns': ['geo_type'],
            'geometry': 'Linestring'
        },
        'layer_styles': {
            'columns': ['styleQML','styleSLD']
        }
    }
}
