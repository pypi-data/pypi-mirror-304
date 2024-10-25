import os
import math
from math import radians, sin, cos, sqrt, atan2
import numpy as np
import pandas as pd
from pyproj import Geod, Transformer, CRS
import geopandas as gpd
import rasterio
from rasterio.merge import merge
from rasterio.warp import transform_bounds
from rasterio.mask import mask
from shapely.geometry import Polygon, box, shape
from shapely.errors import GEOSException, ShapelyError
from fiona.crs import from_epsg
import gzip
import json
from rtree import index
from collections import Counter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import warnings
from typing import List, Dict
import reverse_geocoder as rg
import pycountry

warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)

def tile_from_lat_lon(lat, lon, level_of_detail):
    sin_lat = math.sin(lat * math.pi / 180)
    x = (lon + 180) / 360
    y = 0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)
    map_size = 256 << level_of_detail
    tile_x = int(x * map_size / 256)
    tile_y = int(y * map_size / 256)
    return tile_x, tile_y

def quadkey_to_tile(quadkey):
    tile_x = tile_y = 0
    level_of_detail = len(quadkey)
    for i in range(level_of_detail):
        bit = level_of_detail - i - 1
        mask = 1 << bit
        if quadkey[i] == '1':
            tile_x |= mask
        elif quadkey[i] == '2':
            tile_y |= mask
        elif quadkey[i] == '3':
            tile_x |= mask
            tile_y |= mask
    return tile_x, tile_y, level_of_detail

# def swap_coordinates(features):
#     for feature in features:
#         if feature['geometry']['type'] == 'Polygon':
#             new_coords = []
#             for polygon in feature['geometry']['coordinates']:
#                 new_coords.append([[lat, lon] for lon, lat in polygon])
#             feature['geometry']['coordinates'] = new_coords
#         elif feature['geometry']['type'] == 'MultiPolygon':
#             new_coords = []
#             for multipolygon in feature['geometry']['coordinates']:
#                 new_multipolygon = []
#                 for polygon in multipolygon:
#                     new_multipolygon.append([[lat, lon] for lon, lat in polygon])
#                 new_coords.append(new_multipolygon)
#             feature['geometry']['coordinates'] = new_coords

def swap_coordinates(features):
    for feature in features:
        if feature['geometry']['type'] == 'Polygon':
            new_coords = [[[lat, lon] for lon, lat in polygon] for polygon in feature['geometry']['coordinates']]
            feature['geometry']['coordinates'] = new_coords
        elif feature['geometry']['type'] == 'MultiPolygon':
            new_coords = [[[[lat, lon] for lon, lat in polygon] for polygon in multipolygon] for multipolygon in feature['geometry']['coordinates']]
            feature['geometry']['coordinates'] = new_coords

def initialize_geod():
    return Geod(ellps='WGS84')

def calculate_distance(geod, lon1, lat1, lon2, lat2):
    _, _, dist = geod.inv(lon1, lat1, lon2, lat2)
    return dist

def normalize_to_one_meter(vector, distance_in_meters):
    return vector * (1 / distance_in_meters)

def setup_transformer(from_crs, to_crs):
    return Transformer.from_crs(from_crs, to_crs, always_xy=True)

def transform_coords(transformer, lon, lat):
    try:
        x, y = transformer.transform(lon, lat)
        if np.isinf(x) or np.isinf(y):
            print(f"Transformation resulted in inf values for coordinates: {lon}, {lat}")
        return x, y
    except Exception as e:
        print(f"Error transforming coordinates {lon}, {lat}: {e}")
        return None, None

def create_polygon(vertices):
    flipped_vertices = [(lon, lat) for lat, lon in vertices]
    return Polygon(flipped_vertices)

def create_geodataframe(polygon, crs=4326):
    return gpd.GeoDataFrame({'geometry': [polygon]}, crs=from_epsg(crs))

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def get_raster_bbox(raster_path):
    with rasterio.open(raster_path) as src:
        bounds = src.bounds
    return box(bounds.left, bounds.bottom, bounds.right, bounds.top)

