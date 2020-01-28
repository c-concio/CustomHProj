import sqlite3

import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from Controller import DatabaseController
from Model import AdminModel, DatabaseClass
from kivy.uix.screenmanager import Screen


# -------------------------------------------------------------------
#                       Screen Functions
# -------------------------------------------------------------------

# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    AdminModel.screenManager.transition.direction = 'left'
    AdminModel.screenManager.current = screen_name
    return


def return_screen(screen_name):
    AdminModel.screenManager.transition.direction = 'right'
    AdminModel.screenManager.current = screen_name


# function that powers off application
def quit_application():
    raise SystemExit


# Button switches to the
def initialize_buttons():
    AdminModel.adminMainScreen.inventoryButton.bind(on_press=lambda x: switch_screen('Inventory Screen'))
    AdminModel.adminMainScreen.internetButton.bind(on_press=lambda x: switch_screen('Internet Settings Screen'))
    AdminModel.adminMainScreen.powerButton.bind(on_press=quit_application)
    AdminModel.inventoryScreen.backButton.bind(on_press=lambda x: return_screen('Admin Main Screen'))
    # initialize the inventory button to open up the list of inventories and allow users to change or add inventory items
    AdminModel.inventoryScreen.editIngredientButton.bind(on_press=lambda x: open_popup())


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
    qConn = DatabaseClass.cursor
    qConn.execute("UPDATE Cylinder SET ingredient = ? WHERE cylinderID = ?", (text, spinner.parent.cylinderID))
    DatabaseClass.conn.commit()


# open popup window and show ingredient items
def open_popup():
    popup = Popup(title='Ingredients', size_hint=(None, None), size=(400, 400))
    ingredient_list_scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
    DatabaseController.update_ingredients()
    gridLayout = GridLayout(cols=1, size_hint_y=None, height=len(DatabaseClass.ingredientArray) * 50)
    DatabaseController.update_ingredients()
    for i in DatabaseClass.ingredientArray:
        template = AdminModel.InventoryPopupButtonLayout()
        template.ingredientButton.text = i.ingredientType
        bind_ingredient_button(template.ingredientButton)
        bind_delete_button(template.deleteButton, i.ingredientType)
        gridLayout.add_widget(template)
    ingredient_list_scroll_view.add_widget(gridLayout)
    AdminModel.popup.content = ingredient_list_scroll_view
    AdminModel.popup.open()


def refresh_popup():
    ingredient_list_scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
    DatabaseController.update_ingredients()
    gridLayout = GridLayout(cols=1, size_hint_y=None, height=len(DatabaseClass.ingredientArray) * 50)
    DatabaseController.update_ingredients()
    for i in DatabaseClass.ingredientArray:
        template = AdminModel.InventoryPopupButtonLayout()
        template.ingredientButton.text = i.ingredientType
        bind_ingredient_button(template.ingredientButton)
        bind_delete_button(template.deleteButton, i.ingredientType)
        gridLayout.add_widget(template)
    ingredient_list_scroll_view.add_widget(gridLayout)
    AdminModel.popup.content = ingredient_list_scroll_view


def bind_delete_button(button, ingredient):
    button.bind(on_press=lambda x: DatabaseController.delete_ingredient(ingredient))


def bind_ingredient_button(button):
    button.bind(on_press=lambda x: DatabaseController.edit_ingredient())
