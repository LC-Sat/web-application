# =============================================================================
# Imports
# =============================================================================


import folium
import os
import json


# =============================================================================
# Scripts
# =============================================================================


class Map:


	def __init__(self, debug, tiles_file):

		self.debug = debug

		with open(tiles_file, 'r', encoding = "utf-8") as file:

			self.tiles = json.load(file)
			file.close()

		return


	def __str__(self):

		return "Map class"


	def reload(self, debug, tiles_file):

		self.debug = debug

		with open(tiles_file, 'r', encoding = "utf-8") as file:

			self.tiles = json.load(file)
			file.close()

		return



	def create_map(self, latitude, longitude, title, icon, color, zoom_start, map_destination):

		# create map base
		m = folium.Map(location = [latitude[0], longitude[0]], zoom_start = zoom_start, title = title, control_scale=True)

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


		# Add cansat recorded coordonates markers
		for i in range(0, len(latitude) - 1):

			try:

				folium.Marker(
				    location=[latitude[i], longitude[i]],
				    icon = folium.Icon(color=color, icon=icon),
				).add_to(m)

			except Exception as e:

				break

		# Add map tiles

		try:

			for tile in self.tiles["tiles"]:

				folium.TileLayer(str(tile)).add_to(m)

		except Exception as e:

			pass

		folium.LayerControl().add_to(m)

		# Save map and store it to static/result folder
		m.save(os.path.join(map_destination, "map.html"))

		return

		