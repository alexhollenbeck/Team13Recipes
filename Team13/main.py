import categories,parse,objects
import transformDiet
import transformHealthy
import transformCuisine
cuisines = ['indian','mediterranean','cannibal']

def main():
    categories.ingredientDB = parse.readIngredientsFromFile('FOOD_DATA/FOOD_DES.txt')
    categories.update()
    debug = True

    print "Recipe transformer initialized."
    recipeURL = raw_input("Enter a url for a recipe page from allrecipes.com:")
    print 'Loading recipe...'
    recipeInfo = parse.getRecipe(recipeURL)
    print 'Processing data...'
    recipe = parse.processRecipe(recipeInfo)
    print "Recipe loaded. \n Transformations:\n For a diet (vegetarian and lactose-free) tranformation (or 'un-diet') type 0\n For a healthy transformation type 1\n For a cuisine transformation type 2\n"
    transformationType = int(raw_input("Choose a transformation: "))
    if transformationType ==0:
        print "Diet transformation selected. To convert from meat and lactose to vegetarian and lactose-free type 0, otherwise type 1:"
        dietType = int(raw_input("Diet Selection: "))
        vegRecipe = transformDiet.transformDiet(recipe, dietType == 0)
        transformDiet.printRecipe(vegRecipe, "Diet")
    elif transformationType ==1:
        print "Healthy transformation selected. To convert to healthy type 0, otherwise type 1"
        healthyType = int(raw_input("Healthy Selection: "))
        healthyRecipe = transformHealthy.transformHealthy(recipe, healthyType == 0)
        transformHealthy.printRecipe(healthyRecipe, "Healthy")
    elif transformationType ==2:
        print "Cuisine transformation selected. Choose a cuisine type:\n For Indian type 0 \n For Mediterranean type 1\n For Cannibal type 2"
        cuisineType = int(raw_input("Cuisine Type: "))

        if cuisineType ==0:
            transformCuisine.cuisineChange(recipe,cuisines[0])
        elif cuisineType ==1:
            transformCuisine.cuisineChange(recipe,cuisines[1])
        elif cuisineType ==2:
            transformCuisine.cuisineChange(recipe,cuisines[2])
        else:
            print "Incorrect cuisine choice. Please try again."
    else:
        print "Incorrect transformation choice. Please try again."

main()
