import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

class Mapa():

    def __init__(self):

        self.fig = plt.figure(figsize=(15, 10))
        self.ax = self.fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude=0))

        self.ax.set_extent((-80, -30, -40, 15))
        self.ax.coastlines()

        # Fonte: https://gis.stackexchange.com/questions/88209/python-mapping-in-matplotlib-cartopy-color-one-country
        shpfilename = shpreader.natural_earth(resolution='110m',
                                            category='cultural',
                                            name='admin_0_countries')

        reader = shpreader.Reader(shpfilename)
        countries = reader.records()

        for country in countries:
            if country.attributes['NAME_EN'] == 'Brazil':
                self.ax.add_geometries([country.geometry], ccrs.PlateCarree(),
                                facecolor='#C8D5B9',
                                label=country.attributes['NAME_EN'])

        self.ax.add_feature(cfeature.BORDERS)
        self.ax.add_feature(cfeature.OCEAN)