def raster_intersects_polygon(raster_path, polygon):
    with rasterio.open(raster_path) as src:
        bounds = src.bounds
        if src.crs.to_epsg() != 4326:
            bounds = transform_bounds(src.crs, 'EPSG:4326', *bounds)
        raster_bbox = box(*bounds)
        intersects = raster_bbox.intersects(polygon) or polygon.intersects(raster_bbox)
        # print(f"Raster bounds: {bounds}")
        # print(f"Polygon bounds: {polygon.bounds}")
        # print(f"Intersects: {intersects}")
        return intersects

def save_raster(input_path, output_path):
    import shutil
    shutil.copy(input_path, output_path)
    print(f"Copied original file to: {output_path}")

def merge_geotiffs(geotiff_files, output_dir):
    if not geotiff_files:
        # print("No files intersected with the polygon.")
        return

    src_files_to_mosaic = [rasterio.open(file) for file in geotiff_files if os.path.exists(file)]

    if src_files_to_mosaic:
        try:
            mosaic, out_trans = merge(src_files_to_mosaic)

            out_meta = src_files_to_mosaic[0].meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": mosaic.shape[1],
                "width": mosaic.shape[2],
                "transform": out_trans
            })

            merged_path = os.path.join(output_dir, "lulc.tif")
            with rasterio.open(merged_path, "w", **out_meta) as dest:
                dest.write(mosaic)

            print(f"Merged output saved to: {merged_path}")
        except Exception as e:
            print(f"Error merging files: {e}")
    else:
        print("No valid files to merge.")

    for src in src_files_to_mosaic:
        src.close()

def convert_format_lat_lon(input_coords):
    # Convert input to the desired output format
    output_coords = [[coord[1], coord[0]] for coord in input_coords]

    # Add the first point to the end to close the polygon
    output_coords.append(output_coords[0])

    return output_coords

def get_coordinates_from_cityname(place_name):
    # Initialize the geocoder
    geolocator = Nominatim(user_agent="my_geocoding_script")
    
    try:
        # Attempt to geocode the place name
        location = geolocator.geocode(place_name)
        
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except (GeocoderTimedOut, GeocoderServiceError):
        print(f"Error: Geocoding service timed out or encountered an error for {place_name}")
        return None

# # Sampling and Classification Functions
# def sample_geotiff(geotiff_path, transformed_coords):
#     with rasterio.open(geotiff_path) as src:
#         sampled_values = np.array(list(src.sample(transformed_coords.reshape(-1, 2))))
#     return sampled_values.reshape(transformed_coords.shape[:-1] + (3,))

# def get_land_cover_class(rgb, land_cover_classes):
#     return land_cover_classes.get(tuple(rgb), 'Unknown')

# def find_full_class_name(partial_name, land_cover_classes):
#     for full_name in land_cover_classes.values():
#         if partial_name.lower() == full_name.lower()[:len(partial_name)]:
#             return full_name
#     return 'Unknown'

# def get_dominant_class(cell_values, land_cover_classes):
#     unique, counts = np.unique(cell_values.reshape(-1, 3), axis=0, return_counts=True)
#     dominant_rgb = unique[np.argmax(counts)]
#     class_name = get_land_cover_class(dominant_rgb, land_cover_classes)
#     # if class_name == 'Unknown':
#     #     print(f"Unknown RGB value: {dominant_rgb}")
#     return class_name

# def calculate_dominant_classes(sampled_values, land_cover_classes):
#     return np.apply_along_axis(lambda x: get_dominant_class(x, land_cover_classes), axis=2, arr=sampled_values)

# def create_grid(dominant_classes, land_cover_classes):
#     class_to_index = {cls: idx for idx, cls in enumerate(land_cover_classes.values())}
#     return np.array([[class_to_index[find_full_class_name(cls, land_cover_classes)] for cls in row] for row in dominant_classes])

def rgb_distance(color1, color2):
    return np.sqrt(np.sum((np.array(color1) - np.array(color2))**2))  
      
