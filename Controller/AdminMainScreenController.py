import sqlite3

import kivy
from kivy.core.window import Window
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
    AdminModel.inventoryScreen.editIngredientButton.bind(on_press=lambda x: open_ingredient_popup())
    AdminModel.inventoryScreen.sortToggleButton.bind(on_press=sort_cylinder_inventory)


def initialize_admin_buttons():
    AdminModel.adminMainScreen.inventoryButton.bind(on_press=lambda x: switch_screen('Inventory Screen'))
    AdminModel.adminMainScreen.powerButton.bind(on_press=quit_application)
    AdminModel.inventoryScreen.backButton.bind(on_press=lambda x: return_screen('Admin Main Screen'))
    AdminModel.adminMainScreen.returnMainScreen.bind(on_press=lambda x: switch_screen("User Main Screen"))

def switch_screen(screen_name):
    MainModel.mainScreenManager.transition.direction = 'left'
    MainModel.mainScreenManager.current = screen_name


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
    set_ingredient_list(inventory_item_template.ingredientSpinner, cylinder_item.cylinderType)
    inventory_item_template.ingredientSpinner.bind(text=update_ingredient_choice)

    # setup the percent label
    if cylinder_item.cylinderType == "base":
        inventory_item_template.percentLabel.text = str(int(cylinder_item.amount))
        inventory_item_template.progressBar.value = ((cylinder_item.amount / 4000) * 100)

    elif cylinder_item.cylinderType == "flavor":
        inventory_item_template.percentLabel.text = str(int(cylinder_item.amount))
        inventory_item_template.progressBar.value = ((cylinder_item.amount / 100) * 100)

    # bind the reset button to change the label text and rebind on press
    inventory_item_template.resetButton.bind(on_press=lambda x: open_reset_motor_popup(cylinder_item.cylinderID, cylinder_item.cylinderType))

    AdminModel.inventoryScreen.grid.add_widget(inventory_item_template)


# get the ingredient choices from the database and set it on the spinner values
def set_ingredient_list(spinner, cylinderType):
    ingredientArray = []
    for i in DatabaseClass.ingredientArray:
        if i.ingredientType == cylinderType:
            ingredientArray.append(i.ingredient)

    spinner.values = ingredientArray


# update the ingredient choice for a cylinder
def update_ingredient_choice(spinner, text):
    # get the spinner's parent's cylinder ID and update ingredient choice
    cursor = DatabaseClass.conn.cursor()
    cursor.execute("UPDATE cylinder SET ingredient = ? WHERE id = ?", (text, spinner.parent.cylinderID))
    DatabaseClass.conn.commit()


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


# -------------------------------------------------------------------
#                       Popup Screen Functions
# -------------------------------------------------------------------

# open popup window and show ingredient items
def open_ingredient_popup():
    AdminModel.ingredientPopup = Popup(title='Ingredients', size_hint=(None, None),
                                       size=(Window.width * 0.7, Window.height * 0.7))
    ingredient_list_scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
    DatabaseController.update_ingredients()
    gridLayout = GridLayout(cols=1, size_hint_y=None, height=len(DatabaseClass.ingredientArray) * 50 + 40, spacing=10)
    DatabaseController.update_ingredients()

    for i in DatabaseClass.ingredientArray:
        template = AdminModel.InventoryPopupButtonLayout(i.ingredientID, i.ingredientType)
        template.ingredientButton.text = i.ingredient
        bind_ingredient_button(template.ingredientButton)
        bind_delete_button(template.deleteButton, i.ingredient)
        if i.ingredientType == "base":
            template.ingredientButton.background_color = (0.8, 0.3, 0.3, 1)
        elif i.ingredientType == "flavor":
            template.ingredientButton.background_color = (0.5, 0.5, 1, 0.8)
        gridLayout.add_widget(template)

    add_ingredient_button = Button(text='Add Ingredient Type', size_hint_y=None, height=40)
    add_ingredient_button.bind(on_press=lambda x: add_text_field(add_ingredient_button, gridLayout))
    gridLayout.add_widget(add_ingredient_button)
    # add_text_field(add_ingredient_button, gridLayout)

    ingredient_list_scroll_view.add_widget(gridLayout)
    AdminModel.ingredientPopup.content = ingredient_list_scroll_view
    AdminModel.ingredientPopup.open()


def open_add_confirmation_popup(new_ingredient):
    AdminModel.addConfirmationPopup = Popup(title_align="center", title_size=22, size_hint=(None, None),
                                            size=(Window.width * 0.6, 125))

    AdminModel.addConfirmationPopup.title = "Add " + new_ingredient + "?"
    addInventoryLayout = AdminModel.AddInventoryPopupLayout()

    addInventoryLayout.confirmButton.bind(on_press=lambda x: DatabaseController.add_ingredient(new_ingredient))
    addInventoryLayout.declineButton.bind(on_press=lambda x: dismiss_add_confirmation_popup())

    AdminModel.addConfirmationPopup.content = addInventoryLayout
    AdminModel.addConfirmationPopup.open()


def dismiss_add_confirmation_popup():
    AdminModel.addConfirmationPopup.dismiss()
    AdminModel.text_input.text = ""


def dismiss_delete_confirmation_popup():
    AdminModel.deleteConfirmationPopup.dismiss()
    AdminModel.text_input.text = ""


