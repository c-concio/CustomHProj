import sqlite3

from Controller import AdminMainScreenController
from Model import DatabaseClass, DatabaseClass, AdminModel


# function that inserts new ingredients
def update_cylinders():
    # clear the cylinder array
    DatabaseClass.cylinderArray.clear()

    DatabaseClass.cursor.execute("SELECT id, ingredient, amount FROM cylinder")
    result = DatabaseClass.cursor.fetchall()

    for i in result:
        DatabaseClass.cylinderArray.append(DatabaseClass.Cylinder(i[0], i[1], i[2]))


def get_cylinder(cylinder_id):
    for i in DatabaseClass.cylinderArray:
        if i.cylinderID == cylinder_id:
            return i


def update_ingredients():
    # clear the ingredient array
    DatabaseClass.ingredientArray.clear()

    DatabaseClass.cursor.execute("SELECT * FROM ingredient")
    result = DatabaseClass.cursor.fetchall()

    for i in result:
        DatabaseClass.ingredientArray.append(DatabaseClass.Ingredient(i[0], i[1]))


def database_close():
    DatabaseClass.conn.close()

# delete the ingredient selected
def delete_ingredient(ingredient):
    DatabaseClass.cursor.execute('DELETE FROM ingredient WHERE IngredientType =?', [ingredient])
    DatabaseClass.cursor.execute("UPDATE cylinder SET ingredient = 'None' WHERE ingredient =?", [ingredient])
    DatabaseClass.conn.commit()
    # refresh page and popup
    AdminModel.inventoryScreen.grid.clear_widgets()
    AdminMainScreenController.setup_inventory_screen()
    AdminMainScreenController.refresh_popup()

#
def edit_ingredient():
    pass


def add_ingredient(new_ingredient):
    DatabaseClass.cursor.execute("INSERT INTO ingredient(IngredientType) VALUES (?)", (new_ingredient,))
    DatabaseClass.conn.commit()
    AdminMainScreenController.refresh_popup()
    # refresh page and popup
    AdminModel.inventoryScreen.grid.clear_widgets()
    AdminMainScreenController.setup_inventory_screen()
    AdminMainScreenController.refresh_popup()
