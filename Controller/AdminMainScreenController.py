import kivy
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput

from Model import AdminModel
from kivy.uix.screenmanager import Screen


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


# Add an inventory item into the screen
def add_inventory_template(inventoryScreen):
    inventory_item_template = AdminModel.InventoryItemTemplate(AdminModel.inventoryNumber)
    AdminModel.inventoryNumber += 1

    # setup the values for the ingredientSpinner and bind the function update_ingredient to it
    set_ingredient_list(inventory_item_template.ingredientSpinner)
    inventory_item_template.ingredientSpinner.bind(text=update_ingredient)

    # setup the percent label
    inventory_item_template.percentLabel.text = '50'
    update_cylinder_amount(inventory_item_template, 20)

    # TODO: Update percent amount

    inventoryScreen.grid.add_widget(inventory_item_template)


def update_cylinder_amount(inventory_item_template, sub_amount):
    inventory_item_template.percentLabel.text = str(float(inventory_item_template.percentLabel.text) - sub_amount)
    inventory_item_template.progressBar.value -= sub_amount


# update the ingredient choice in the database
def update_ingredient(spinner, text):
    pass


# get the ingredient choices from the database and set it on the spinner values
def set_ingredient_list(spinner):
    spinner.values = ('Ingredient 1', 'Ingredient 2', 'Ingredient 3')


def add_text_input(pressed_button):
    try:
        remove_text_input()
    except:
        pass

    AdminModel.pressedButton = pressed_button
    text_input = AdminModel.textInput

    # clear any prexious text in textInput and put it over the pressed button
    text_input.text = ''
    pressed_button.add_widget(text_input)

    text_input.size = text_input.parent.size
    text_input.pos = text_input.parent.pos
    text_input.bind(on_text_validate=on_enter)


def set_button_text(text):
    AdminModel.pressedButton.text = text


def on_enter(instance):
    AdminModel.pressedButton.text = instance.text
    remove_text_input()


def remove_text_input():
    AdminModel.pressedButton.remove_widget(AdminModel.textInput)
