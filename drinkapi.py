import urllib.request
import json

# http://www.thecocktaildb.com/api/json/v1/1
# /random.php      # returns a random drink
# /lookup.php?i={} # returns drink with ID = {}
# /filter.php?     # find a drink with a given filter
#             i={} # find drinks with ingredient {}
#             a={} # find drinks with Alcoholic or Non_Alcoholic
#             c={} # find drinks in category Ordinary_Drink or Cocktail
#             g={} # finds drinks using glass {}
# /list.php?       # lookup valid entries
#             i=list
#             a=list
#             c=list
#             g=list
# /search.php?s={} # find drink with {} in name
###
# {"drinks":[{  # Dict with "drinks" and a list of drink dictionaries
#   idDrink                 # Unique ID
#   strDrink                # Name of drink
#   strAlcoholic            # Alcoholic or Non alcoholic?
#   strGlass                # Type of glass used
#   strInstructions         # Instructions for mixing drink
#   strDrinkThumb           # URL of thumbnail image for drink (Optional)
#   strIngredient1..15      # Ingredients in drink
#   strMeasure1..15         # Measurements for each ingredient
#   dateModified            # Date of last change
# }]}
###


drink_image = "{0[strDrink]}"
api_root = 'http://www.thecocktaildb.com/api/json/v1/1'
api_random = api_root + '/random.php'
api_filter = api_root + '/filter.php?'
api_list = api_root + '/list.php?'
api_i = "i={}"
api_a = "a={}"
api_c = "c={}"
api_g = "g={}"
api_search = '/search.php?s={}'


def getlist(list_type):
    url = api_list + list_type.format('list')
    with urllib.request.urlopen(url) as response:
        drink_data = response.read().decode('utf-8')
        drinks = json.loads(drink_data)['drinks']
        for drink in drinks:
            print(drink)


def search(term):
    url = api_search.format(term)
    with urllib.request.urlopen(url) as response:
        drink_data = response.read().decode('utf-8')
        drink = json.loads(drink_data)['drinks'][0]
        for key, value in drink.items():
            print(key, value)

if __name__ == "__main__":
    getlist(api_a)
    print('...')
    getlist(api_i)
    print('...')
    getlist(api_g)
    print('...')
    getlist(api_c)

