Recipes Project - EECS 337
========
#### Zak Allen, Shikhar Mohan, Alex Hollenbeck, Tasha McKinney


Written in Python 2.7, this project applies transformations to recipes from allrecipes.com
>Food data and ingredient nutrient information sourced from http://ashleyw.co.uk/project/food-nutrient-database

### Transformations
1. Vegetarian & Lactose-free
2. Cuisine transformation: Indian, Mediterranean, and Cannibal
3. Healthy - low fat & low sodium

>All of the transformations will involve ingredient substitutions. Ingredients each have a type (protein, seasoning, etc), and substitutions will only be allowed if the two ingredients are of the same type. The nature of the substitution depends on the transformation:

1. Look for ingredients in the recipe whose dietary restrictions field includes vegetarian. Replace those ingredients with ingredients of the same type. If lactose-free options are desired, look for ingredients in the recipe that contain lactose, and replace with lactose-free ingredients.

2. For each ingredient in the recipe, check if it is present in the list of possible ingredients for the desired cuisine. If it is not, replace it with an ingredient of the same type.

3. For each ingredient in the recipe check if it falls beneath a baseline "healthy" level of fat or sodium. If it does not, replace it with an ingredient of the same type that does fall beneath the baseline.

>All of the recipe transformations are reversible:

1. For recipes that are vegetarian or lactose-free, ingredients are substituted for meat or ingredients with lactose of the same type. 

2. For each ingredient in the starting cuisine type check if it is present in the list of possible ingredients for the desired cuisine. If it is not, replace it with an ingredient of the same type.

3. For each ingredient in the recipe, check if it is falls beneath a baseline "healthy" level of fat or sodium or contains "low-fat" or "low-sodium". If it does, replace it with an ingredient of the same type that does not fall beneath the baseline.


### Running
<b>Dependencies:</b> beautifulsoup4<br>
To install beautifulsoup4 run:
```
sudo pip install beautifulsoup4
```
After dependency installation navigate to Team13 folder and just run main:
```
cd Team13
python main.py
``` 
and follow the provided prompts
<br>
<b>Autograder:</b> <br>
Navigate to Team13 folder and run autograder:
```
cd Team13
python autograder.py
```

NOTE: This project runs the OLD version of the autograder. It requires a json answers file in the Recipes folder with a url, which is included in this repo.