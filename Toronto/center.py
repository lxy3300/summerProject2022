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
    index = get_center_point(Toronto)
    center_point = dataframe.iloc[index]['centroid']
    # Calculate the distance from the centroid of other districts to center point
    points_df = gpd.GeoDataFrame({'geometry': dataframe['centroid']}, crs='EPSG:5234')
    dataframe['distance'] = points_df.distance(center_point)
    dataframe['centroid'] = dataframe['centroid'].to_crs('EPSG:4326')
    return dataframe


if __name__ == "__main__":
    path_to_Toronto = '../Toronto_data/accident_number/accident_number.shp'
    Toronto = read_file(path_to_Toronto)
    # change crs to calculate centroid for each district
    Toronto_proj = Toronto.to_crs('epsg:4087')
    Toronto_proj['centroid'] = Toronto_proj['geometry'].centroid.to_crs('EPSG:4326')
    Toronto = Toronto_proj.to_crs('EPSG:4326')
    # get the distance
    Toronto = get_distance(Toronto)
    # extract center area of halifax
    Toronto_center = Toronto[Toronto['distance'] <= 10000]

    # draw the map with centroid
    Toronto_centroid = Toronto_center.copy()
    ax = Toronto_centroid.plot(
        column='ACNUMBER', cmap='Blues',
        linewidth=0.5, edgecolor='0.5')
    Toronto_centroid['geometry'] = Toronto_centroid['centroid']
    Toronto_centroid.plot(ax=ax, color="black", markersize=0.2)
    plt.savefig("../Toronto_image/map_centroid.png", dpi=600)

    # draw the map with number
    Toronto_center.plot(
        column='ACNUMBER', cmap='Blues',
        linewidth=0.2, edgecolor='0.5')
    for index, row in Toronto_center.iterrows():
        xy = row['centroid'].coords[:]
        plt.annotate(
            row['ACNUMBER'], xy=xy[0],
            ha='center', va='center',
            size=3)
    plt.savefig("../Toronto_image/map_number.png", dpi=600)

    # save file without centroid
    Toronto_center = Toronto_center.drop(columns=['centroid'])
    path_to_center = '../Toronto_data/Toronto_center/Toronto_center.shp'
    save_file(Toronto_center, path_to_center)