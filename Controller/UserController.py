import re

import kivy
import pymysql
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase

import i2c
from Controller import DatabaseController
from Model import UserModel, DatabaseClass, MainModel
from Controller import MainScreenController

kivy.require('1.9.0')


# -------------------------------------------------------------------
#                       Screen Functions
# -------------------------------------------------------------------

# function takes in a screen and switches the screenManager to the passed screen
def switch_screen(screen_name):
    MainModel.mainScreenManager.transition.direction = 'left'
    MainModel.mainScreenManager.current = screen_name
    return


# def return_screen(screen_name):
#     UserModel.screenManager.transition.direction = 'right'
#     UserModel.screenManager.current = screen_name

def initialize_main_screen_buttons():
    UserModel.userMainScreen.startButton.bind(on_press=lambda x: MainScreenController.switch_screen('Split Screen'))
    UserModel.userMainScreen.qrButton.bind(on_press=lambda x: MainScreenController.switch_screen('QR Screen'))
    # UserModel.userMainScreen.startButton.bind(on_press=lambda x: print("Start button pressed"))


# Button switches to
def initialize_buttons():
    reset_temporary_table()
    # Step buttons
    UserModel.splitScreen.step1.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.sizeScreen))
    UserModel.splitScreen.step2.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.baseScreen))
    UserModel.splitScreen.step3.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.flavorScreen))
    UserModel.splitScreen.step4.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.amountScreen))
    UserModel.splitScreen.step5.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.confirmScreen))

    UserModel.splitScreen.confirmScreen.orderButton.bind(on_press=lambda x: orderFinish())

    UserModel.splitScreen.step4.bind(on_press=lambda x: buildAmountScreen(UserModel.splitScreen.amountScreen))

    # UserModel.userMainScreen.startButton.bind(on_press=lambda x: print("Start button pressed"))

    # Screen buttons
    UserModel.splitScreen.sizeScreen.nextButton.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.baseScreen))
    UserModel.splitScreen.baseScreen.nextButton.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.flavorScreen))
    UserModel.splitScreen.flavorScreen.nextButton.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.amountScreen))

    UserModel.splitScreen.sizeScreen.nextButton.bind(on_press=lambda x: enableStep2())
    UserModel.splitScreen.baseScreen.nextButton.bind(on_press=lambda x: enableStep3())
    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: enableStep4())
    #    UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: enableStep5())
    #    UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: loadOrder())

    # UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: i2c.run())
    # UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: print("I2C"))
    # UserModel.amountScreen.doneButton.bind(on_press=lambda x: switch_screen('Split Screen'))
    # UserModel.splitScreen.nextButton1.bind(on_press=lambda x: switch_screen('Base Screen'))
    # UserModel.amountScreen.addButton.bind(on_press=lambda x: switch_screen('Loading Screen'))

    UserModel.splitScreen.baseScreen.nextButton.bind(on_press=lambda x: getBaseList())


    # UserModel.splitScreen.baseScreen.sauceOfMonthButton.bind(on_press=lambda x: showPopupWindow())
    # UserModel.splitScreen.sizeScreen.nextButton.bind(
    #     on_press=lambda x: UserModel.SauceOfMonth.updateButtons(UserModel.SauceOfMonth()))


    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: getFlavorList())

    # TODO: uncomment
    # Trigger Amount screen properties
    UserModel.splitScreen.flavorScreen.nextButton.bind(
        on_press=lambda x: buildAmountScreen(UserModel.splitScreen.amountScreen))



# -------------------------------------------------------------------
#                       Carousel Functions
# -------------------------------------------------------------------
def initialize_carousel(split_screen):
    # add all the screens to the carousel
    split_screen.carouselWidget.add_widget(split_screen.sizeScreen)
    split_screen.carouselWidget.add_widget(split_screen.baseScreen)
    split_screen.carouselWidget.add_widget(split_screen.flavorScreen)
    split_screen.carouselWidget.add_widget(split_screen.amountScreen)
    split_screen.carouselWidget.add_widget(split_screen.confirmScreen)


