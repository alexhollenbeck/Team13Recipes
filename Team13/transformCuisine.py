from categories import cuisines as cuisines
import categories, parse,re,objects
from categories import poultryAndGame as poultryAndGame,\
livestock as livestock, \
stocks as stocks, \
seafood as seafood,\
meats as meats

meatsCategories = ['0500', '0700', '1000','1300','1700']
cheeseCategory = ['0100']
spiceHerbsCategory = ['0200']
sauce= ['0600']
veggiesGarnish = ['1100']

def cuisineChange(recipe, cuisineType):
	if cuisineType == "indian":
		changeToIndian(recipe)
	elif cuisineType == "mediterranean":
		changeToMediterranean(recipe)
	elif cuisineType == "cannibal":
		changeToCannibal(recipe)

def changeToIndian(recipe):
	cuisine = "indian"
	ingredients = recipe.ingredients
	cuisineMeats = cuisines[cuisine]["meats"]
	cuisineCheese = cuisines[cuisine]['cheese']
	cuisineSpiceHerb = cuisines[cuisine]['spicesAndHerbs']
	cuisineSauces = cuisines[cuisine]['sauces']
	cuisineVegGarn = cuisines[cuisine]['veggiesAndGarnish']
	modifiedIngredients=[]
	addSpices = False
	vegIndex = 0
	for ing in ingredients:
		category = ing.category
		if category in meatsCategories or ing.name in meats:
			if fitsCuisineForCategory(ing,cuisineMeats):
				(meat,meatInDescriptor) = findIngNames(ing,cuisineMeats)
				if meat in (poultryAndGame + seafood) or meatInDescriptor in (poultryAndGame + seafood):
					modifiedIngredients.append(updateIngredient(ing,cuisineMeats[0],"boneless",""))
				else:
					modifiedIngredients.append(updateIngredient(ing, cuisineMeats[1], "", ""))
		elif category in cheeseCategory:
			pat = re.search("cheese*",ing.name.lower())
			pat2 = re.search("cheese*",ing.descriptor.lower())
			if pat or pat2:
				if fitsCuisineForCategory(ing,cuisineCheese):
					(cheese,cheeseInDescriptor) = findIngNames(ing,cuisineCheese)
					modifiedIngredients.append(updateIngredient(ing,cuisineCheese[0],"",""))
		elif category in spiceHerbsCategory:
			if fitsCuisineForCategory(ing,cuisineSpiceHerb):
				if not addSpices:
					addSpices= True
					modifiedIngredients.append({ing.name+"$"+ing.descriptor:', '.join(cuisineSpiceHerb[0:3])})
					modifiedIngredients.append(updateIngredient(ing,"","",""))
				else:
					modifiedIngredients.append(updateIngredient(ing, "", "", ""))
		elif category in sauce or ing.name in stocks:
			if fitsCuisineForCategory(ing,cuisineSauces):
				modifiedIngredients.append(updateIngredient(ing,cuisineSauces[0],"tomato puree based",""))
		elif category in veggiesGarnish:
			veggieGarName = ing.name
			veggieDescriptor = ing.descriptor
			isVeggie = findVeggies(veggieGarName,veggieDescriptor,cuisine)
			if not isVeggie:
				if vegIndex < len(cuisineVegGarn):
					modifiedIngredients.append(updateIngredient(ing,cuisineVegGarn[vegIndex],"",""))
					vegIndex+=1
				else:
					modifiedIngredients.append(updateIngredient(ing,"","",""))
	if addSpices:
		for spiceHerb in cuisineSpiceHerb[0:3]:
			newIng=parse.findIngredient(spiceHerb)
			if not newIng.name:
				newIng = objects.Ingredient(name=spiceHerb)
			ingredients.append(newIng)
	recipe.ingredients = formatIngredients(ingredients)
	recipe.steps = replaceDirections(modifiedIngredients,recipe.steps)
	recipe.name = "Indian Version of -"+recipe.name
	print recipe.unicode()

