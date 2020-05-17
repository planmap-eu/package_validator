import geopandas
import fiona
import numpy
import pandas
import shapely
from pprint import pprint as pp
from fiona import listlayers


def read(fname, lname):
    import geopandas
    return geopandas.read_file(fname, layer=lname, driver='GKPG')

def check_crs():
    CRSs = dict()
    for ln in listlayers(FiNAME):
        ld = read(FiNAME, ln)
        crs = ld.crs
        # CRS check:
        # - 'layer_styles' (by QGIS) has no 'geometry'
        # - accumulate crs(s) in a hash to check later for heterogeneity (multiple crs's)
        if ln != 'layer_styles':
            lcrs = CRSs.get(crs, [])
            lcrs.append(ln)
            CRSs[crs] = lcrs
        else:
            assert crs is None, "Expecting 'layer_styles' CRS to be `None`, instead got {}".format(crs)
    # Check CRS:
    # - if more than one crs was found, say it
    if len(CRSs) > 1:
        msg = 'WARNING: multiple CRS found in this dataset!'
        fnc = '*' * (len(msg)+2)
        print('{fnc}\n {msg} \n{fnc}'.format(fnc=fnc,msg=msg))
    # For each crs (hopefully, one), print it (WKT)
    for crs,lrs in CRSs.items():
        msg = '\nCRS: {}'.format(lrs)
        print(msg)
        print('---')
        print(crs.to_string())

# Fix geometry (3D -> 2D)
def drop_Z(gdf):
    def _drop_Z(feature):
        return shapely.wkt.loads(feature.to_wkt())

    return geopandas.GeoDataFrame(L, geometry=L.geometry.apply(_drop_Z))

# Print rows with NULLs
def print_nulls(L):
    """
    If 'geometry' has Nulls, clean them out
    """
    if L.isnull().sum().sum():
        print("There are some nulls in table:")
        with pandas.option_context('display.width',160):
            _nils = L.loc[L.isnull().any(axis=1)]
            print("\n{}\n-----".format(_nils))

# Check for all-null columns...
def clean_nulls(L):
    nil_cols = filter(lambda c:all(L[c].isnull()), L.columns)
    for c in nil_cols:
        print('Removing all-none column:',c)
        del L[c]
    if L['geometry'].isnull().any():
        print("Null 'geometry' value(s) found, removing them.")
        L.dropna(subset=['geometry'], inplace=True)
    return L

# Set OBJECTID Index
def set_objectid(L):
    if 'OBJECTID' in L.columns:
        L.set_index('OBJECTID', inplace=True)
    else:
        L.index.name = 'OBJECTID'
    return L

def summary():
    for ln in listlayers(FiNAME):
        # Label
        print('='*_tw)
        print("'{}'".format(ln))
        print('-'*_tw)
        ld = read(FiNAME, ln)
        if len(ld) > n_samples:
            print(ld.sample(n_samples))
        else:
            print(ld)
        print("CRS:",ld.crs.to_string())
        print('-'*_tw)
        print()
