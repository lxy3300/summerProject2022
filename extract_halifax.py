import geopandas as gpd
import matplotlib.pyplot as plt


def read_file(path):
    data = gpd.read_file(path)
    return data


def save_file(data, path):
    data.to_file(path)


if __name__ == "__main__":
    # the boundary file for the whole Canada
    path_to_ca = 'data/map_boundary/lct_000b16a_e.shp'
    ca_map = read_file(path_to_ca)
    # re-project to WGS84
    ca_map = ca_map.to_crs("EPSG:4326")
    # extract halifax data from whole canada data
    halifax = ca_map[ca_map.CMANAME == "Halifax"]
    halifax = halifax.drop(columns=['CTUID', 'PRUID', 'PRNAME', 'CMAUID', 'CMAPUID', 'CMANAME', 'CMATYPE'])
    # save halifax data
    path_to_halifax = 'data/whole_halifax/whole_halifax.shp'
    save_file(halifax, path_to_halifax)
    # draw the map
    halifax.plot()
    plt.savefig('image/whole_halifax.png', dpi=600)
    plt.show()
