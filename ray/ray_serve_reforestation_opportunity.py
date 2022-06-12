import georasters as gr
import json
import random
from shapely.geometry import Polygon
from shapely.geometry import Point
import pandas as pd
import os
from osgeo import gdal


def bbox(long0, lat0, lat1, long1):
    return Polygon([[long0, lat0], [long1, lat0], [long1, lat1], [long0, lat1]])


def get_point_list(geometry):
    point_list = [Point(geometry.bounds[0], geometry.bounds[1]),
                                 Point(geometry.bounds[0], geometry.bounds[3]),
                                 Point(geometry.bounds[2], geometry.bounds[1]),
                                 Point(geometry.bounds[2], geometry.bounds[3])]
    return point_list


def load_bounding_boxes():
    file = open('bounding_boxes.json')
    boxes = json.load(file)
    return boxes


bounding_boxes = load_bounding_boxes()
keys = list(bounding_boxes.keys())


# def find_sat_image(geometry, stop_flag=False):
#
#     for key in keys:
#         bounding_box = bounding_boxes[key]
#         long0 = float(bounding_box['west'])
#         long1 = float(bounding_box['east'])
#         lat0 = float(bounding_box['south'])
#         lat1 = float(bounding_box['north'])
#         outer_poly = bbox(long0, lat0, lat1, long1)
#         if outer_poly.contains(geometry):
#             return [key]
#
#     # If we've gotten to this point, the geometry is not fully contained within a single sat image
#     key_list = []
#     if not stop_flag:
#         points = get_point_list(geometry)
#         for point in points:
#             key = find_sat_image(point, True)
#             key_list.append(key)
#
#     return key_list


def get_file_list():
    # make list of directories
    file_path_list = []
    tif_locations = []
    dir = r'K:\tiffs'

    for subdir, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            file_path_list.append(file_path)
            tif_locations.append(file_path[18:-3] + 'tif')
    # return tif_locations
    return file_path_list


def find_sat_image(geometry, stop_flag=False):
    path_list = get_file_list()

    for file in path_list:

        sat_image = gdal.Open(file)
        ulx, xres, xskew, uly, yskew, yres = sat_image.GetGeoTransform()
        lrx = ulx + (sat_image.RasterXSize * xres)
        lry = uly + (sat_image.RasterYSize * yres)
        outer_poly = bbox(ulx, lry, uly, lrx)
        if outer_poly.contains(geometry):
            return [file[9:]]

    key_list = []
    if not stop_flag:
        points = get_point_list(geometry)
        for point in points:
            key = find_sat_image(point, True)
            key_list.append(key[9:])

    return key_list




def get_op_selections(target_tif, selections):
    return target_tif.iloc[selections]['geometry']


def read_tif(file_path):
    try:
        wa_chunk_raster = gr.from_file(file_path)
    except:
        print('missing file ' + file_path)
        return None
    wa_chunk_frame = wa_chunk_raster.to_geopandas()
    wa_chunk_frame = wa_chunk_frame.to_crs(26910)
    return wa_chunk_frame


def main():
    tif_list = pd.read_csv('data/100_reforestation_samples.csv', header=None)
    outer_dict = {}
    none_dict = {}

    for tif in tif_list[0]:
        inner_dict = {}
        inner_none_dict = {}
        active_tif = read_tif(os.path.join('data/total_op_split', tif))
        if active_tif is None:
            continue
        selections = random.sample(range(0, active_tif.shape[0]), 100)

        for index in selections:
            dict_to_store = {}
            key = find_sat_image(active_tif.iloc[index]['geometry'])
            dict_to_store['tif'] = tif
            dict_to_store['index'] = index
            dict_to_store['geometry'] = active_tif.iloc[index]['geometry'].bounds
            dict_to_store['value'] = active_tif.iloc[index]['value'].item()
            dict_to_store['key'] = key

            if key is not None:
                inner_dict[tif + '_' + str(index)] = dict_to_store
            else:
                inner_none_dict[tif + '_' + str(index)] = dict_to_store

        if len(inner_none_dict) != 0:
            none_dict[tif] = inner_none_dict
            print('none dict ' + tif + ' done')
        outer_dict[tif] = inner_dict
        print('dict ' + tif + ' done')

    with open('results.json', 'w') as outfile:
        json.dump(outer_dict, outfile)

    with open('none_results.json', 'w') as outfile_none:
        json.dump(none_dict, outfile_none)

    outfile.close()
    outfile_none.close()


main()