def get_nearest_class(pixel, land_cover_classes):
    distances = {class_name: rgb_distance(pixel, color) 
                 for color, class_name in land_cover_classes.items()}
    return min(distances, key=distances.get)

def get_dominant_class(cell_data, land_cover_classes):
    if cell_data.size == 0:
        return 'No Data'
    pixel_classes = [get_nearest_class(tuple(pixel), land_cover_classes) 
                     for pixel in cell_data.reshape(-1, 3)]
    class_counts = Counter(pixel_classes)
    return class_counts.most_common(1)[0][0]

def convert_land_cover_array(input_array, land_cover_classes):
    # Create a mapping of class names to integers
    class_to_int = {name: i for i, name in enumerate(land_cover_classes.values())}

    # Create a vectorized function to map string values to integers
    vectorized_map = np.vectorize(lambda x: class_to_int.get(x, -1))

    # Apply the mapping to the input array
    output_array = vectorized_map(input_array)

    return output_array

def validate_polygon_coordinates(geometry):
    if geometry['type'] == 'Polygon':
        for ring in geometry['coordinates']:
            if ring[0] != ring[-1]:
                ring.append(ring[0])  # Close the ring
            if len(ring) < 4:
                return False
        return True
    elif geometry['type'] == 'MultiPolygon':
        for polygon in geometry['coordinates']:
            for ring in polygon:
                if ring[0] != ring[-1]:
                    ring.append(ring[0])  # Close the ring
                if len(ring) < 4:
                    return False
        return True
    else:
        return False

# def filter_buildings(geojson_data, plotting_box):
#     return [feature for feature in geojson_data if plotting_box.intersects(shape(feature['geometry']))]
def filter_buildings(geojson_data, plotting_box):
    filtered_features = []
    for feature in geojson_data:
        if not validate_polygon_coordinates(feature['geometry']):
            print("Skipping feature with invalid geometry")
            print(feature['geometry'])
            continue
        try:
            geom = shape(feature['geometry'])
            if not geom.is_valid:
                print("Skipping invalid geometry")
                print(geom)
                continue
            if plotting_box.intersects(geom):
                filtered_features.append(feature)
        except ShapelyError as e:
            print(f"Skipping feature due to geometry error: {e}")
    return filtered_features

def create_building_polygons(filtered_buildings):
    building_polygons = []
    idx = index.Index()
    count = 0
    for i, building in enumerate(filtered_buildings):
        polygon = Polygon(building['geometry']['coordinates'][0])
        height = building['properties']['height']
        if (height <= 0) or (height == None):
            # print("A building with a height of 0 meters was found. A height of 10 meters was set instead.")
            count += 1
            height = 10
        building_polygons.append((polygon, height))
        idx.insert(i, polygon.bounds)
    
    # print(f"{count} of the total {len(filtered_buildings)} buildings did not have height data. A height of 10 meters was set instead.")
    return building_polygons, idx

# GeoJSON and Data Loading Functions
# def load_geojsons_from_multiple_gz(file_paths):
#     geojson_objects = []
#     for gz_file_path in file_paths:
#         with gzip.open(gz_file_path, 'rt', encoding='utf-8') as file:
#             for line in file:
#                 try:
#                     data = json.loads(line)
#                     geojson_objects.append(data)
#                 except json.JSONDecodeError as e:
#                     print(f"Skipping line in {gz_file_path} due to JSONDecodeError: {e}")
#     return geojson_objects

def load_geojsons_from_multiple_gz(file_paths):
    geojson_objects = []
    for gz_file_path in file_paths:
        with gzip.open(gz_file_path, 'rt', encoding='utf-8') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    # Check and set default height if necessary
                    if 'properties' in data and 'height' in data['properties']:
                        if data['properties']['height'] is None:
                            # print("No building height data was found. A height of 10 meters was set instead.")
                            data['properties']['height'] = 0
                    else:
                        # If 'height' property doesn't exist, add it with default value
                        if 'properties' not in data:
                            data['properties'] = {}
                        # print("No building height data was found. A height of 10 meters was set instead.")
                        data['properties']['height'] = 0
                    geojson_objects.append(data)
                except json.JSONDecodeError as e:
                    print(f"Skipping line in {gz_file_path} due to JSONDecodeError: {e}")
    return geojson_objects