def open_delete_confirmation_popup(ingredient):
    AdminModel.deleteConfirmationPopup = Popup(title_align="center", title_size=22, size_hint=(None, None),
                                               size=(Window.width * 0.6, 125))

    AdminModel.deleteConfirmationPopup.title = "Delete " + ingredient + "?"
    addInventoryLayout = AdminModel.AddInventoryPopupLayout()

    addInventoryLayout.confirmButton.bind(on_press=lambda x: DatabaseController.delete_ingredient(ingredient))
    addInventoryLayout.declineButton.bind(on_press=lambda x: dismiss_delete_confirmation_popup())

    AdminModel.deleteConfirmationPopup.content = addInventoryLayout
    AdminModel.deleteConfirmationPopup.open()


def add_text_field(addInventoryButton, gridLayout):
    AdminModel.text_input = TextInput(pos=addInventoryButton.pos, size=addInventoryButton.size)
    AdminModel.text_input.multiline = False
    AdminModel.text_input.bind(on_text_validate=lambda x: open_add_confirmation_popup(AdminModel.text_input.text))
    gridLayout.height = len(DatabaseClass.ingredientArray) * 50 + 90
    gridLayout.add_widget(AdminModel.text_input)
    # disable the button
    addInventoryButton.disabled = True


def refresh_ingredient_popup():
    ingredient_list_scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
    DatabaseController.update_ingredients()
    gridLayout = GridLayout(cols=1, size_hint_y=None, height=len(DatabaseClass.ingredientArray) * 50 + 40, spacing=10)
    DatabaseController.update_ingredients()
    for i in DatabaseClass.ingredientArray:
        template = AdminModel.InventoryPopupButtonLayout(i.ingredientID, i.ingredientType)
        template.ingredientButton.text = i.ingredient
        bind_ingredient_button(template.ingredientButton)
        bind_delete_button(template.deleteButton, i.ingredient)
        if i.ingredientType == "base":
            template.ingredientButton.background_color = (0.8, 0.3, 0.3, 1)
        elif i.ingredientType == "flavor":
            template.ingredientButton.background_color = (0.5, 0.5, 1, 0.8)
        gridLayout.add_widget(template)

    add_ingredient_button = Button(text='Add Ingredient Type', size_hint_y=None, height=40)
    add_ingredient_button.bind(on_press=lambda x: add_text_field(add_ingredient_button, gridLayout))
    gridLayout.add_widget(add_ingredient_button)
    # add_text_field(add_ingredient_button, gridLayout)

    ingredient_list_scroll_view.add_widget(gridLayout)
    AdminModel.ingredientPopup.content = ingredient_list_scroll_view


def bind_delete_button(button, ingredient):
    button.bind(on_press=lambda x: open_delete_confirmation_popup(ingredient))


def bind_ingredient_button(button):
    button.bind(on_press=lambda x: DatabaseController.change_ingredient_type(button))


# Popup for the reset motor function. Popup has up, down, and done button
def open_reset_motor_popup(cylinderID, cylinderType):
    # TODO: Reset motor all the way to the top of the cylinder

    AdminModel.resetMotorPopup = Popup(title='Ingredients', size_hint=(None, None),
                                       size=(Window.width * 0.7, Window.height * 0.7))
    AdminModel.resetMotorPopup.auto_dismiss = False
    AdminModel.resetMotorPopup.title = ""
    AdminModel.resetMotorPopup.separator_height = 0

    # add a ResetMotorPopupLayout to the popup
    resetMotorPopupLayout = AdminModel.ResetMotorPopupLayout()
    bind_reset_motor_buttons(resetMotorPopupLayout.upButton, resetMotorPopupLayout.pauseButton,
                             resetMotorPopupLayout.downButton, resetMotorPopupLayout.doneButton, cylinderID, cylinderType)

    AdminModel.resetMotorPopup.content = resetMotorPopupLayout

    AdminModel.resetMotorPopup.open()


def bind_reset_motor_buttons(upButton, pauseButton, downButton, doneButton, cylinderID, cylinderType):
    upButton.bind(on_press=lambda x: move_motor_up(cylinderID, cylinderType))
    pauseButton.bind(on_press=lambda x: pause_motor(cylinderID))
    downButton.bind(on_press=lambda x: move_motor_down(cylinderID, cylinderType))
    doneButton.bind(on_press=lambda x: done_reset_motor(cylinderID))


def done_reset_motor(cylinderID):
    AdminModel.resetMotorPopup.dismiss()
    pause_motor(cylinderID)
    setup_inventory_screen()


def move_motor_up(cylinderID, cylinderType):
    AdminModel.threadLock.acquire()
    AdminModel.moveMotorUp = True
    AdminModel.moveMotorDown = False
    AdminModel.threadLock.release()

    AdminModel.activeThread = AdminModel.MotorUpThread(cylinderID, cylinderType)
    AdminModel.activeThread.start()


def move_motor_down(cylinderID, cylinderType):
    AdminModel.threadLock.acquire()
    AdminModel.moveMotorUp = False
    AdminModel.moveMotorDown = True
    AdminModel.threadLock.release()

    AdminModel.activeThread = AdminModel.MotorDownThread(cylinderID, cylinderType)
    AdminModel.activeThread.start()

    print("Down button")


def pause_motor(cylinderID):
    AdminModel.threadLock.acquire()
    AdminModel.moveMotorUp = False
    AdminModel.moveMotorDown = False
    AdminModel.threadLock.release()

    print("Pause Button")


def temporary_dissmiss_reset_popup():
    pause_motor()

    # TODO: move the motor up a bit

    print("Popup dissmissed")
