import geopandas as gpd
import matplotlib.pyplot as plt


def read_file(path):
    data = gpd.read_file(path)
    return data


def save_file(data, path):
    data.to_file(path)


if __name__ == "__main__":
    # the boundary file for the whole Canada, the same file that used to extract halifax
    path_to_ca = '../Halifax_data/map_boundary/lct_000b16a_e.shp'
    ca_map = read_file(path_to_ca)
    # re-project to WGS84
    ca_map = ca_map.to_crs("EPSG:4326")
    # extract Toronto data from whole canada
    Toronto = ca_map[ca_map.CMANAME == "Toronto"]
    Toronto = Toronto.drop(columns=['CTUID', 'PRUID', 'PRNAME', 'CMAUID', 'CMAPUID', 'CMANAME', 'CMATYPE'])
    # save Toronto data
    # path need to be created in advance
    path_to_Toronto = '../Toronto_data/whole_Toronto/whole_Toronto.shp'
    save_file(Toronto, path_to_Toronto)
    # draw the map
    Toronto.plot()
    plt.savefig('../Toronto_image/whole_Toronto.png', dpi=600)
    plt.show()