def resetStepButtons():
    UserModel.splitScreen.step2.disabled = True
    UserModel.splitScreen.step3.disabled = True
    UserModel.splitScreen.step4.disabled = True
    UserModel.splitScreen.step5.disabled = True


# -------------------------------------------------------------------
#                       Size Screen Functions
# -------------------------------------------------------------------
def resetSizeScreen():
    UserModel.splitScreen.sizeScreen.sizeList = []
    UserModel.splitScreen.sizeScreen.toggleButtonSmall.state = 'normal'
    UserModel.splitScreen.sizeScreen.toggleButtonMedium.state = 'normal'
    UserModel.splitScreen.sizeScreen.toggleButtonLarge.state = 'normal'
    UserModel.splitScreen.sizeScreen.nextButton.disabled = True
    UserModel.splitScreen.sizeScreen.nextButton.colour = (0, 0, 0, 0)


# -------------------------------------------------------------------
#                       Base Screen Functions
# -------------------------------------------------------------------

# get the list of bases selected by user
def getBaseList():
    connect = DatabaseClass.conn
    cursor = connect.cursor()

    for base in UserModel.splitScreen.baseScreen.baseList:
        cursor.execute("INSERT INTO temporary(ingredient) VALUES(?);", (base,))
        connect.commit()

        print("Added " + base + " to Temporary table")
    cursor.close()



def resetBaseScreen():
    # Clear the buttons from the grid
    UserModel.splitScreen.baseScreen.grid.clear_widgets()
    # Reset to normal state for all buttons
    for button in UserModel.splitScreen.baseScreen.baseToggleList:
        button.state = 'normal'
        button.disabled = False
    # Reset lists and re-add all buttons (to list and screen)
    UserModel.splitScreen.baseScreen.createButtons()

    UserModel.splitScreen.baseScreen.nextButton.disabled = True
    UserModel.splitScreen.baseScreen.nextButton.colour = (0, 0, 0, 0)


# -------------------------------------------------------------------
#                       Sauce of the Month Functions
# -------------------------------------------------------------------

# Popup window of sauce of the month
def showPopupWindow():
    show = UserModel.SauceOfMonth()
    popupWindow = Popup(title="", separator_height=0, size_hint=(None, None), size=(600, 600), content=show,
                        auto_dismiss=True
                        # , pos_hint={'x': 5.0 / Window.width, 'y': 5.0 / Window.height}
                        )

    # Done button dismisses popup
    show.doneButton.bind(on_press=lambda x: popupWindow.dismiss())
    # Jump to base screen when sauce is chosen
    show.doneButton.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.baseScreen))
    # Enable base step
    show.doneButton.bind(on_press=lambda x: enableStep3())
    # Enable flavor step
    show.doneButton.bind(on_press=lambda x: enableStep4())
    # Selects the buttons for base screen
    show.doneButton.bind(on_press=lambda x: select_base_toggle_buttons())
    # Selects the buttons for flavor screen
    show.doneButton.bind(on_press=lambda x: select_flavor_toggle_buttons())
    popupWindow.open()

def select_base_toggle_buttons():
    sauceOfMonth = UserModel.SauceOfMonth()
    baseScreen = UserModel.splitScreen.baseScreen

    for ingredient in sauceOfMonth.sauceList:
        ingredient = re.sub("\\s+", ",", ingredient.strip())
        values = ingredient.split(',')
        for baseToggle in baseScreen.baseToggleList:
            for value in values:
                if value == baseToggle.text:
                    baseToggle.state = "down"
                    baseScreen.baseList.append(baseToggle.text)

        if len(baseScreen.baseList) < 1:
            baseScreen.nextButton.disabled = True
            baseScreen.nextButton.text = ""
            baseScreen.nextButton.colour = (1, 1, 1, 0)
        else:
            baseScreen.nextButton.disabled = False
            baseScreen.nextButton.text = "Next"
            baseScreen.nextButton.colour = (1, 1, 1, 0.6)

        # Disable other buttons when 2 bases are chosen
        if len(baseScreen.baseList) >= 2:
            for button in baseScreen.baseToggleList:
                if button.text not in baseScreen.baseList:
                    button.disabled = True
                    # print("This button disabled: " + button.text)
        else:
            for button in baseScreen.baseToggleList:
                if button.text not in baseScreen.baseList:
                    button.disabled = False
                    # print("This button recovered: " + button.text)

