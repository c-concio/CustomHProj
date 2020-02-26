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

def select_first_row_from_condition(ingredient):
    try:
        cursor = DatabaseClass.conn.cursor()

        cursor.execute("SELECT ID FROM(SELECT * FROM (SELECT *, "
                       "row_number() over (PARTITION BY ingredient ORDER BY steps DESC) as rownum "
                       "FROM cylinder"
                       ") cylinder "
                       "WHERE ingredient = ? AND steps > 10 AND rownum = 1);", (ingredient,))

        rows = cursor.fetchone()
        print("Fetched first row")

        cursor.close()

        for row in rows:
            # print(row)
            return row

    except sqlite3.Error as e:
        print("Failed to select first row", e)

    # finally:
    #     if (connect):
    #         connect.close()

def update_temporary_cylinder(ingredient):
    try:
        cursor = DatabaseClass.conn.cursor()

        cylinder_id = 0

        try:
            # select the cylinder id with ingredient name
            cylinder_id = select_first_row_from_condition(ingredient)
            print("Cylinder id", cylinder_id)

        except:
            print("No corresponding cylinder with this name")

        sql = "UPDATE temporary SET cylinder_id = ? WHERE ingredient = ?"
        cursor.execute(sql, (cylinder_id, ingredient))

        print("Updated single row to temporary table")
        # cursor.close()
    except sqlite3.Error as e:
        print("Failed to update temporary table. ", e)
    return cursor.lastrowid