import sqlite3

from Controller import AdminMainScreenController
from Model import DatabaseClass, DatabaseClass, AdminModel


# function that inserts new ingredients
def update_cylinders():
    # clear the cylinder array
    DatabaseClass.cylinderArray.clear()

    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT id, ingredient, steps FROM cylinder")
    result = cursor.fetchall()

    for i in result:
        DatabaseClass.cylinderArray.append(DatabaseClass.Cylinder(i[0], i[1], i[2]))

    cursor.close()


def get_cylinder(cylinder_id):
    for i in DatabaseClass.cylinderArray:
        if i.cylinderID == cylinder_id:
            return i


def update_ingredients():
    # clear the ingredient array
    DatabaseClass.ingredientArray.clear()

    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT * FROM ingredient")
    result = cursor.fetchall()

    for i in result:
        DatabaseClass.ingredientArray.append(DatabaseClass.Ingredient(i[0], i[1]))

    cursor.close()


def database_close():
    DatabaseClass.conn.close()


# delete the ingredient selected
def delete_ingredient(ingredient):
    cursor = DatabaseClass.conn.cursor()
    cursor.execute('DELETE FROM ingredient WHERE IngredientType =?', [ingredient])
    cursor.execute("UPDATE cylinder SET ingredient = 'None' WHERE ingredient =?", [ingredient])
    DatabaseClass.conn.commit()

    # refresh page and popup
    AdminModel.inventoryScreen.grid.clear_widgets()
    AdminMainScreenController.setup_inventory_screen()
    AdminMainScreenController.refresh_popup()
    cursor.close()


#
def edit_ingredient():
    pass


def add_ingredient(new_ingredient):
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("INSERT INTO ingredient(IngredientType) VALUES (?)", (new_ingredient,))
    DatabaseClass.conn.commit()
    AdminMainScreenController.refresh_popup()
    # refresh page and popup
    AdminModel.inventoryScreen.grid.clear_widgets()
    AdminMainScreenController.setup_inventory_screen()
    AdminMainScreenController.refresh_popup()
    cursor.close()


def ascend_cylinders():
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT * FROM cylinder ORDER BY steps ASC")

    DatabaseClass.cylinderArray.clear()

    result = cursor.fetchall()

    for i in result:
        DatabaseClass.cylinderArray.append(DatabaseClass.Cylinder(i[0], i[1], i[3]))

    cursor.close()


def update_steps_amount(id, amount):
    cursor = DatabaseClass.conn.cursor()
    sql = "UPDATE cylinder SET steps = {} WHERE id = {}".format(amount, id)

    cursor.execute(sql)

    DatabaseClass.conn.commit()
    cursor.close()