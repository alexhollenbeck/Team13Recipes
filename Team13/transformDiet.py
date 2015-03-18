import categories, re, copy, parse, random, pdb
from categories import dietSubstitutions as dietSubs
from categories import undietSubstitutions as undietSubstitutions
from categories import meats as meats

def transformDiet(recipe, diet):
    dietRecipe = recipe
    subbedIngs = {}
    if not diet:
        dietSubstitutions = undietSubstitutions
    else:
        dietSubstitutions = dietSubs
    for ingredient in dietRecipe.ingredients:
        substitution = ""
        if ingredient.name in dietSubstitutions:
            baseIng = dietSubstitutions[ingredient.name]
            if ingredient.descriptor in baseIng:
                substitution = baseIng[ingredient.descriptor]
            else:
                if baseIng[""]:
                    substitution = baseIng[""]
                else:
                    print "Nothing to substitute"
        if ingredient.name in meats and diet:
            substitution = "tofu"
        descs = ingredient.descriptor.split()
        for word in descs:
            if word in meats and diet:
                substitution = "tofu"
        if ingredient.name == "tofu" and not diet:
            substitution = random.choice(meats)
        if substitution:
            newIng = dietSubIngredient(ingredient, substitution)
            ind = dietRecipe.ingredients.index(ingredient)
            dietRecipe.ingredients[ind] = newIng
            subbedIngs[newIng] = dietRecipe.ingredients[ind]
            print 'Substituting ', ingredient.name, ' for ', substitution
    dir = dietRecipe.directions
    for step in dir:
        newStep = re.split(r'[;,\s]\s*', step)
        for word in range(0, len(newStep)):
            if newStep[word] in meats and diet:
                newStep[word] = "tofu"
        newStep = ' '.join(newStep)
        ind = dir.index(step)
        dir[ind] = newStep
    dietRecipe.directions = dir
    dietRecipe.steps = parse.makeSteps(dietRecipe.directions, dietRecipe.tools, dietRecipe.mainMethods, dietRecipe.secondaryMethods)
    return dietRecipe

def dietSubIngredient(ingredient, substitution = '', sodium = False, fat = False):
    if substitution:
        newIng = parse.parseIngredient({"name":substitution, "amount": ""})
    newIng.unit = ingredient.unit
    newIng.amount = ingredient.amount
    return newIng

def printRecipe(recipe, transformType): 
    recipe.name = "%s Version of - " % transformType + recipe.name
    print recipe.unicode()