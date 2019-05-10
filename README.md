# Walkscore_webscraper
An unofficial walk score web scraper that was built to find walk scores for cities of interest for a travel web app. The list of cities are provided by a CSV file which contains information from Foursquare (Geonames).

[](walkScoreScraper.py)

### WalkScore
[Walkscore](https://www.walkscore.com/) offers a service to provide a single metric that can describe the walkability, bikability, and transit-ability (?) of a location, neighborhood or city within the USA, Canada, or Australia. These scores are very useful for travelling, moving, and can even impact real estate value. 

Walkscore does offer an [API](https://www.walkscore.com/professional/walk-score-apis.php) which will yield the walk, transit, or bike scores  of a single location given a lat/long coordinate. However, the API currently does not provide walk scores aggregated by neighborhood or city. To find this information, you have to surf their [neighborhoood and city page](https://www.walkscore.com/cities-and-neighborhoods/). 

This web scraper was developped to access select cities. I found there is a general formula to URL construction which is ST/city for USA, and CC-ST/city for Canada/Australia. ST = abbreviated state, CC = county code.

### Input Data

Here is a sample of the CSV we fed to walkscore. The American cities have state information, while not all Canadian or Australian cities had their corresponding states. And if so, they were probably elongated version. As a work around, I had to manually create a dictionary of all Canadian or Australian provinces/states to reference. And for the sake of sharing, I will link these JSONs below.

### Canada


### Australia

