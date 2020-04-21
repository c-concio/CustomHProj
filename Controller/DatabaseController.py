import sqlite3

from kivy.uix.label import Label

from Controller import AdminMainScreenController
from Model import DatabaseClass, DatabaseClass, AdminModel


# function that inserts new ingredients
def update_cylinders():
    # clear the cylinder array
    DatabaseClass.cylinderArray.clear()

    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT * FROM cylinder")
    result = cursor.fetchall()

    for i in result:
        DatabaseClass.cylinderArray.append(DatabaseClass.Cylinder(i[0], i[1], i[2], i[3]))

    cursor.close()


def get_cylinder(cylinder_id):
    for i in DatabaseClass.cylinderArray:
        if i.cylinderID == cylinder_id:
            return i


def update_ingredients():
    # clear the ingredient array
    DatabaseClass.ingredientArray.clear()

    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT * FROM ingredients")
    result = cursor.fetchall()

    for i in result:
        DatabaseClass.ingredientArray.append(DatabaseClass.Ingredient(i[0], i[1], i[2]))

    cursor.close()


def database_close():
    DatabaseClass.conn.close()


# delete the ingredient selected
def delete_ingredient(ingredient):
    cursor = DatabaseClass.conn.cursor()
    cursor.execute('DELETE FROM ingredients WHERE Ingredient =?', [ingredient])
    cursor.execute("UPDATE cylinder SET ingredient = 'None' WHERE ingredient =?", [ingredient])
    DatabaseClass.conn.commit()

    # refresh page and popup
    AdminModel.inventoryScreen.grid.clear_widgets()
    AdminMainScreenController.setup_inventory_screen()
    AdminMainScreenController.refresh_ingredient_popup()
    cursor.close()


def edit_ingredient():
    AdminModel.deleteConfirmationPopup.dismiss()


# if the button given if a base, change type to flavor and change the color as well
def change_ingredient_type(button):
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT Type, Ingredient FROM ingredients WHERE ID = {}".format(button.parent.parent.ingredientID))

    result = cursor.fetchall()
    if result[0][0] == "base":
        cursor.execute("UPDATE ingredients SET Type = 'flavor' Where ID = {}".format(button.parent.parent.ingredientID))
        button.background_color = (0.5, 0.5, 1, 0.8)
    elif result[0][0] == "flavor":
        cursor.execute("UPDATE ingredients SET Type = 'base' Where ID = {}".format(button.parent.parent.ingredientID))
        button.background_color = (0.8, 0.3, 0.3, 1)

    DatabaseClass.conn.commit()

    cursor.execute(
        "UPDATE cylinder SET ingredient = 'None' WHERE ingredient = '{}' AND type = '{}'".format(result[0][1],
                                                                                                 result[0][0]))
    DatabaseClass.conn.commit()

    # refresh page and popup
    AdminModel.inventoryScreen.grid.clear_widgets()
    AdminMainScreenController.setup_inventory_screen()
    AdminMainScreenController.refresh_ingredient_popup()

    cursor.close()


def add_ingredient(new_ingredient):
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("INSERT INTO ingredients(Ingredient) VALUES (?)", (new_ingredient,))
    DatabaseClass.conn.commit()
    AdminMainScreenController.refresh_ingredient_popup()
    # refresh page and popup
    AdminModel.inventoryScreen.grid.clear_widgets()
    AdminMainScreenController.setup_inventory_screen()
    AdminMainScreenController.refresh_ingredient_popup()
    cursor.close()
    AdminModel.addConfirmationPopup.dismiss()


def ascend_cylinders():
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT * FROM cylinder ORDER BY steps ASC")

    DatabaseClass.cylinderArray.clear()

    result = cursor.fetchall()

    for i in result:
        DatabaseClass.cylinderArray.append(DatabaseClass.Cylinder(i[0], i[1], i[2], i[3]))

    cursor.close()


# function to get order from temporary tabel
def getOrder():
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT ingredient FROM temporary")

    result = cursor.fetchall()
    from Model import UserModel

    UserModel.splitScreen.confirmScreen.confirmLayout.clear_widgets()

    for i in result:
        newLabel = Label(text=i[0], size_hint_y=0.2, size_hint_x=0.5)
        UserModel.splitScreen.confirmScreen.confirmLayout.add_widget(newLabel)

    cursor.close()


