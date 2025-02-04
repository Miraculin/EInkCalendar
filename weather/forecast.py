class Forecast():
    '''Represents a single forecast containing the data needed for the template to render'''    
    def __init__(self):
        self.temperature = 0
        self.weather = ""
        self.icon = ""

    def set_forecast(self, temperature, weather, icon):
        self.temperature = temperature
        self.weather = weather
        self.icon = icon


