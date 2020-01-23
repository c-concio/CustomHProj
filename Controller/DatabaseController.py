import sqlite3
from Model import DatabaseClass, DatabaseClass

# connect to the database called example.db
conn = sqlite3.connect('Model/Cylinder.db')
cylinderCursor = conn.cursor()
ingredientCursor = conn.cursor()

# function that inserts new ingredients
def update_cylinders():
    # clear the cylinder array
    DatabaseClass.cylinderArray.clear()

    cylinderCursor.execute("SELECT cylinderID, ingredient, amount FROM Cylinder")
    result = cylinderCursor.fetchall()

    for i in result:
        DatabaseClass.cylinderArray.append(DatabaseClass.Cylinder(i[0], i[1], i[2]))


def get_cylinder(cylinder_id):
    for i in DatabaseClass.cylinderArray:
        if i.cylinderID == cylinder_id:
            return i

def update_ingredients():
    # clear the ingredient array
    DatabaseClass.ingredientArray.clear()

    ingredientCursor.execute("SELECT * FROM Ingredients")
    result = ingredientCursor.fetchall()

    for i in result:
        DatabaseClass.ingredientArray.append(DatabaseClass.Ingredient(i[0], i[1]))


def database_close():
    conn.close()
