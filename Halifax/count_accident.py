import shapely.geometry
import fiona

if __name__ == "__main__":
    # open the halifax district data
    with fiona.open("../Halifax_data/whole_Halifax/whole_Halifax.shp") as district_records:    # source file
        accidents_schema = district_records.schema
        # column for the number of accidents in each district
        accidents_schema["properties"]["ACNUMBER"] = 'int'

        with fiona.open(
                "../Halifax_data/accident_number/accident_number.shp",
                "w",
                crs=district_records.crs,
                driver=district_records.driver,
                schema=accidents_schema,
        ) as dst:  # destination file for save
            # loop through each district in halifax
            for district in district_records:
                number = 0     # the number of accidents happened in current district
                shape = shapely.geometry.shape(district['geometry'])  # the shape of current district

                # open the accident file
                # loop through each conflict to check if it is in the current district
                with fiona.open("../Halifax_data/Traffic_Collisions.geojson") as accidents_records:
                    for accident in accidents_records:
                        point = shapely.geometry.shape(accident['geometry'])
                        if shape.contains(point):
                            number += 1

                district['properties']['ACNUMBER'] = number
                dst.write(district)