def update_steps_amount(id, amount):
    cursor = DatabaseClass.conn.cursor()
    sql = "UPDATE cylinder SET steps = {} WHERE id = {}".format(amount, id)

    cursor.execute(sql)

    DatabaseClass.conn.commit()
    cursor.close()


def select_first_row_from_condition(ingredient, steps):
    try:
        cursor = DatabaseClass.conn.cursor()

        cursor.execute("SELECT ID FROM(SELECT * FROM (SELECT *, "
                       "row_number() over (PARTITION BY ingredient ORDER BY steps DESC) as rownum "
                       "FROM cylinder"
                       ") cylinder "
                       "WHERE ingredient = ? AND steps > ? AND rownum = 1);", (ingredient, steps))

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


def update_temporary_cylinder(ingredient, steps):
    try:
        cursor = DatabaseClass.conn.cursor()

        cylinder_id = 0

        try:
            # select the cylinder id with ingredient name
            cylinder_id = select_first_row_from_condition(ingredient, steps)
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

    cursor.close()


def get_temporary_table():
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT * FROM temporary")

    result = cursor.fetchall()

    string = ""

    for i in result:
        string += str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "\n"

    cursor.close()

    return string


def get_cylinder_ingredients():
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT  ingredient FROM cylinder WHERE type = 'Base' OR type = 'base'")

    result = cursor.fetchall()

    string = "Bases\n"

    for i in result:
        string += str(i[0]) + "\n"

    cursor.execute("SELECT ingredient FROM cylinder WHERE type = 'Flavor' OR type = 'flavor'")

    result = cursor.fetchall()

    string += "Flavors\n"

    for i in result:
        string += str(i[0]) + "\n"

    cursor.close()

    return string


def add_temporary_recipe(baseArray, flavorArray):
    cursor = DatabaseClass.conn.cursor()
    sql = "INSERT INTO temporary (ingredient) VALUES ('{}')"


    for baseString in baseArray:
        cursor.execute(sql.format(baseString))

    print("committing")

    DatabaseClass.conn.commit()
    cursor.close()


def get_cylinder_type(cylinderId):
    cursor = DatabaseClass.conn.cursor()
    sql = "SELECT type FROM cylinder WHERE id = {}"

    cursor.execute(sql.format(cylinderId))

    DatabaseClass.conn.commit()

    result = cursor.fetchall()
    type = ""
    for i in result:
        type = i[0]

    cursor.close()

    return type


def clear_temporary_table():
    cursor = DatabaseClass.conn.cursor()
    sql = "DELETE FROM temporary"

    cursor.execute(sql)

    DatabaseClass.conn.commit()

    cursor.close()


def completeOrder():
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("SELECT * FROM temporary")

    results = cursor.fetchall()

    for result in results:
        cursor.execute("SELECT steps FROM cylinder WHERE id = " + str(result[1]))
        step = cursor.fetchall()
        string = "UPDATE cylinder SET steps = " + str(step[0][0]) + " - " + str(result[2]) + " WHERE id = " + str(result[1])
        print(string)
        cursor.execute(string)

    cursor.close()


def add_cylinder_steps(cylinderID, cylinderType, amountAdd, dbConn):
    cursor = dbConn.cursor()
    cursor.execute("SELECT steps FROM cylinder where id = " + str(cylinderID))
    currentSteps = cursor.fetchall()

    newSteps = currentSteps[0][0] + amountAdd

    if cylinderType == "base":
        if newSteps <= 4000:
            cursor.execute("UPDATE cylinder SET steps = " + str(newSteps) + " WHERE id = " + str(cylinderID))
            dbConn.commit()
    elif cylinderType == "flavor":
        if newSteps <= 100:
            cursor.execute("UPDATE cylinder SET steps = " + str(newSteps) + " WHERE id = " + str(cylinderID))
            dbConn.commit()

    cursor.close()


def sub_cylinder_steps(cylinderID, amountAdd, dbConn):
    cursor = dbConn.cursor()
    cursor.execute("SELECT steps FROM cylinder where id = " + str(cylinderID))
    currentSteps = cursor.fetchall()

    newSteps = currentSteps[0][0] - amountAdd

    if newSteps > 0:
        cursor.execute("UPDATE cylinder SET steps = " + str(newSteps) + " WHERE id = " + str(cylinderID))
        dbConn.commit()

    cursor.close()