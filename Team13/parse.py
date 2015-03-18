import objects
import categories
import string
import pprint
import sys
import re
import pdb
from urllib2 import urlopen
from bs4 import BeautifulSoup

def getRecipe(url):
    recipePage = urlopen(url)
    soup = BeautifulSoup(recipePage.read())
    recipeInfo = {}
    recipeInfo["title"] = soup.find(id="itemTitle").string
    recipeInfo["rating"] = soup.find(itemprop="ratingValue")["content"]
    recipeInfo["author"] = soup.find("span", {"id": "lblSubmitter"}).text
    recipeInfo["servings"] = soup.find(id="lblYield").string
    recipeInfo["time"] = soup.find_all("span", {"class":"time"})
    if recipeInfo["time"]:
        recipeInfo["time"] = recipeInfo["time"][0].text
    ingredientsListing = soup.findAll(itemprop="ingredients")
    ingredients = []
    for ingredient in ingredientsListing:
        if ingredient.find_next(id="lblIngName"):
            nextEl = ingredient.find_next(id="lblIngName")
            if nextEl["class"][0] == "ingred-heading" or nextEl.string.replace(u'\xa0', u' ') == " ":
                continue
            else:
                amount = ""
                name = ""
                if ingredient.find_next(id="lblIngAmount"):
                    amount = ingredient.find_next(id="lblIngAmount").string
                if ingredient.find_next(id="lblIngName"):
                    name = ingredient.find_next(id="lblIngName").string
                ingredients.append({"name": name, "amount": amount})
    recipeInfo["ingredients"] = ingredients
    directionsListing = soup.find_all("span", {"class":"plaincharacterwrap break"})
    directions = []
    for direction in directionsListing:
        directions.append(direction.string)
    recipeInfo["directions"] = directions
    rec = processRecipe(recipeInfo)
    recipeInfo['primary cooking method'] = rec.secondaryMethods
    recipeInfo['secondary cooking method'] = rec.secondaryMethods
    meth = []
    meth.append(rec.secondaryMethods)
    meth.append(rec.secondaryMethods)
    meth = sum(meth, [])
    recipeInfo['cooking tools'] = rec.tools
    recipeInfo['cooking methods'] = meth 
    return recipeInfo
    

def processRecipe(recipeInfo):
    recipe = objects.Recipe(name=recipeInfo['title'],
        author= recipeInfo['author'], 
        cookTime=recipeInfo['time'], 
        servings=recipeInfo['servings'], 
        rating=recipeInfo['rating'])
    recipe.ingredients = parseIngredients(recipeInfo['ingredients'])
    toolsAndMethods = findToolsAndMethods(recipeInfo['directions'],recipe.ingredients)  
    recipe.tools= toolsAndMethods['tools']
    recipe.secondaryMethods = toolsAndMethods['secondaryMethods']
    recipe.secondaryMethods = toolsAndMethods['secondaryMethods']
    recipe.directions = recipeInfo['directions']
    recipe.steps = makeSteps(recipeInfo['directions'],recipe.tools,recipe.secondaryMethods,recipe.secondaryMethods)
    return recipe

def parseIngredient(dict):
    amount = dict['amount']
    name = dict['name']
    amount = amount.split()
    if amount:
        amnt = amount[0]
    else:
        amnt = ""
    if len(amount) > 2:
        a = ''
        for x in range(1, len(amount)):
            if '/' in amount[x]:
                amnt += ' ' + amount[x]
            else:
                a += ' ' + amount[x]
        unit = a
    else:
        try:
            unit = amount[1]
        except:
            unit = 'not specified'
    amount = amnt
    amnt = amount.split()
    total = 0
    for numb in amnt:
        if '/' in numb:
            recon = ''
            for char in numb:
                if char != '/':
                    recon += char + '.0'
                else:
                    recon += char
            numb = eval(recon)
            total += numb
        else:
            total += float(numb)
    amount = str(total)
    if float(amount) > 1:
        if name.endswith('s'):
            name = name[:-1]
    ing = findIngredient(name)
    ing.amount = amount
    ing.unit = unit
    ing.updateString()
    return ing

