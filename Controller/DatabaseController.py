import sqlite3
from Model import DatabaseClass, DatabaseClass


# function that inserts new ingredients
def update_cylinders():
    # clear the cylinder array
    DatabaseClass.cylinderArray.clear()

    DatabaseClass.cylinderCursor.execute("SELECT id, ingredient, amount FROM cylinder")
    result = DatabaseClass.cylinderCursor.fetchall()

    for i in result:
        DatabaseClass.cylinderArray.append(DatabaseClass.Cylinder(i[0], i[1], i[2]))


def get_cylinder(cylinder_id):
    for i in DatabaseClass.cylinderArray:
        if i.cylinderID == cylinder_id:
            return i


def update_ingredients():
    # clear the ingredient array
    DatabaseClass.ingredientArray.clear()

    DatabaseClass.ingredientCursor.execute("SELECT * FROM ingredient")
    result = DatabaseClass.ingredientCursor.fetchall()

    for i in result:
        DatabaseClass.ingredientArray.append(DatabaseClass.Ingredient(i[0], i[1]))


def database_close():
    DatabaseClass.conn.close()
