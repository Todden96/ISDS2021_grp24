import requests # import the module requests
import pandas as pd
data  = requests.get('https://api.punkapi.com/v2/beers?page=1&per_page=80&brewed_after=01-04-2004&abv_gt=5') # submit query with `get` and save response as object

type(data )

jsondata = data.json()


len(jsondata)


type(jsondata)

df = pd.DataFrame.from_dict(jsondata)