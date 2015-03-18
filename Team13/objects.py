class Ingredient:
    def updateString(self):
        self.string = ''
        self.string += 'Name: ' + self.name + '\n'
        self.string += 'Amount: ' + self.amount + '\n'
        self.string += 'Units: ' + self.unit + '\n'
        self.string += 'Descriptor: ' + self.descriptor + '\n'
        self.string += 'Preparation: ' + self.preparation + '\n'
        self.string += 'Category: ' + self.category + '\n'
        self.string += 'Protein: ' + self.protein + '\n'
        self.string += 'Fat: ' + self.fat + '\n'
        self.string += 'Sodium: ' + self.sodium + '\n'
    def __init__(self,
        name = None,
        amount = None, 
        unit = None,
        descriptor = None,
        preparation = None,
        category = None,
        protein = None,
        fat = None,
        sodium = None,
        id = None):
        if id == None:
            self.id = '00000'
        else:
            self.id = id
        if name == None:
            self.name = ''
        else:
            self.name = name
        if amount == None:
            self.amount = '0.0'
        else:
            self.amount = amount
        if unit == None:
            self.unit = 'Not specified'
        else:
            self.unit = unit
        if descriptor == None:
            self.descriptor = 'None'
        else:
            self.descriptor = descriptor
        if preparation == None:
            self.preparation = 'None'
        else:
            self.preparation = preparation
        if category == None:
            self.category = ''
        else:
            self.category = category
        if protein == None:
            self.protein = '0.00'
        else:
            self.protein = protein
        if fat == None:
            self.fat = '0.00'
        else:
            self.fat = fat
        if sodium == None:
            self.sodium = '0.00'
        else:
            self.sodium = sodium

    def unicode(self):
        self.updateString()
        return self.string

class Step:
    def updateString(self):
        self.string = ''
        self.string += '\nDirection: ' + self.direction + '\n'
        self.string += 'Tools:'
        first = True
        if self.tools:
            for tool in self.tools:
                if first:
                    self.string += tool
                    first = False
                else:
                    self.string+= ","+tool
        else:
            self.string+="None"
        self.string +='\nPrimary Methods:'
        first = True
        if self.mainMethods:
            for pm in self.mainMethods:
                if first:
                    self.string += pm
                    first = False
                else:
                    self.string +=','+pm
        else:
            self.string+="None"
        self.string +='\nSecondary Methods:'
        if self.secondaryMethods:
            first = True
            for sm in self.secondaryMethods:
                if first:
                    self.string +=sm
                    first = False
                else:
                    self.string +=','+sm
        else:
            self.string +="None"
        self.string +='\nTime:'
        self.string+=self.time or "None"

    def __init__(self,
        direction=None,
        tools=None,
        mainMethods=None,
        secondaryMethods = None,
        time=None):
        if direction == None:
            self.direction = 'None'
        else:
            self.direction = direction
        if tools == None:
            self.tools = []
        else:
            self.tools = tools
        if mainMethods == None:
            self.mainMethods =[]
        else:
            self.mainMethods = mainMethods
        if secondaryMethods == None:
            self.secondaryMethods = []
        else:
            self.secondaryMethods = secondaryMethods
        if time == None:
            self.time = 'None'
        else:
            self.time = time
    def unicode(self):
        self.updateString()
        return self.string

class Recipe:

    def updateString(self):
        self.string = '\n'
        self.string += 'Recipe Name: ' + self.name + '\n\n'
        self.string += '***************\n**INGREDIENTS**\n***************\n'
        for ing in self.ingredients:
            self.string += ing.unicode() + '\n'
        self.string += '\n\nStep by Step Breakdown of Directions: \n'
        for step in self.steps:
            self.string+='\n*******************\n'
            self.string +=step.unicode()+'\n'
        self.string += '\nAuthor: ' + self.author + '\n'
        self.string += 'Cook Time: ' + self.cookTime + '\n'
        self.string += 'Servings: ' + str(self.servings) + '\n'
        self.string += 'Rating: ' + str(self.rating) + '\n'
        self.string += 'Tools:'
        first = True
        for tool in self.tools:
            if first:
                self.string += tool
                first = False
            else:
                self.string +="," + tool
        self.string += '\nPrimary Methods:'
        first = True
        for method in self.mainMethods:
            if first:
                self.string +=method
                first = False
            else:
                self.string +=","+method

        self.string +='\nSecondary Methods:'
        first = True
        for sMethod in self.secondaryMethods:
            if first:
                self.string +=sMethod
                first = False
            else:
                self.string+=',' + sMethod

    def __init__(self, 
        name = None,
        ingredients = None,
        directions = None,
        steps = None,
        author = None,
        cookTime = None,
        servings = None,
        rating = None,
        tools = None,
        mainMethods = None,
        secondaryMethods = None,
        cuisine = None):
        self.string = ''
        if name == None:
            self.name = ''
        else:
            self.name = name
        if ingredients == None:
            self.ingredients = []
        else:
            self.ingredients = ingredients
        if directions == None:
            self.directions = 'None'
        else:
            self.directions = directions
        if steps == None:
            self.steps = []
        else:
            self.steps = steps
        if author == None:
            self.author = ''
        else:
            self.author = author
        if cookTime == None:
            self.cookTime = ''
        else:
            self.cookTime = cookTime
        if servings == None:
            self.servings = 0.0
        else:
            self.servings = servings
        if rating == None:
            self.rating = 0.0
        else:
            self.rating = rating
        if tools == None:
            self.tools = []
        else:
            self.tools = tools
        if mainMethods == None:
            self.mainMethods = []
        else:
            self.mainMethods = mainMethods
        if secondaryMethods == None:
            self.secondaryMethods = []
        else:
            self.secondaryMethods = secondaryMethods
        if cuisine == None:
            self.cuisine = ''
        else:
            self.cuisine = cuisine

    def unicode(self):
        self.updateString()
        return self.string