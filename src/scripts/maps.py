# =============================================================================
# Imports
# =============================================================================


import folium
import numpy as np
import os


# =============================================================================
# Scripts
# =============================================================================


class Map:


	def __init__(self, debug, tiles_file):

		self.debug = debug

		with open(tiles_file, 'r') as file:

			self.tiles = json.loads(file)
			file.close()


	def __str__(self):

		return "Map class"


	def create_map(self, latitude, longitude, title, icon, color, zoom_start, map_destination):

		m = folium.Map(location = [latitude[0], longitude[0]], zoom_start = zoom_start, title = title)

		if self.debug:

			print("-----------------[MAP]-----------------")
			print(f"MAP | latitude: {str(latitude)}")
			print(f"MAP | longitude: {str(longitude)}")
			print(f"MAP | title: {str(title)}")
			print(f"MAP | icon: {str(icon)}")
			print(f"MAP | color: {str(color)}")
			print(f"MAP | zoom start: {str(zoom_start)}")
			print(f"MAP | map destination: {str(map_destination)}")
			print("---------------[END MAP]---------------\n")

		for tile in tiles["tiles"]:

			folium.TileLayer(str(tile)).add_to(m)

		for i in range(0, len(latitude) - 1):

			folium.Marker(
			    [latitude[i], longitude[i]],
			    popup = "<i>" + str(latitude[i]) + " | " + str(longitude[i]) + "</i>",
			    icon = folium.icon(icon=str(icon), color=str(color))
			).add_to(m)

		m.save(os.path.join(map_destination, "map.html"))

		