def select_flavor_toggle_buttons():
    sauceOfMonth = UserModel.SauceOfMonth()
    flavorScreen = UserModel.splitScreen.flavorScreen

    for ingredient in sauceOfMonth.sauceList:
        ingredient = re.sub("\\s+", ",", ingredient.strip())
        values = ingredient.split(',')
        for flavorToggle in flavorScreen.flavorToggleList:
            for value in values:
                if value == flavorToggle.text:
                    flavorToggle.state = "down"
                    flavorScreen.flavorList.append(flavorToggle.text)

        # Disable other buttons when 3 flavors are chosen
        if len(flavorScreen.flavorList) >= 3:
            for button in flavorScreen.baseToggleList:
                if button.text not in flavorScreen.flavorList:
                    button.disabled = True
                    # print("This button disabled: " + button.text)
        else:
            for button in flavorScreen.flavorToggleList:
                if button.text not in flavorScreen.flavorList:
                    button.disabled = False
                    # print("This button recovered: " + button.text)


# TODO add another function for done button --> bind it to amount page

# -------------------------------------------------------------------
#                       Flavor Screen Functions
# -------------------------------------------------------------------

def getFlavorList():
    connect = DatabaseClass.conn
    cursor = connect.cursor()

    for flavor in UserModel.splitScreen.flavorScreen.flavorList:
        cursor.execute("INSERT INTO temporary(ingredient) VALUES(?);", (flavor,))
        connect.commit()

        print("Added " + flavor + " to Temporary table")
    cursor.close()


def resetFlavorScreen():
    # Clear the buttons from the grid
    UserModel.splitScreen.flavorScreen.grid.clear_widgets()
    # Reset to normal state for all buttons
    for button in UserModel.splitScreen.flavorScreen.flavorToggleList:
        button.state = 'normal'
        button.disabled = False
    # Reset lists and re-add all buttons (to list and screen)
    UserModel.splitScreen.flavorScreen.createButtons()


# setup the flavor screen by getting cylinders(flavor) from the database


# -------------------------------------------------------------------
#                       Amount Screen Functions
# -------------------------------------------------------------------


def increment(label_text):
    amount = int(label_text.text)
    if amount < 10:
        amount += 1
    label_text.text = str(amount)


def decrement(label_text):
    amount = int(label_text.text)
    if amount > 0:
        amount -= 1
    label_text.text = str(amount)


def enableStep2():
    UserModel.splitScreen.step2.disabled = False


def enableStep3():
    UserModel.splitScreen.step3.disabled = False


def enableStep4():
    UserModel.splitScreen.step4.disabled = False


def enableStep5():
    UserModel.splitScreen.step5.disabled = False


