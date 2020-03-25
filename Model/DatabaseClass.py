import sqlite3

cylinderArray = []
ingredientArray = []

# connect to the database called example.db

conn = sqlite3.connect(r'database/pysqlite.db')


class Cylinder:
    def __init__(self, cylinderID, ingredient, amount, cylinderType):
        self.cylinderID = cylinderID
        self.ingredient = ingredient
        self.amount = amount
        self.cylinderType = cylinderType

class Ingredient:
    def __init__(self, ingredientID, ingredient, ingredientType):
        self.ingredientID = ingredientID
        self.ingredient = ingredient
        self.ingredientType = ingredientType

