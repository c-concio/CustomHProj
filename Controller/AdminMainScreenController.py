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
    set_ingredient_list(inventory_item_template)
    inventory_item_template.ingredientSpinner.bind(text=update_ingredient)

    # get the ingredient choices from Database

    # initialize inventory buttons
    # inventory_item_template.cylinderButton.bind(
    #    on_press=lambda x: add_text_input(inventory_item_template.cylinderButton))
    # inventory_item_template.ingredientButton.bind(on_press=lambda x: add_spinner(inventory_item_template.ingredientButton))

    # TODO: Update percent amount

    # TODO: ingredient button. When clicked, a drop down of possible ingredients will be shown and when chosen,
    #  will change the cylinder's ingredient

    inventoryScreen.grid.add_widget(inventory_item_template)


# update the ingredient choice in the database
def update_ingredient(spinner, text):
    pass


# get the ingredient choices from the database and set it on the spinner values
def set_ingredient_list(inventory_item_template):
    spinner = inventory_item_template.ingredientSpinner
    spinner.values = ('Ingredient 1', 'Ingredient 2', 'Ingredient 3')


def add_text_input(pressedButton):
    try:
        remove_text_input()
    except:
        pass

    AdminModel.pressedButton = pressedButton
    text_input = AdminModel.textInput

    # clear any prexious text in textInput and put it over the pressed button
    text_input.text = ''
    pressedButton.add_widget(text_input)

    text_input.size = text_input.parent.size
    text_input.pos = text_input.parent.pos
    text_input.bind(on_text_validate=on_enter)


def add_spinner(pressedButton):
    spinner = AdminModel.spinner
    spinner.text = 'Default Ingredient'
    spinner.values = ('Ingredient 1', 'Ingredient 2', 'Ingredient 3')
    spinner.size_hint = (None, None)
    spinner.size = pressedButton.size
    spinner.pos = pressedButton.pos
    pressedButton.add_widget(spinner)


def add_drop_down(pressedButton):
    dropDown = AdminModel.dropDown
    AdminModel.pressedButton = pressedButton

    dropDown = DropDown()
    dropDown.size = pressedButton.size
    dropDown.pos = pressedButton.pos

    # add buttons (options) for the different types of predefined ingredients
    for i in range(0, 5):
        tempButton = Button(text='Ingredient')

        tempButton.bind(on_release=lambda x: set_button_text(tempButton.text))
        dropDown.add_widget(tempButton)

    mainButton = Button(text='Ingredient', size_hint=(None, None))
    mainButton.bind(on_release=dropDown.open)
    mainButton.size = pressedButton.size
    mainButton.pos = pressedButton.pos

    pressedButton.add_widget(mainButton)


def set_button_text(text):
    AdminModel.pressedButton.text = text


def on_enter(instance):
    AdminModel.pressedButton.text = instance.text
    remove_text_input()


def remove_text_input():
    AdminModel.pressedButton.remove_widget(AdminModel.textInput)
