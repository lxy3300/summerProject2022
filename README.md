# summerProject2022

### data folder
The data folder contains the original data file and the processed data file.
<br>
<br>
### image folder
The image folder includes drawn maps and graph.
<br>
<br>
### python file
The python files implement different functions, such as processing data and drawing graphs.<br>
##### extract_halifax.py
Use the dataset Census tracts Cartographic Boundary File which is saved in 'data/map_boundary' folder.<br>
Data source：https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/bound-limit-2016-eng.cfm <br>
From this dataset to obtain the data of boundary for the entire Canadian region, from which Halifax data are extracted and save in 'data/whole_halifax' folder.<br>
Draw the map for whole Halifax which is 'image/whole_halifax.png'.<br>
<br>
##### count_accident.py
Use the dataset Traffic collision which is saved in 'data' folder.<br>
Data source: https://catalogue-hrm.opendata.arcgis.com/datasets/e0293fd4721e41d7be4d7386c3c59c16_0/explore?location=44.669039%2C-63.625224%2C12.98 <br>
From this dataset, positions of accidents happened in Halifax are obtained. Count the number of accidents happend in each district in Halifax and save date in 'data/accident_number' folder.<br>
<br>
##### center.py
Based on the statistics, the area with the highest number of accidents is selected as the central point. Areas near the central point are selected and is saved in 'data/halifax_center' folder. Only this part of area will be addressed next.<br>
Draw two maps. One is the map of center of Halifax with centroid on each district which is 'image/map_centroid.png'. Another is the map of it with number of accidents annotated on each district which is 'image/map_number.png'.<br>
<br>
##### rate.py
The average number of accidents per month and per day for each district are both calculated and stored, covering the original file in 'data/halifax_center' folder.<br>
<br>
##### graph.py
Each district is treated as a node and neighbouring regions are connected by edges. Draw the map that each node has rate on it.<br>
The graph with month rate on it is 'image/graph_month.png'. The corresponding map is 'image/map_month.png'. The json data of this graph save in 'data/graph_month.json'.<br>
The graph with day rate on it is 'image/graph_day.png'. The corresponding map is 'image/map_day.png'. The json data of this graph save in 'data/graph_day.json'.




