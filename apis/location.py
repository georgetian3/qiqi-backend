import fastapi
from math import sin, cos, radians, asin, sqrt
import requests
import shutil
import numpy as np
from matplotlib import pyplot as plt

        
class LocationApi(fastapi.FastAPI):
    """ Location API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        @self.get('/location')
        async def location():
            return 'location'
        
        @self.get('/bikes-around-me/{lattitude_and_longitude}')
        async def CreateRedZoneMap(my_lat: float, my_long: float):
            #mock data
            activeuser_location = {
                1: {"lat": 40.01256075709379, "long": 116.3517163390383},
                2: {"lat": 40.01256322522058, "long": 116.3518627804347},
                3: {"lat": 40.015106005743235, "long": 116.34531292492439},
                4: {"lat": 40.015106005743235, "long": 116.34555651458665},
                5: {"lat": 40.014810709588076, "long": 116.35134899545217},
                6: {"lat": 40.015162737696514, "long": 116.34559088428011},
                7: {"lat": 40.01249014092127, "long": 116.3517087326486},
                8: {"lat": 40.01134412690182, "long": 116.34358535218374},
                9: {"lat": 40.010148689585584, "long": 116.34284556135756},
                10: {"lat": 40.01019706028805, "long": 116.34304404182312},
                11: {"lat": 40.010563775920374, "long": 116.34812746213488},
                12: {"lat": 40.01049985879172, "long": 116.34824125862033},
                }
            x_long = []
            y_lat = []
            x = []
            y = []
            #get map image of user's location
            map_img = requests.get("https://api.map.baidu.com/staticimage?ak=GjobZyBGoObjhYqt1NyGCD2HAgZVHuzb&center={},{}&markers={},{}&markerStyles=l,A,&width=750&height=750&zoom=16&scale=1&coordtype=gcj02ll&dpiType=ph"
                                   .format(my_long, my_lat, my_long, my_lat), stream=True)
            if map_img.status_code == 200:
                with open("savedmaps/usermap.png",'wb') as f:
                    shutil.copyfileobj(map_img.raw, f)
            else:
                return({"error": "could not fetch map image"})
            #find distance between users, +- 20 meter error value when compared to baidu map's distance calculator
            my_lat_rad = radians(my_lat)
            my_long_rad = radians(my_long)

            for i in activeuser_location:
                their_lat_rad = radians(activeuser_location[i]["lat"])
                their_long_rad = radians(activeuser_location[i]["long"])
            
                distance = 6371 * (2 * asin(sqrt(sin((their_lat_rad - my_lat_rad) / 2)**2 + cos(their_lat_rad) * cos(my_lat_rad) * sin((their_long_rad - my_long_rad) / 2)**2)))
                print(str(distance) + " KM",)
            
                #check if any other users are in a 1100 meter range


                if distance <= 1.1:
                    x_long.append(activeuser_location[i]["long"])
                    y_lat.append(activeuser_location[i]["lat"])

            #convert lat and long to picture pixel coordinates
            for i in range (len(x_long)):
                print
                genesispointLong = my_long - 0.013454430062566303
                genesispointLat = my_lat - 0.010450340579161832
                x.append((x_long[int(i)] - genesispointLong)/0.0000358785)
                print(x_long[int(i)] - genesispointLong)
                y.append((y_lat[int(i)] - genesispointLat)/0.0000278676)
            

            #find red zone
            height = 25
            width = 0
            mapsquareX = []
            mapsquareY = []
            counter = 0
            while height < 751:
                counter = counter + 1
                width = width + 25
                count = 0
                delete_itemX = []
                delete_itemY = []

                #find number of bikes in a certain area of map
                for i in range (len(x)):
                    if x[i] <= width and y[i] <= height and x[i] > width-25 and y[i] > height-25:
                        count = count + 1
                        delete_itemX.append(x[i])
                        delete_itemY.append(y[i])
                # delete bikes which are in a certain area of map after processing them
                if len(delete_itemX) > 0:
                    for i in range(len(delete_itemX)):
                        x.remove(delete_itemX[i])
                        y.remove(delete_itemY[i])

                #if that area in map has more than XXX bikes, save its coordinates
                if count > 20:
                    mapsquareX.extend([width-25,width,width-25,width])
                    mapsquareY.extend([height-25,height-25,height,height])
                
                if width == 750:
                    height = height + 25
                    width = 0

            im = plt.imread("savedmaps/usermap.png")
            fig, ax = plt.subplots()
            im = ax.imshow(im, extent=[0,750,0,750])

            #plot red zones
            squareX = np.array(mapsquareX)
            squareY = np.array(mapsquareY)
            amountofsquares = len(mapsquareX)/4

            for i in range(int(amountofsquares)):
                squarecoordlist = [4*i +1, 4*i + 3, 4*i + 2, 4*i]
                print(list(squareX[squarecoordlist]))
                im = plt.fill("a", "b", "r", alpha=0.3,
                        data={"a": list(squareX[squarecoordlist]),
                            "b": list(squareY[squarecoordlist])})

            plt.savefig("savedmaps/redzoneimage.png", dpi=200)
            plt.show()
            return({"notice": "red zone map generated"})