def changeToMediterranean(recipe):
	cuisine = "mediterranean"
	ingredients = recipe.ingredients
	cuisineMeats = cuisines[cuisine]["meats"]
	cuisineCheese = cuisines[cuisine]['cheese']
	cuisineSpiceHerb = cuisines[cuisine]['spicesAndHerbs']
	cuisineSauces = cuisines[cuisine]['sauces']
	cuisineVegGarn = cuisines[cuisine]['veggiesAndGarnish']

	modifiedIngredients=[]
	addSpices = False
	vegIndex = 0
	for ing in ingredients:
		category = ing.category
		if category in meatsCategories or ing.name in meats:

			if fitsCuisineForCategory(ing,cuisineMeats):
				(meat,meatInDescriptor) = findIngNames(ing,cuisineMeats)
				if meat in (poultryAndGame + seafood) or meatInDescriptor in (poultryAndGame + seafood):
					modifiedIngredients.append(updateIngredient(ing,cuisineMeats[0],"boneless",""))
				else:
					modifiedIngredients.append(updateIngredient(ing, cuisineMeats[1], "lamb", ""))
		elif category in cheeseCategory:
			pat = re.search("cheese*",ing.name.lower())
			pat2 = re.search("cheese*",ing.descriptor.lower())
			if pat or pat2:
				if fitsCuisineForCategory(ing,cuisineCheese):
					(cheese,cheeseInDescriptor) = findIngNames(ing,cuisineCheese)
					modifiedIngredients.append(updateIngredient(ing,cuisineCheese[0],"",""))
		elif category in spiceHerbsCategory:
			if fitsCuisineForCategory(ing,cuisineSpiceHerb):
				if not addSpices:
					addSpices= True
					modifiedIngredients.append({ing.name+"$"+ing.descriptor:', '.join(cuisineSpiceHerb)})
					modifiedIngredients.append(updateIngredient(ing,"","",""))
				else:
					modifiedIngredients.append(updateIngredient(ing, "", "", ""))
		elif category in sauce:
			if fitsCuisineForCategory(ing,cuisineSauces):
				modifiedIngredients.append(updateIngredient(ing,cuisineSauces[0],"",""))
		elif category in veggiesGarnish:
			veggieGarName = ing.name
			veggieDescriptor = ing.descriptor
			isVeggie = findVeggies(veggieGarName,veggieDescriptor,cuisine)
			if not isVeggie:
				if vegIndex < len(cuisineVegGarn):
					modifiedIngredients.append(updateIngredient(ing,cuisineVegGarn[vegIndex],"",""))
					vegIndex+=1
				else:
					modifiedIngredients.append(updateIngredient(ing,"","",""))
	if addSpices:
		for spiceHerb in cuisineSpiceHerb[0:3]:
			newIng=parse.findIngredient(spiceHerb)
			if not newIng.name:
				newIng = objects.Ingredient(name=spiceHerb)
			ingredients.append(newIng)

	recipe.ingredients = formatIngredients(ingredients)
	recipe.steps = replaceDirections(modifiedIngredients,recipe.steps)
	recipe.name = "Mediterranean Version of - "+recipe.name
	print recipe.unicode()