def findIngredient(ingr):
    ingr = ingr.lower()
    items = ingr.split()
    descriptors = []
    preparations = []
    soupOrSauce = False
    spiceOrPowder = False
    babyFood = False
    dairyProduct = False
    rawFood = False
    meatProduct = False
    sweetProduct = False
    snackProduct = False
    grainProduct = False
    beefProduct = False
    porkProduct = False
    poultryProduct = False
    fishProduct = False
    gameProduct = False
    groundProduct = False
    primeIng = ''
    for item in items:
        if item.endswith(','):
            if item.endswith('less,'):
                pass
            else:
                primeIng = item
                break
    if primeIng == '':
        filter = []
        if 'for' in items:
            ind = items.index('for')
            for j in range(0, ind):
                filter.append(items[j])
        elif 'with' in items:
            ind = items.index('with')
            for j in range(0, ind):
                filter.append(items[j])
        else:
            filter = items
        primeIng = filter[len(filter) - 1]
    primeIndex = items.index(primeIng)
    for x in range(0, primeIndex):
        if items[x].endswith('ed') and not items[x] == 'red':
            preparations.append(items[x])
        else:
            descriptors.append(items[x])
    p = items[(primeIndex + 1):]
    for item in p:
        preparations.append(item)
    if primeIng.endswith(','):
        primeIng = primeIng[:-1]
    if primeIng == 'zucchinis':
        primeIng = 'zucchini'
    primeIng = primeIng.lower()
    if (primeIng == 'soup' 
        or primeIng == 'sauce' 
        or primeIng == 'paste'
        or primeIng == 'bouillon'
        or primeIng == 'spread'):
        soupOrSauce = True
    if (primeIng == 'spice' 
        or primeIng == 'powder' 
        or primeIng == 'salt'
        or primeIng == 'cinnamon'
        or primeIng == 'nutmeg'):
        spiceOrPowder = True
    if 'baby' in items:
        babyFood = True
    if ('cheese' in primeIng 
        or 'milk' in primeIng 
        or 'cream' in primeIng 
        or 'yogurt' in primeIng 
        or 'whey' in primeIng 
        or 'egg' in primeIng 
        or 'butter' in primeIng
        or 'yolk' in primeIng):
        dairyProduct = True
        rawFood = True
    if 'fresh' in items or 'raw' in items:
        rawFood = True
    if ('meat' in items 
        or 'beef' in items 
        or 'pork' in items 
        or 'chicken' in items
        or 'turkey' in items
        or 'lamb' in items 
        or 'fish' in items
        or 'bacon' in items
        or 'mutton' in items):
        meatProduct = True
        rawFood = True
    if 'ground' in items:
        groundProduct = True
    if ('beef' in items
        or 'steak' in items):
        beefProduct = True
    if ('bacon' in items
        or 'pork' in items):
        porkProduct = True
    if ('chicken' in items
        or 'duck' in items
        or 'poultry' in items
        or 'turkey' in items):
        poultryProduct = True
    if ('lamb' in items
        or 'mutton' in items
        or 'veal' in items):
        gameProduct = True
    if ('fish' in items):
        fishProduct = True
    if ('sugar' in items 
        or 'syrup' in items 
        or 'sweetener' in items 
        or 'pudding' in items 
        or 'candies' in items 
        or 'candy' in items 
        or 'honey' in items 
        or 'frosting' in items
        or 'topping' in items
        or 'pie filling' in items
        or 'pectin' in items
        or 'marmalade' in items
        or 'molasses' in items
        or 'jelly' in items
        or 'jam' in items
        or 'fruit butter' in items
        or 'dessert' in items
        or 'flan' in items
        or 'rennin' in items
        or 'custard' in items
        or 'cocoa' in items
        or 'gum' in items
        or 'gelatin' in items
        or 'chocolate' in items
        or 'sherbet' in items):
        sweetProduct = True
    if ('cracker' in primeIng
        or 'crumbs' in primeIng):
        snackProduct = True
    if ('flour' in primeIng
        or 'grain' in primeIng
        or 'barley' in primeIng
        or 'cornmeal' in primeIng
        or 'millet' in primeIng
        or 'rice' in primeIng
        or 'pasta' in primeIng
        or 'noodle' in primeIng
        or 'oat' in primeIng
        or 'wheat' in primeIng
        or 'macaroni' in primeIng
        or 'spaghetti' in primeIng
        or 'hominy' in primeIng
        or 'sorghum' in primeIng
        or 'teff' in primeIng
        or 'quinoa' in primeIng
        or 'triticale' in primeIng
        or 'rye' in primeIng
        or 'couscous' in primeIng
        or 'bulgur' in primeIng
        or 'amaranth' in primeIng):
        grainProduct = True
    matches = []
    for DBing in categories.ingredientDB:
        matchScore = 0.0
        match = False
        soup = False
        spice = False
        baby = False
        dairy = False
        raw = False
        meat = False
        sweet = False
        snack = False
        grain = False
        pork = False
        beef = False
        poultry = False
        game = False
        fish = False
        meatMix = False
        ground = False
        if primeIng == 'flour':
            primeIng = 'flr'
        des = DBing.descriptor.split()
        nam = DBing.name.split(',')
        if DBing.category == '0600':
            soup = True
        if DBing.category == '0200':
            spice = True
        if DBing.category == '0300':
            baby = True
        if DBing.category == '0100':
            dairy = True
        if (DBing.category == '0500' 
            or DBing.category == '0700' 
            or DBing.category == '1000' 
            or DBing.category == '1300' 
            or DBing.category == '1500' 
            or DBing.category == '1700'):
            meat = True
        if 'BY-PRODUCTS' in DBing.name:
            meatMix = True
        if 'ground' in DBing.descriptor:
            gound = True
        if DBing.category == '0500':
            poultry = True
        if DBing.category == '1000':
            pork = True
        if DBing.category == '1300':
            beef = True
        if DBing.category == '1500':
            fish = True
        if DBing.category == '1700':
            game = True
        if DBing.category == '1900':
            sweet = True
        if DBing.category == '1800':
            snack = True
        if DBing.category == '2000':
            grain = True
        if 'RAW' in DBing.name:
            raw = True
        for word in nam:
            if primeIng not in word.lower():
                pass
            else:
                match = True
                if primeIng == word.lower():
                    matchScore += 100
                else:
                    matchScore += 50
                break
        for word in descriptors:
            if word == 'and':
                pass
            else:
                if word not in DBing.descriptor.lower():
                    pass
                else:
                    match = True
                    if word in categories.colors:
                        r = .1
                    elif descriptors.index(word) == len(descriptors) - 1:
                        r = .8 
                    else:
                        r = 1
                    for d in des:
                        if word in d.lower():
                            if word == 'crumbs':
                                pass
                            c = ''
                            if d.endswith(','):
                                c = d[:-1]
                            if word == c or word == d.lower():
                                matchScore += 2.0 / ((des.index(d) + 1.0) * r)
                            else:
                                matchScore += 1.0 / ((des.index(d) + 1.0) * r)
                            break
        if match:
            ing = objects.Ingredient()
            if primeIng == 'flr':
                ing.name += 'flour'
            else:
                ing.name += primeIng
            ing.origName = primeIng
            if len(descriptors) != 0:
                ing.descriptor = ''
            for i in descriptors:
                ing.descriptor += i + ' '
            ing.id = DBing.id
            if preparations == []:
                pass
            else:
                if ing.preparation == 'None':
                    ing.preparation = ''
                for word in preparations:
                    ing.preparation += word + ' '
            ing.category = DBing.category
            if DBing.protein != '' and DBing.protein != '\n':
                ing.protein = DBing.protein
            if DBing.sodium != '' and DBing.sodium != '\n':
                ing.sodium = DBing.sodium
            if DBing.fat != '' and DBing.fat != '\n':
                ing.fat = DBing.fat
            if soup and not soupOrSauce:
                matchScore = matchScore / 3.0
            if spice and not spiceOrPowder:
                matchScore = matchScore / 2.0
            if baby and not babyFood:
                matchScore = matchScore / 2.0
            if dairy and not dairyProduct:
                matchScore = matchScore / 2.0
            if rawFood and not raw:
                matchScore = matchScore / 2.0
            if meat and not meatProduct:
                matchScore = matchScore / 2.0
            if meatProduct and meatMix:
                matchScore = matchScore / 2.0
            if porkProduct and not pork:
                matchScore = matchScore / 5.0
            if beefProduct and not beef:
                matchScore = matchScore / 5.0
            if poultryProduct and not poultry:
                matchScore = matchScore / 5.0
            if fishProduct and not fish:
                matchScore = matchScore / 5.0
            if gameProduct and not game:
                matchScore = matchScore / 5.0
            if sweet and not sweetProduct:
                matchScore = matchScore / 2.0
            if sweetProduct and not sweet:
                matchScore = matchScore / 2.0
            if snack and not snackProduct:
                matchScore = matchScore / 2.0
            if grain and not grainProduct:
                matchScore = matchScore / 2.0
            if grainProduct and not grain:
                matchScore = matchScore / 2.0
            if ground and not groundProduct:
                matchScore = matchScore / 2.0
            tup = (ing, matchScore)
            matches.append(tup)
    result = objects.Ingredient()
    topIndex = 0
    topScore = 0
    for find in matches:
        if find[1] > topScore:
            result = find[0]
            topIndex = matches.index(find)
            topScore = find[1]
    if result.name == 'flr':
        result.name = 'flour'
    if '.' not in result.sodium:
        result.sodium = '0.00'
    if '.' not in result.fat:
        result.fat = '0.00'
    if '.' not in result.protein:
        result.protien = '0.00'
    return result