def extract_building_heights_from_geotiff(geotiff_path, geojson_data):
    # Check if geojson_data is a string, if so, parse it
    if isinstance(geojson_data, str):
        geojson = json.loads(geojson_data)
        input_was_string = True
    else:
        geojson = geojson_data
        input_was_string = False

    count_0 = 0
    count_1 = 0
    count_2 = 0

    # Open the GeoTIFF file and keep it open for the entire process
    with rasterio.open(geotiff_path) as src:
        # print("Raster CRS:", src.crs)
        # print("Raster Bounds:", src.bounds)
        # print("Raster Affine Transform:", src.transform)

        # Create a transformer for coordinate conversion
        transformer = Transformer.from_crs(CRS.from_epsg(4326), src.crs, always_xy=True)

        # Process each feature in the GeoJSON
        for feature in geojson:
            if (feature['geometry']['type'] == 'Polygon') & (feature['properties']['height']<=0):
                count_0 += 1
                # Transform coordinates from (lat, lon) to the raster's CRS
                coords = feature['geometry']['coordinates'][0]
                transformed_coords = [transformer.transform(lon, lat) for lat, lon in coords]
                
                # Create a shapely polygon from the transformed coordinates
                polygon = shape({"type": "Polygon", "coordinates": [transformed_coords]})
                
                try:
                    # Mask the raster data with the polygon
                    masked, mask_transform = mask(src, [polygon], crop=True, all_touched=True)
                    
                    # Extract valid height values
                    heights = masked[0][masked[0] != src.nodata]
                    
                    # Calculate average height if we have valid samples
                    if len(heights) > 0:
                        count_1 += 1
                        avg_height = np.mean(heights)
                        feature['properties']['height'] = float(avg_height)
                    else:
                        count_2 += 1
                        feature['properties']['height'] = 10
                        print(f"No valid height data for feature: {feature['properties']}")
                except ValueError as e:
                    print(f"Error processing feature: {feature['properties']}. Error: {str(e)}")
                    feature['properties']['extracted_height'] = None

    if count_0 > 0:
        print(f"{count_0} of the total {len(geojson_data)} building footprint from OSM did not have height data.")
        print(f"For {count_1} of these building footprints without height, values from Open Building 2.5D Temporal were assigned.")
        print(f"For {count_2} of these building footprints without height, no data exist in Open Building 2.5D Temporal. Height values of 10m were set instead")

    # Return the result in the same format as the input
    if input_was_string:
        return json.dumps(geojson, indent=2)
    else:
        return geojson

def extract_building_heights_from_geojson(geojson_data_0: List[Dict], geojson_data_1: List[Dict]) -> List[Dict]:
    # Convert geojson_data_1 to Shapely polygons with height information
    reference_buildings = []
    for feature in geojson_data_1:
        geom = shape(feature['geometry'])
        height = feature['properties']['height']
        reference_buildings.append((geom, height))

    count_0 = 0
    count_1 = 0
    count_2 = 0
    # Process geojson_data_0 and update heights where necessary
    updated_geojson_data_0 = []
    for feature in geojson_data_0:
        geom = shape(feature['geometry'])
        height = feature['properties']['height']
        if height == 0:     
            count_0 += 1       
            # Find overlapping buildings in geojson_data_1
            overlapping_heights = []
            for ref_geom, ref_height in reference_buildings:
                try:
                    if geom.intersects(ref_geom):
                        overlap_area = geom.intersection(ref_geom).area
                        if overlap_area / geom.area > 0.3:  # More than 50% overlap
                            overlapping_heights.append(ref_height)
                except GEOSException as e:
                    print(f"GEOS error at a building polygon {ref_geom}")
                    # Attempt to fix the polygon
                    try:
                        fixed_ref_geom = ref_geom.buffer(0)
                        if geom.intersects(fixed_ref_geom):
                            overlap_area = geom.intersection(ref_geom).area
                            if overlap_area / geom.area > 0.3:  # More than 50% overlap
                                overlapping_heights.append(ref_height)
                                break
                    except Exception as fix_error:
                        print(f"Failed to fix polygon")
                    continue
            
            # Update height if overlapping buildings found
            if overlapping_heights:
                count_1 += 1
                new_height = max(overlapping_heights)
                feature['properties']['height'] = new_height
            else:
                count_2 += 1
                feature['properties']['height'] = 10
        
        updated_geojson_data_0.append(feature)
    
    if count_0 > 0:
        print(f"{count_0} of the total {len(geojson_data_0)} building footprint from OSM did not have height data.")
        print(f"For {count_1} of these building footprints without height, values from Microsoft Building Footprints were assigned.")
        print(f"For {count_2} of these building footprints without height, no data exist in Microsoft Building Footprints. Height values of 10m were set instead")

    return updated_geojson_data_0

