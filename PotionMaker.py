import argparse
import logging
import json

LOG_FORMAT = "[%(levelname)s] %(message)s"
LOG_DEBUG_FORMAT = "[%(threadName)s-%(filename)s-%(funcName)s-%(lineno)s | %(levelname)s] %(message)s"

log = logging.getLogger(__name__)

def has_necessary_ingredients(required_ingredients : list, all_ingredients : list) -> bool:
    has_count = 0
    for ingredient in required_ingredients:
        if ingredient in all_ingredients:
            has_count += 1
        if has_count >= 2:
            return True
    return False

def get_all_ingredients(supply : dict) -> list:
    all_ingredients = []
    for ingredient in supply.keys():
        if supply[ingredient] > 0:
            all_ingredients.append(ingredient)
    return all_ingredients

def trim_list_to_my_supply(my_available_ingredients : list, all_useable_ingredients : list) -> list:
    my_supply = []

    for ingredient in my_available_ingredients:
        if ingredient in all_useable_ingredients:
            my_supply.append(ingredient)
    
    my_supply.sort()
    return my_supply

def run(args, **kwargs):
    
    recipes = json.load(kwargs['potion_recipe_file'])
    my_supply = json.load(kwargs['ingredients'])

    if kwargs['reset']:
        for key in my_supply.keys():
            my_supply[key] = 0
        answer = input("Are you sure you want to clear your ingredients (y/n)? ").strip().lower()
        if (answer == 'y'):
            with open(kwargs["ingredients"].name, 'w') as ingredients_write_fd:
                json.dump(my_supply, ingredients_write_fd, indent=4)
            print("Ingredients cleared!")
        return

    all_available_ingredients = get_all_ingredients(my_supply)
    can_make = []
    for potion in recipes.keys():
        if has_necessary_ingredients(recipes[potion], all_available_ingredients):
            can_make.append(
                (potion, trim_list_to_my_supply(all_available_ingredients, recipes[potion]))
            )

    print("===Here are all the potions you can make===")
    for tup in can_make:
        print(f"{tup[0]}: {tup[1]}")

		
class SymbolFormatter(logging.Formatter):
    symbols = ["x", "!", "-", "+", "DBG"]
    
    def format(self, record):
        symbol_record = logging.makeLogRecord(vars(record))
		
        for index, symbol in enumerate(self.symbols):
            if record.levelno >= (len(self.symbols) - index) * 10:
                symbol_record.levelname = symbol
                break
			
        return super(SymbolFormatter, self).format(symbol_record)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--potion_recipe_file", type=argparse.FileType('r'), default="recipes.json", help="JSON file with all potion recipes")
    parser.add_argument("-i", "--ingredients", type=argparse.FileType('r'), default="ingredients.json", help="JSON file with your current ingredients")
    parser.add_argument("--debug", action="store_true", default=False, help="Show debug information")
    parser.add_argument("--logging", type=str, help="Log file")
    parser.add_argument("-r", "--reset", action="store_true", default=False, help="Resets ingredients JSON to all 0s")
    args = parser.parse_args()
    kwargs = vars(args)

    log.setLevel(logging.DEBUG)
	
    formatter = logging.Formatter(LOG_DEBUG_FORMAT) if args.debug else SymbolFormatter(LOG_FORMAT)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG if args.debug else logging.INFO)
    handler.setFormatter(formatter)
    log.addHandler(handler)
	
    if args.logging:
        file_handler = logging.FileHandler(args.logging)
        file_handler.setLevel(logging.DEBUG if args.debug else logging.INFO)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)

    try:
        run(args, **kwargs)
    except KeyboardInterrupt:
        log.debug("keyboard interrupt")
    except AssertionError as e:
        log.error(e)
    except Exception as e:
        log.debug("Unknown exception")
        log.exception(e)
		

if __name__ == "__main__":
	main()
