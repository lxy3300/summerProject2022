import shapely.geometry
import fiona

if __name__ == "__main__":
    # open the halifax district Halifax_data
    with fiona.open("../Toronto_data/whole_Toronto/whole_Toronto.shp") as district_records:    # source file
        accidents_schema = district_records.schema
        # column for the number of accidents in each district
        accidents_schema["properties"]["ACNUMBER"] = 'int'

        with fiona.open(
                "../Toronto_data/accident_number/accident_number.shp",
                "w",
                crs=district_records.crs,
                driver=district_records.driver,
                schema=accidents_schema,
        ) as dst:  # destination file for save
            # put each accident in list
            points = []
            with fiona.open("../Toronto_data/Traffic_Collisions.geojson") as accidents_records:
                for accident in accidents_records:
                    point = shapely.geometry.shape(accident['geometry'])
                    points.append(point)

            for district in district_records:
                shape = shapely.geometry.shape(district['geometry'])  # the shape of current district
                accidents_list = [x for x in points if shape.contains(x)]
                number = len(accidents_list)
                points = [x for x in points if not shape.contains(x)]
                district['properties']['ACNUMBER'] = number
                dst.write(district)
