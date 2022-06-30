import geopandas as gpd
import matplotlib.pyplot as plt


def read_file(path):
    data = gpd.read_file(path)
    return data


def save_file(data, path):
    data.to_file(path)


def get_center_point(dataframe):
    max = dataframe.iloc[0]['ACNUMBER']
    idx = 0
    for index, row in dataframe.iterrows():
        if max < row['ACNUMBER']:
            max = row['ACNUMBER']
            idx = index
    return idx


def get_distance(dataframe):
    dataframe['centroid'] = dataframe['centroid'].to_crs('EPSG:5234')
    # choose the district has most accidents as the center point
    index = get_center_point(halifax)
    center_point = dataframe.iloc[index]['centroid']
    # Calculate the distance from the centroid of other districts to center point
    points_df = gpd.GeoDataFrame({'geometry': dataframe['centroid']}, crs='EPSG:5234')
    dataframe['distance'] = points_df.distance(center_point)
    dataframe['centroid'] = dataframe['centroid'].to_crs('EPSG:4326')
    return dataframe


if __name__ == "__main__":
    path_to_halifax = 'data/accident_number/accident_number.shp'
    halifax = read_file(path_to_halifax)
    # change crs to calculate centroid for each district
    halifax_proj = halifax.to_crs('epsg:4087')
    halifax_proj['centroid'] = halifax_proj['geometry'].centroid.to_crs('EPSG:4326')
    halifax = halifax_proj.to_crs('EPSG:4326')
    # get the distance
    halifax = get_distance(halifax)
    # extract center area of halifax
    halifax_center = halifax[halifax['distance'] <= 10000]

    # draw the map with centroid
    halifax_centroid = halifax_center.copy()
    ax = halifax_centroid.plot(
        column='ACNUMBER', cmap='Blues',
        linewidth=0.5, edgecolor='0.5')
    halifax_centroid['geometry'] = halifax_centroid['centroid']
    halifax_centroid.plot(ax=ax, color="black", markersize=0.2)
    plt.savefig("image/map_centroid.png", dpi=600)

    # draw the map with number
    halifax_center.plot(
        column='ACNUMBER', cmap='Blues',
        linewidth=0.2, edgecolor='0.5')
    for index, row in halifax_center.iterrows():
        xy = row['centroid'].coords[:]
        plt.annotate(
            row['ACNUMBER'], xy=xy[0],
            ha='center', va='center',
            size=3)
    plt.savefig("image/map_number.png", dpi=600)

    # save file without centroid
    halifax_center = halifax_center.drop(columns=['centroid'])
    path_to_center = 'data/halifax_center/halifax_center.shp'
    save_file(halifax_center, path_to_center)