def parseIngredients(ingredients):
    ings = []
    for ing in ingredients:
        ings.append(parseIngredient(ing))
    return ings

def findToolsAndMethods(directions,ingredients):
    exclude = set(string.punctuation)
    ingredientsList = []
    for ing in ingredients:
        ingredientsList.append(ing.name)
    words = []
    parsed = {"tools":[],"secondaryMethods":[],"secondaryMethods":[]}
    for sentence in directions:
        sentence = ''.join(ch for ch in sentence if ch not in exclude)
        w = sentence.split()
        for word in w:
            word = word.lower()
            if word not in words:
                words.append(word)
    for word in words:
        nextWordIndex = words.index(word)+1
        double_word =''
        try:
            double_word = word+' '+words[nextWordIndex]
        except:
            double_word = word
        try:
            lastTool = parsed['tools'][-1]
        except:
            lastTool = ''
        if word not in lastTool:
            if double_word in categories.tools:
                parsed['tools'].append(double_word)
            elif word in categories.tools:
                if double_word not in ingredientsList:
                    parsed['tools'].append(word)
        if double_word in categories.secondaryMethods:
            parsed['secondaryMethods'].append(double_word)
        elif word in categories.secondaryMethods:
            if double_word not in ingredientsList:
                parsed['secondaryMethods'].append(word)
        if double_word in categories.secondaryMethods:
            parsed['secondaryMethods'].append(double_word)
        elif word in categories.secondaryMethods:
            if double_word not in ingredientsList:
                parsed['secondaryMethods'].append(word)
    return parsed

