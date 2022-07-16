import geopandas as gpd
import matplotlib.pyplot as plt


def read_file(path):
    data = gpd.read_file(path)
    return data


def save_file(data, path):
    data.to_file(path)


if __name__ == "__main__":
    # the boundary file for the whole Canada
    path_to_ca = '../Halifax_data/map_boundary/lct_000b16a_e.shp'
    ca_map = read_file(path_to_ca)
    # re-project to WGS84
    ca_map = ca_map.to_crs("EPSG:4326")
    # extract halifax data from whole canada
    Halifax = ca_map[ca_map.CMANAME == "Halifax"]
    Halifax = Halifax.drop(columns=['CTUID', 'PRUID', 'PRNAME', 'CMAUID', 'CMAPUID', 'CMANAME', 'CMATYPE'])
    # save halifax data
    # path need to be created in advance
    path_to_Halifax = '../Halifax_data/whole_Halifax/whole_Halifax.shp'
    save_file(Halifax, path_to_Halifax)
    # draw the map
    Halifax.plot()
    plt.savefig('../Halifax_image/whole_Halifax.png', dpi=600)
    plt.show()
