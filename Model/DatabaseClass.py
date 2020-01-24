import sqlite3

cylinderArray = []
ingredientArray = []

# connect to the database called example.db
conn = sqlite3.connect('Model/Cylinder.db')
cylinderCursor = conn.cursor()
ingredientCursor = conn.cursor()
queryCursor = conn.cursor()

class Cylinder:
    def __init__(self, cylinderID, ingredient, amount):
        self.cylinderID = cylinderID
        self.ingredient = ingredient
        self.amount = amount


class Ingredient:
    def __init__(self, ingredientID, ingredientType):
        self.ingredientID = ingredientID
        self.ingredientType = ingredientType
