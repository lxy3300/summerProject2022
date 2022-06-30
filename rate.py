import geopandas as gpd


def read_file(path):
    data = gpd.read_file(path)
    return data


def save_file(data, path):
    data.to_file(path)


if __name__ == "__main__":
    path_to_center = 'data/halifax_center/halifax_center.shp'
    center = read_file(path_to_center)
    months = 52
    center['rate'] = center['ACNUMBER']/months
    save_file(center, path_to_center)