def changeToCannibal(recipe):
	cuisine = "cannibal"
	ingredients = recipe.ingredients
	cuisineMeats = cuisines[cuisine]["meats"]
	cuisineCheese = cuisines[cuisine]['cheese']
	cuisineSpiceHerb = cuisines[cuisine]['spicesAndHerbs']
	cuisineSauces = cuisines[cuisine]['sauces']
	cuisineVegGarn = cuisines[cuisine]['veggiesAndGarnish']

	modifiedIngredients=[]
	addSpices = False
	vegIndex = 0
	for ing in ingredients:
		category = ing.category
		if category in meatsCategories or ing.name in meats:

			if fitsCuisineForCategory(ing,cuisineMeats):
				(meat,meatInDescriptor) = findIngNames(ing,cuisineMeats)
				modifiedIngredients.append(updateIngredient(ing, cuisineMeats[0], "", ""))
		elif category in cheeseCategory:
			pat = re.search("cheese*",ing.name.lower())
			pat2 = re.search("cheese*",ing.descriptor.lower())
			if pat or pat2:
				if fitsCuisineForCategory(ing,cuisineCheese):
					(cheese,cheeseInDescriptor) = findIngNames(ing,cuisineCheese)
					modifiedIngredients.append(updateIngredient(ing,cuisineCheese[0],"",""))
		elif category in spiceHerbsCategory:
			if fitsCuisineForCategory(ing,cuisineSpiceHerb):
				if not addSpices:
					addSpices= True
					modifiedIngredients.append({ing.name+"$"+ing.descriptor:', '.join(cuisineSpiceHerb)})
					modifiedIngredients.append(updateIngredient(ing,"","",""))
				else:
					modifiedIngredients.append(updateIngredient(ing, "", "", ""))
		elif category in sauce:
			if fitsCuisineForCategory(ing,cuisineSauces):
				modifiedIngredients.append(updateIngredient(ing,cuisineSauces[0],"",""))

		elif category in veggiesGarnish:
			veggieGarName = ing.name
			veggieDescriptor = ing.descriptor
			isVeggie = findVeggies(veggieGarName,veggieDescriptor,cuisine)
			if not isVeggie:
				if vegIndex < len(cuisineVegGarn):
					modifiedIngredients.append(updateIngredient(ing,cuisineVegGarn[vegIndex],"",""))
					vegIndex+=1
				else:
					modifiedIngredients.append(updateIngredient(ing,"","",""))
	if addSpices:
		for spiceHerb in cuisineSpiceHerb[0:3]:
			newIng=parse.findIngredient(spiceHerb)
			if not newIng.name:
				newIng = objects.Ingredient(name=spiceHerb)
			ingredients.append(newIng)

	recipe.ingredients = formatIngredients(ingredients)
	recipe.steps = replaceDirections(modifiedIngredients,recipe.steps)
	recipe.name = "Cannibal Version of -"+recipe.name
	print recipe.unicode()

def replaceDirections(ingredients,steps):
	for ing in ingredients:
		for key,value in ing.iteritems():
			for step in steps:
				splitKey = key.split('$')
				name = splitKey[0]
				descriptor = splitKey[1]
				print 'DIR: ', name, ' ', descriptor
				val = re.search("(?i)(%s|%s)" % (name, descriptor), step.direction)
				if val:
					step.direction = re.sub("(?i)(%s|%s)" % (name, descriptor), value, step.direction)
	return steps

def findVeggies(name,descriptor,cuisine):
	for veggie in cuisines[cuisine]['veggiesAndGarnish']:
		pat = re.search("%s.*" % veggie,name)
		pat2 = re.search("%s.*" % veggie,descriptor)
		if pat:
			return True
		elif pat2:
			return True

def findInDescriptor(descriptor, cuisineList):
	words = descriptor.split(' ')
	x = ''
	for word in words:
		if word in cuisineList:
			x = word
			break
	return x

def formatIngredients(ingredientsList):
	uniqueIng = []
	finalIng = []
	for ing in ingredientsList:
		if not ing.name in uniqueIng and ing.name:
			uniqueIng.append(ing.name)
			finalIng.append(ing)
	return finalIng

def updateIngredient(ingredient, name, descriptor, preparation):
	origName = ingredient.name
	origDesc = ingredient.descriptor
	ingredient.name = name
	ingredient.descriptor = descriptor
	ingredient.preparation = preparation

	return {origName + "$" + origDesc:name}

def findIngNames(ing, category):
	return (ing.name, findInDescriptor(ing.descriptor, category))

def fitsCuisineForCategory(ing, category):
	(name, nameInDescriptor) = findIngNames(ing, category)
	fits = False
	if name not in category and nameInDescriptor not in category:
		fits = True
	return fits