def amountScreenDone():
    baseList = UserModel.splitScreen.baseScreen.baseList
    sizeList = UserModel.splitScreen.sizeScreen.sizeList
    # Update temporary table
    connect = DatabaseClass.conn
    cursor = connect.cursor()

    # Update flavors in temporary table
    for i, flavor in enumerate(UserModel.splitScreen.amountScreen.flavorLayoutList):
        cursor.execute("UPDATE temporary "
                       "SET ml = ?"
                       "WHERE ingredient = ?",
                       (flavor.label_text.text,
                        UserModel.splitScreen.amountScreen.flavorLayoutList[i].flavorName.text))
    # Update flavor cylinder_id in temporary table
    for flavor in UserModel.splitScreen.flavorScreen.flavorList:
        DatabaseController.update_temporary_cylinder(flavor, 10)


    # When 1 base is chosen
    if len(baseList) == 1:
        print("1 Base")
        if len(sizeList) != 0:
            if sizeList[0] == "SMALL":
                cursor.execute("UPDATE temporary "
                               "SET ml = ?"
                               "WHERE ingredient = ?",
                               (10, baseList[0]))

                print(baseList[0])
            elif sizeList[0] == "MEDIUM":
                cursor.execute("UPDATE temporary "
                               "SET ml = ?"
                               "WHERE ingredient = ?",
                               (50, baseList[0]))
            elif sizeList[0] == "LARGE":
                cursor.execute("UPDATE temporary "
                               "SET ml = ?"
                               "WHERE ingredient = ?",
                               (100, baseList[0]))
    # When 2 bases are chosen
    elif len(baseList) == 2:
        sliderValue = UserModel.splitScreen.amountScreen.slider.value
        baseProportionList = [sliderValue, 360 - sliderValue]
        if len(sizeList) != 0:
            if sizeList[0] == "SMALL":
                for i, base in enumerate(baseList):
                    cursor.execute("UPDATE temporary "
                                   "SET ml = ?"
                                   "WHERE ingredient = ?",
                                   (baseProportionList[i] * 10 / 360, baseList[i]))
                    print(baseProportionList[i] * 10 / 360)
                    print(baseList[i])
                # Update base cylinder_id
                for base in UserModel.splitScreen.baseScreen.baseList:
                        DatabaseController.update_temporary_cylinder(base, 10)

            elif sizeList[0] == "MEDIUM":
                for i, base in enumerate(baseList):
                    cursor.execute("UPDATE temporary "
                                   "SET ml = ?"
                                   "WHERE ingredient = ?",
                                   (baseProportionList[i] * 50 / 360, baseList[i]))
                    print(baseProportionList[i] * 50 / 360)
                    print(baseList[i])
                # Update base cylinder_id
                for base in UserModel.splitScreen.baseScreen.baseList:
                        DatabaseController.update_temporary_cylinder(base, 50)

            elif sizeList[0] == "LARGE":
                for i, base in enumerate(baseList):
                    cursor.execute("UPDATE temporary "
                                   "SET ml = ?"
                                   "WHERE ingredient = ?",
                                   (baseProportionList[i] * 100 / 360, baseList[i]))
                    print(baseProportionList[i] * 100 / 360)
                    print(baseList[i])
                # Update base cylinder_id
                for base in UserModel.splitScreen.baseScreen.baseList:
                        DatabaseController.update_temporary_cylinder(base, 100)


    connect.commit()
    cursor.close()


def orderFinish():
    # open the loading popup
    UserModel.popup.open()

    # Deselect all previous options
    resetStepButtons()
    resetSizeScreen()
    resetBaseScreen()
    resetFlavorScreen()
    # # Push data to online database
    # updateOnlineDatabase()
    # # Pull data from online database
    # getOnlineDatabase()
    # Reset temporary table
    switch_screen(screen_name="User Main Screen")

    # change all the changes onto the database
    DatabaseController.completeOrder()

    reset_temporary_table()

    UserModel.popup.dismiss()


def buildAmountScreen(amountScreen):
    amountScreen.scroll.clear_widgets()
    if Window.width < 770:
        if not amountScreen.built:
            button = UserModel.DoneRoundedButton1()
            button.bind(on_press=lambda x: amountScreenDone())
            button.bind(on_press=lambda x: enableStep5())
            button.bind(on_press=lambda x: DatabaseController.getOrder())
            button.bind(
                on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.confirmScreen))
            amountScreen.box.add_widget(button)
        buildAmountScreenGridLayout(amountScreen)
    else:
        if not amountScreen.built:
            button = UserModel.DoneRoundedButton2()
            button.bind(on_press=lambda x: amountScreenDone())
            button.bind(on_press=lambda x: enableStep5())
            button.bind(on_press=lambda x: DatabaseController.getOrder())
            button.bind(
                on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.confirmScreen))

            amountScreen.add_widget(button)
        buildAmountScreenStackLayout(amountScreen)

    amountScreen.built = True


