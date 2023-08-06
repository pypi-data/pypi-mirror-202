import geopandas as gpd
import pickle
import pkg_resources
import glob
import os

def get_sentinel_paths():
    # Get the directory path for sentinel2 tif files 
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'sentinel2_dataset'))
    sentinel_paths = glob.glob(os.path.join(dir_path, '*.tif'))
    return sentinel_paths
    
def load_lcsamples ():
    # Load land cover samples saved as .geojson file
    filepath = pkg_resources.resource_filename(__name__, 'lc_samples/landcover_samples.geojson')
    data = gpd.read_file(filepath)
    
    return data

def load_trainedlc_rf():
    # Load the trained random forest model
    filepath = pkg_resources.resource_filename(__name__, 'trained_models/rf_classification_model.sav')
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    
    return model

def load_trained_pca():
    # Load the trained PCA model
    filepath = pkg_resources.resource_filename(__name__, 'trained_models/pca_decomposition_model.sav')
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    
    return model


    
    
 
