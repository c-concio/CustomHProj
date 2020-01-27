import sqlite3

import kivy
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput

from Controller import DatabaseController
from Model import AdminModel, DatabaseClass, MainModel
from kivy.uix.screenmanager import Screen


# -------------------------------------------------------------------
#                       Screen Functions
# -------------------------------------------------------------------

# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    MainModel.mainScreenManager.transition.direction = 'left'
    MainModel.mainScreenManager.current = screen_name
    return


def return_screen(screen_name):
    MainModel.mainScreenManager.transition.direction = 'right'
    MainModel.mainScreenManager.current = screen_name


# function that powers off application
def quit_application(self):
    raise SystemExit


# Button switches to the
def initialize_buttons():
    AdminModel.adminMainScreen.inventoryButton.bind(on_press=lambda x: switch_screen('Inventory Screen'))
    AdminModel.adminMainScreen.internetButton.bind(on_press=lambda x: switch_screen('Internet Settings Screen'))
    AdminModel.adminMainScreen.powerButton.bind(on_press=quit_application)
    AdminModel.inventoryScreen.backButton.bind(on_press=lambda x: return_screen('Admin Main Screen'))


# -------------------------------------------------------------------
#                       Inventory Screen Functions
# -------------------------------------------------------------------

# setup the inventory screen by getting cylinders from the database and adding an inventory item template for each
def setup_inventory_screen():
    # update all the cylinders from the database
    DatabaseController.update_cylinders()
    for cylinder_item in DatabaseClass.cylinderArray:
        add_inventory_template(cylinder_item)


# Add an inventory item into the screen
def add_inventory_template(cylinder_item):
    inventory_item_template = AdminModel.InventoryItemTemplate(cylinder_item.cylinderID)

    # assign cylinder name to label
    inventory_item_template.cylinderButton.text = 'Cylinder ' + str(cylinder_item.cylinderID)

    # assign chosen ingredient
    inventory_item_template.ingredientSpinner.text = cylinder_item.ingredient

    # setup the values for the ingredientSpinner and bind the function update_ingredient to it
    DatabaseController.update_ingredients()
    set_ingredient_list(inventory_item_template.ingredientSpinner)
    inventory_item_template.ingredientSpinner.bind(text=update_ingredient_choice)

    # setup the percent label
    inventory_item_template.percentLabel.text = str(cylinder_item.amount)
    inventory_item_template.progressBar.value = cylinder_item.amount

    AdminModel.inventoryScreen.grid.add_widget(inventory_item_template)


# get the ingredient choices from the database and set it on the spinner values
def set_ingredient_list(spinner):
    ingredientArray = []
    for i in DatabaseClass.ingredientArray:
        ingredientArray.append(i.ingredientType)
    spinner.values = ingredientArray


# update the ingredient choice for a cylinder
def update_ingredient_choice(spinner, text):
    # get the spinner's parent's cylinder ID and update ingredient choice
    qConn = DatabaseClass.queryCursor
    qConn.execute("UPDATE cylinder SET ingredient = ? WHERE id = ?", (text, spinner.parent.cylinderID))
    DatabaseClass.conn.commit()