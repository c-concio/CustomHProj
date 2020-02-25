import sqlite3

import kivy
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
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
def initialize_inventory_buttons():
    # initialize the inventory button to open up the list of inventories and allow users to change or add inventory items
    AdminModel.inventoryScreen.editIngredientButton.bind(on_press=lambda x: open_popup())
    AdminModel.inventoryScreen.sortToggleButton.bind(on_press=sort_cylinder_inventory)

def initialize_admin_buttons():
    AdminModel.adminMainScreen.inventoryButton.bind(on_press=lambda x: switch_screen('Inventory Screen'))
    AdminModel.adminMainScreen.powerButton.bind(on_press=quit_application)
    AdminModel.inventoryScreen.backButton.bind(on_press=lambda x: return_screen('Admin Main Screen'))

# -------------------------------------------------------------------
#                       Inventory Screen Functions
# -------------------------------------------------------------------

# setup the inventory screen by getting cylinders from the database and adding an inventory item template for each
def setup_inventory_screen():
    AdminModel.inventoryScreen.grid.clear_widgets()
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

    # bind the reset button to change the label text and rebind on press
    inventory_item_template.resetButton.bind(on_press=reset_cylinder)

    AdminModel.inventoryScreen.grid.add_widget(inventory_item_template)


def reset_cylinder(button):
    # set steps to 100
    DatabaseController.update_steps_amount(button.parent.cylinderID, 0)
    newButton = refresh_inventory_button(button.parent.cylinderID)

    # change text to "set up"
    newButton.text = 'Set up'

    # rebind button to reset the motor and change button to reset button
    newButton.bind(on_press=set_up_cylinder)
    newButton.unbind(on_press=reset_cylinder)


def set_up_cylinder(button):
    # set steps to 100
    DatabaseController.update_steps_amount(button.parent.cylinderID, 100)
    newButton = refresh_inventory_button(button.parent.cylinderID)

    # change button to reset and rebind back to set up when pressed
    newButton.text = 'Reset'

    newButton.bind(on_press=reset_cylinder)
    newButton.unbind(on_press=set_up_cylinder)

# get the ingredient choices from the database and set it on the spinner values
def set_ingredient_list(spinner):
    ingredientArray = []
    for i in DatabaseClass.ingredientArray:
        ingredientArray.append(i.ingredientType)
    spinner.values = ingredientArray


# update the ingredient choice for a cylinder
def update_ingredient_choice(spinner, text):
    # get the spinner's parent's cylinder ID and update ingredient choice
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("UPDATE cylinder SET ingredient = ? WHERE id = ?", (text, spinner.parent.cylinderID))
    DatabaseClass.conn.commit()


# open popup window and show ingredient items
def open_popup():
    popup = Popup(title='Ingredients', size_hint=(None, None), size=(400, 400))
    ingredient_list_scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
    DatabaseController.update_ingredients()
    gridLayout = GridLayout(cols=1, size_hint_y=None, height=len(DatabaseClass.ingredientArray) * 50 + 40, spacing=10)
    DatabaseController.update_ingredients()

    for i in DatabaseClass.ingredientArray:
        template = AdminModel.InventoryPopupButtonLayout()
        template.ingredientButton.text = i.ingredientType
        bind_ingredient_button(template.ingredientButton)
        bind_delete_button(template.deleteButton, i.ingredientType)
        gridLayout.add_widget(template)

    add_ingredient_button = Button(text='Add Ingredient Type', size_hint_y=None, height=40)
    add_ingredient_button.bind(on_press=lambda x: add_text_field(add_ingredient_button, gridLayout))
    gridLayout.add_widget(add_ingredient_button)
    # add_text_field(add_ingredient_button, gridLayout)

    ingredient_list_scroll_view.add_widget(gridLayout)
    AdminModel.popup.content = ingredient_list_scroll_view
    AdminModel.popup.open()


def add_text_field(addInventoryButton, gridLayout):
    AdminModel.text_input = TextInput(pos=addInventoryButton.pos, size=addInventoryButton.size)
    AdminModel.text_input.multiline = False
    AdminModel.text_input.bind(on_text_validate=lambda x: DatabaseController.add_ingredient(AdminModel.text_input.text))
    gridLayout.height = len(DatabaseClass.ingredientArray) * 50 + 90
    gridLayout.add_widget(AdminModel.text_input)
    # disable the button
    addInventoryButton.disabled = True


def refresh_popup():
    ingredient_list_scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
    DatabaseController.update_ingredients()
    gridLayout = GridLayout(cols=1, size_hint_y=None, height=len(DatabaseClass.ingredientArray) * 50 + 40, spacing=10)
    DatabaseController.update_ingredients()
    for i in DatabaseClass.ingredientArray:
        template = AdminModel.InventoryPopupButtonLayout()
        template.ingredientButton.text = i.ingredientType
        bind_ingredient_button(template.ingredientButton)
        bind_delete_button(template.deleteButton, i.ingredientType)
        gridLayout.add_widget(template)

    add_ingredient_button = Button(text='Add Ingredient Type', size_hint_y=None, height=40)
    add_ingredient_button.bind(on_press=lambda x: add_text_field(add_ingredient_button, gridLayout))
    gridLayout.add_widget(add_ingredient_button)
    # add_text_field(add_ingredient_button, gridLayout)

    ingredient_list_scroll_view.add_widget(gridLayout)
    AdminModel.popup.content = ingredient_list_scroll_view


def bind_delete_button(button, ingredient):
    button.bind(on_press=lambda x: DatabaseController.delete_ingredient(ingredient))


def bind_ingredient_button(button):
    button.bind(on_press=lambda x: DatabaseController.edit_ingredient())


def sort_cylinder_inventory(self):
    # update the cylinderArray

    DatabaseController.ascend_cylinders()
    AdminModel.inventoryScreen.grid.clear_widgets()

    for cylinder_item in DatabaseClass.cylinderArray:
        add_inventory_template(cylinder_item)
    self.unbind(on_press=sort_cylinder_inventory)
    self.bind(on_press=un_sort_cylinder_inventory)


def un_sort_cylinder_inventory(self):
    setup_inventory_screen()
    self.unbind(on_press=un_sort_cylinder_inventory)
    self.bind(on_press=sort_cylinder_inventory)

def refresh_inventory_button(cylinderID):
    AdminModel.inventoryScreen.grid.clear_widgets()

    DatabaseController.update_cylinders()

    for cylinder_item in DatabaseClass.cylinderArray:
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

        # bind the reset button to change the label text and rebind on press
        inventory_item_template.resetButton.bind(on_press=reset_cylinder)

        if (cylinder_item.cylinderID == cylinderID):
            button = inventory_item_template.resetButton


        AdminModel.inventoryScreen.grid.add_widget(inventory_item_template)

    return button
