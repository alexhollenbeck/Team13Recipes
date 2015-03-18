import categories, re, copy, parse
from categories import healthySubstitutions as healthySubstitutions

def transformHealthy(recipe, boo):
    healthyRecipe = recipe
    subbedIngs = {}
    fat = False
    sodium = False
    for ingredient in healthyRecipe.ingredients:
        substitution = ""
        if ingredient.name in healthySubstitutions:
            baseIng = healthySubstitutions[ingredient.name]
            if ingredient.descriptor in baseIng:
                substitution = baseIng[ingredient.descriptor]
            else:
                if baseIng[""]:
                    substitution = baseIng[""]
                else:
                    print "Nothing to substitute"
        if '.' not in ingredient.sodium:
            ingredient.sodium = '0.00'
        if '.' not in ingredient.fat:
            ingredient.fat = '0.00'
        try:
            if substitution:
                newIng = healthySubIngredient(ingredient, substitution)
                ind = healthyRecipe.ingredients.index(ingredient)
                healthyRecipe.ingredients[ind] = newIng
                print 'Substituting ', ingredient.name, ' for ', substitution
            elif float(ingredient.fat) > 9.0 and 'low' not in ingredient.descriptor and 'fat' not in ingredient.descriptor and not ingredient.category == '0900' and not ingredient.category == '1100':
                newIng = healthySubIngredient(ingredient, boo, fat = True)
                fat = True
                subbedIngs[ingredient.name] = newIng.name
                ind = healthyRecipe.ingredients.index(ingredient)
                healthyRecipe.ingredients[ind] = newIng
                print 'Substituting ', ingredient.name, ' for ', newIng.name
            elif float(ingredient.sodium) > 3.5 and 'low' not in ingredient.descriptor and 'sodium' not in ingredient.descriptor and not ingredient.category == '0900' and not ingredient.category == '1100':
                newIng = healthySubIngredient(ingredient, boo, sodium = True)
                sodium = True
                subbedIngs[ingredient.name] = newIng.name
                ind = healthyRecipe.ingredients.index(ingredient)
                healthyRecipe.ingredients[ind] = newIng
                print 'Substituting ', ingredient.name, ' for ', newIng.name
        except:
            try:
                float(ingredient.fat)
            except:
                print ingredient.fat, 'cannot be converted to a float'
            try:
                float(ingredient.sodium)
            except:
                print ingredient.sodium, 'cannot be converted to a float'
    dir = healthyRecipe.directions
    for step in dir:
        newStep = step.split()
        for word in newStep:
            if word.endswith(','):
                word = word[:-1]
            if word in healthySubstitutions:
                try:
                    ind = newStep.index(word)
                except:
                    word = word + ','
                    ind = newStep.index(word)
                    word = word[:-1]
                newStep[ind] = healthySubstitutions[word]
                if not isinstance(newStep[ind], basestring):
                    newStep[ind] = newStep[ind][""]
            elif word in subbedIngs:
                try:
                    ind = newStep.index(word)
                except:
                    word = word + ','
                    ind = newStep.index(word)
                    word = word[:-1]
                newStep[ind] = subbedIngs[word]
        newStep = ' '.join(newStep)
        ind = dir.index(step)
        dir[ind] = newStep
    healthyRecipe.directions = dir
    healthyRecipe.steps = parse.makeSteps(healthyRecipe.directions, healthyRecipe.tools, healthyRecipe.mainMethods, healthyRecipe.secondaryMethods)
    if not boo: 
        if sodium:
            dir.append("Add lots of salt")
        else:
            dir.append("Add lots of lard or grease")
    return healthyRecipe

def healthySubIngredient(ingredient, boo, substitution = '', sodium = False, fat = False):
    if not boo:
        if substitution:
            newIng = parse.parseIngredient({"name":substitution, "amount": ""})
        elif sodium:
            newIng = parse.parseIngredient({"name": 'extra salt', "amount": "100"})
        elif fat:
            newIng = parse.parseIngredient({"name": 'extra lard', "amount": "100"})
    else:
        if substitution:
            newIng = parse.parseIngredient({"name":substitution, "amount": ""})
        elif sodium:
            newIng = parse.parseIngredient({"name": 'low sodium ' + ingredient.descriptor + ' ' + ingredient.name + ', ' + ingredient.preparation, "amount": ""})
        elif fat:
            newIng = parse.parseIngredient({"name": 'low fat ' + ingredient.descriptor + ' ' + ingredient.name + ', ' + ingredient.preparation, "amount": ""})
    newIng.unit = ingredient.unit
    newIng.amount = ingredient.amount
    return newIng

def printRecipe(recipe, transformType): 
    recipe.name = "%s Version of - " % transformType + recipe.name
    print recipe.unicode()