def buildAmountScreenGridLayout(amountScreen):
    # add grid layout into the scroll view

    grid = UserModel.AmountGridLayout()

    # check the base array in the UserModel and add corresponding layout to grid
    # TODO: replace baselist with actual baselist
    baseList = UserModel.splitScreen.baseScreen.baseList
    flavorList = UserModel.splitScreen.flavorScreen.flavorList
    flavorLayoutList = UserModel.splitScreen.amountScreen.flavorLayoutList

    # if there is only one base selected, then the layout should only have one base, no slider, and show the full pie
    if len(baseList) == 1:
        baseTemplate = UserModel.BaseGridTemplate1()
        baseTemplate.baseLabel1.text = baseList[0]
        grid.add_widget(baseTemplate)
    else:
        # Bases
        baseTemplate = UserModel.BaseGridTemplate2()
        baseTemplate.baseLabel1.text = baseList[0]
        baseTemplate.baseLabel2.text = baseList[1]
        grid.add_widget(baseTemplate)
        amountScreen.slider = baseTemplate.slider

    # check how many flavors and add flavor templates
    for f in flavorList:
        flavorLayoutList.append(UserModel.FlavorsLayout(f))
        grid.add_widget(UserModel.FlavorsLayout(name=f))

    amountScreen.scroll.add_widget(grid)


def buildAmountScreenStackLayout(amountScreen):
    amountScreen.scroll.clear_widgets()

    # TODO: replace baselist with actual baselist
    baseList = UserModel.splitScreen.baseScreen.baseList
    flavorList = UserModel.splitScreen.flavorScreen.flavorList
    flavorLayoutList = UserModel.splitScreen.amountScreen.flavorLayoutList

    # variable to count the total height of all the elements in layout
    totalHeight = 20
    space = 10
    padding = 10

    grid = UserModel.AmountGridLayout()
    stack = StackLayout(orientation="tb-lr", padding=[padding], spacing=space)
    stack.size_hint_y = None

    # if there is only one base selected, then the layout should only have one base, no slider, and show the full pie
    if len(baseList) == 1:
        baseTemplate = UserModel.BaseStackTemplate1()
        #baseTemplate.baseLabel1.text = baseList[0]
        #baseTemplate.baseLabel1.width = Window.width * 0.5
        stack.add_widget(baseTemplate)
        baseLabel = Label(text=baseList[0], size_hint_x=None, width=Window.width * 0.5, height=50, size_hint_y=None)
        baseLabel.font_name = "Pacifico"
        baseLabel.font_size = "18sp"
        stack.add_widget(baseLabel)
        totalHeight += 50 + (2 * space)
    else:
        # Bases
        baseTemplate = UserModel.BaseStackTemplate2()
        baseTemplate.width = Window.width * 0.5
        baseTemplate.baseLabel1.text = baseList[0]
        baseTemplate.baseLabel2.text = baseList[1]
        stack.add_widget(baseTemplate)
        totalHeight += 50 + 75 + 70 + (2 * space)
        amountScreen.slider = baseTemplate.slider

    # check how many flavors and add flavor templates
    for f in flavorList:
        flavor = UserModel.FlavorsLayout(name=f)
        flavor.size_hint_x = None
        flavor.width = Window.width * 0.5
        stack.add_widget(flavor)
        totalHeight += flavor.height + (2 * space)
        flavorLayoutList.append(flavor)

    pieChart = UserModel.AmountPieChart()
    pieChart.width = (Window.width * 0.5) - (5 * padding)

    if len(baseList) == 1:
        pieChart.pie_chart_value = 360
    else:
        pieChart.pie_chart_value = baseTemplate.slider.value
        baseTemplate.pie = pieChart
        baseTemplate.slider.bind(value=updatePie)

    stack.add_widget(pieChart)

    stack.height = totalHeight

    grid.add_widget(stack)

    amountScreen.scroll.add_widget(grid)
    pass


