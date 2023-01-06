# SkyrimPotionCreator
 Quick and dirty calculator to see what potions you can make in skyrim given your current ingredients
 
 Simply fill out the ingredients.json with the number of each ingredient in your inventory and run the python program. You can use the flags to change the input files if you'd prefer, but there really is no need to.
 
# Usage
```
usage: PotionMaker.py [-h] [-p POTION_RECIPE_FILE] [-i INGREDIENTS] [--debug] [--logging LOGGING]

optional arguments:
  -h, --help            show this help message and exit
  -p POTION_RECIPE_FILE, --potion_recipe_file POTION_RECIPE_FILE
                        JSON file with all potion recipes
  -i INGREDIENTS, --ingredients INGREDIENTS
                        JSON file with your current ingredients
  --debug               Show debug information
  --logging LOGGING     Log file
```