def get_country_name(lat, lon):
    # Perform reverse geocoding
    results = rg.search((lat, lon))

    # Extract the country code
    country_code = results[0]['cc']

    # Get the country name from the country code
    country = pycountry.countries.get(alpha_2=country_code)

    if country:
        return country.name
    else:
        return None

def filter_and_convert_gdf_to_geojson(gdf, rectangle_vertices):

    # Reproject to WGS84 if necessary
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs(epsg=4326)

    # Downcast 'height' to save memory
    gdf['height'] = pd.to_numeric(gdf['height'], downcast='float')

    # Add 'confidence' column
    gdf['confidence'] = -1.0

    # Define rectangle polygon
    # rectangle_vertices = [
    #     (56.168518, 14.85961),
    #     (56.172627, 14.85961),
    #     (56.172627, 14.866734),
    #     (56.168518, 14.866734)
    # ]
    rectangle_vertices_lonlat = [(lon, lat) for lat, lon in rectangle_vertices]
    rectangle_polygon = Polygon(rectangle_vertices_lonlat)

    # Use spatial index to filter geometries
    gdf.sindex  # Ensure spatial index is built
    possible_matches_index = list(gdf.sindex.intersection(rectangle_polygon.bounds))
    possible_matches = gdf.iloc[possible_matches_index]
    precise_matches = possible_matches[possible_matches.intersects(rectangle_polygon)]
    filtered_gdf = precise_matches.copy()

    # Delete intermediate data to save memory
    del gdf, possible_matches, precise_matches

    # Function to swap coordinates
    def swap_coordinates(coords):
        if isinstance(coords[0][0], (float, int)):
            return [[lat, lon] for lon, lat in coords]
        else:
            return [swap_coordinates(ring) for ring in coords]

    # Create GeoJSON features
    features = []
    for idx, row in filtered_gdf.iterrows():
        geom = row['geometry'].__geo_interface__
        properties = {
            'height': row['height'],
            'confidence': row['confidence']
        }

        if geom['type'] == 'MultiPolygon':
            for polygon_coords in geom['coordinates']:
                single_geom = {
                    'type': 'Polygon',
                    'coordinates': swap_coordinates(polygon_coords)
                }
                feature = {
                    'type': 'Feature',
                    'properties': properties,
                    'geometry': single_geom
                }
                features.append(feature)
        elif geom['type'] == 'Polygon':
            geom['coordinates'] = swap_coordinates(geom['coordinates'])
            feature = {
                'type': 'Feature',
                'properties': properties,
                'geometry': geom
            }
            features.append(feature)
        else:
            pass  # Handle other geometry types if necessary

    # Create a FeatureCollection
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    # # Write the GeoJSON data to a file
    # with open('output.geojson', 'w') as f:
    #     json.dump(geojson, f)

    # Clean up
    del filtered_gdf, features

    # print("Script execution completed.")
    return geojson["features"]