def updatePie(instance, value):
    instance.parent.pie.pie_chart_value = instance.value


def updateOnlineDatabase():
    sameRecipe = False
    countCheck = 0
    id = 0
    # Get ingredients from temporary table
    local_conn = DatabaseClass.conn
    local_cursor = local_conn.cursor()
    sqlBase = "SELECT ingredient FROM temporary;"
    local_cursor.execute(sqlBase)
    bases = local_cursor.fetchall()
    sqlFlavor = "SELECT ingredient FROM temporary;"
    local_cursor.execute(sqlFlavor)
    flavors = local_cursor.fetchall()
    try:
        conn = pymysql.connect(host='127.0.0.1',
                               user='root',
                               password='customh',
                               db='cylinder')
        cursor = conn.cursor()

        # Create array of bases
        baseArray = [None] * 2
        for i, base in enumerate(bases):
            print(base[0])
            baseArray.pop(i)
            baseArray.insert(i, base[0])

        print("Base Array: ")
        print(baseArray)

        # Create array of flavors
        flavorArray = [None] * 3
        for i, flavor in enumerate(flavors):
            print(base[0])
            flavorArray.pop(i)
            flavorArray.insert(i, flavor[0])

        print("Flavor Array: ")
        print(flavorArray)

        ingredientArray = baseArray + flavorArray
        print(ingredientArray)
        checkSQL = "SELECT * FROM online;"
        cursor.execute(checkSQL)
        checkIngredients = cursor.fetchall()

        # Check if this recipe exists (5 ingredients)
        for checkIngredient in checkIngredients:
            countCheck = 0
            for i in range(1, 6):
                if checkIngredient[i] == ingredientArray[i - 1]:
                    countCheck += 1
                    # If all 5 match, get the id
                    if countCheck == 5:
                        id = checkIngredient[0]
                        sameRecipe = True
                        continue

        # If same recipe, update the count
        if sameRecipe == True:
            print("In update")
            val = (ingredientArray[0], ingredientArray[1], ingredientArray[2], ingredientArray[3], ingredientArray[4])
            updateSQL = "UPDATE online SET count = count + 1 WHERE id = %s"
            sameRecipe = False
            cursor.execute(updateSQL, id)
            id = 0
            conn.commit()
        # If new recipe, insert new row
        else:
            print("In insert")
            # Put ordered ingredients to online database
            val = (
            ingredientArray[0], ingredientArray[1], ingredientArray[2], ingredientArray[3], ingredientArray[4], 1)
            insertSQL = "INSERT INTO online(ingredient1,ingredient2,ingredient3,ingredient4,ingredient5,count) VALUES(%s,%s,%s,%s,%s,%s);"
            cursor.execute(insertSQL, val)
            conn.commit()

        local_cursor.close()
        cursor.close()
    except:
        print("Proxy not setup, could not push temporary table to online database")


def getOnlineDatabase():
    try:
        conn = pymysql.connect(host='127.0.0.1',
                               user='root',
                               password='customh',
                               db='cylinder')

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM online;")

        rows = cursor.fetchall()
        print("Online database contains:")
        for row in rows:
            print(row)

        cursor.close()
    except:
        print("Proxy not setup, could not push temporary table to online database")


def reset_temporary_table():
    conn = DatabaseClass.conn
    cursor = conn.cursor()

    sql = "DELETE FROM temporary;"

    cursor.execute(sql)
    conn.commit()
    cursor.close()


# -------------------------------------------------------------------
#                       Amount Screen Functions
# -------------------------------------------------------------------

def header_font_size():
    fontSize = Window.width * 0.05
    if fontSize < 23:
        fontSize = 23
    if fontSize > 36:
        fontSize = 36

    # fontSize = 100

    return fontSize


# -------------------------------------------------------------------
#                       Confirm Screen Functions
# -------------------------------------------------------------------