def makeSteps(directions,tools,mainMethods,secondaryMethods):
    listOfSteps =[]
    exclude = set(string.punctuation)
    for direction in directions:
        steps = direction.split('.')
        for step in steps:
            if step:
                stepObj = objects.Step()
                stepObj.direction = step
                sentence = ''.join(ch for ch in step if ch not in exclude)
                w = sentence.split()
                for word in w:
                    nextWordIndex = w.index(word)+1
                    double_word = ''
                    try:
                        double_word = word + ' '+w[nextWordIndex]
                    except:
                        double_word = word
                    word = word.lower()
                    double_word = double_word.lower()
                    if double_word in tools and double_word not in stepObj.tools:
                        stepObj.tools.append(double_word)
                    elif word in tools and word not in stepObj.tools:
                        stepObj.tools.append(word)
                    if double_word in secondaryMethods and double_word not in stepObj.secondaryMethods:
                        stepObj.secondaryMethods.append(double_word)
                    elif word in secondaryMethods and word not in stepObj.secondaryMethods:
                        stepObj.secondaryMethods.append(word)
                    if double_word in secondaryMethods and double_word not in stepObj.secondaryMethods:
                        stepObj.secondaryMethods.append(double_word)
                    elif word in secondaryMethods and word not in stepObj.secondaryMethods:
                        stepObj.secondaryMethods.append(word)
                    pat = re.search('minute*|hour*',double_word,re.IGNORECASE)
                    time= double_word.split()
                    if pat and time[0].isdigit():
                        stepObj.time = double_word
                listOfSteps.append(stepObj)
    return listOfSteps

def tokenizeLine(string):
    line = string.split('^')
    numArgs = len(line)
    out = []
    for item in line:
        if item == '':
            out.append(item)
        else:
            if item[0] != '~':
                out.append(item)
            else:
                text = item.split('~')
                empty = False
                appended = False
                for word in text:
                    if len(text) == 3 and text[1] == word and word != '':
                        out.append(word)
                        appended = True
                    if empty and word == '' and not appended:
                        out.append(word)
                        empty = False
                        appended = True
                    else:
                        if word == '':
                            empty = True
    return out

def readIngredientFromLine(line):
    tokens = tokenizeLine(line)
    output = objects.Ingredient()
    output.category = tokens[1]
    output.descriptor = tokens[2].lower()
    output.name = tokens[3]
    output.protein = tokens[11]
    output.fat = tokens[12]
    output.sodium = tokens[13]
    return output

def readIngredientsFromFile(fileName):
    ingredientList = []
    with open(fileName, 'r') as f:
        while(True):
            line = f.readline()
            if not line:
                break
            ingredientList.append(readIngredientFromLine(line))
    return ingredientList