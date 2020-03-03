import kivy
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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase

import i2c
from Controller import DatabaseController
from Model import UserModel, DatabaseClass, MainModel

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


# Button switches to
def initialize_buttons():
    # Step buttons
    UserModel.splitScreen.step1.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.sizeScreen))
    UserModel.splitScreen.step2.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.baseScreen))
    UserModel.splitScreen.step3.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.flavorScreen))
    UserModel.splitScreen.step4.bind(
        on_press=lambda x: UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.amountScreen))

    UserModel.splitScreen.step1.bind(on_press=lambda x: deleteAmountScreen())
    UserModel.splitScreen.step2.bind(on_press=lambda x: deleteAmountScreen())
    UserModel.splitScreen.step3.bind(on_press=lambda x: deleteAmountScreen())
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

    # UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: i2c.run())
    # UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: print("I2C"))
    # UserModel.amountScreen.doneButton.bind(on_press=lambda x: switch_screen('Split Screen'))
    # UserModel.splitScreen.nextButton1.bind(on_press=lambda x: switch_screen('Base Screen'))
    # UserModel.amountScreen.addButton.bind(on_press=lambda x: switch_screen('Loading Screen'))

    UserModel.splitScreen.baseScreen.nextButton.bind(on_press=lambda x: getBaseList())
    UserModel.splitScreen.baseScreen.nextButton.bind(on_press=lambda x: deleteAmountScreen())

    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: getFlavorList())

    # TODO: uncomment
    # Trigger Amount screen properties
    # UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: reloadAmountScreen())
    UserModel.splitScreen.flavorScreen.nextButton.bind(on_press=lambda x: buildAmountScreen(UserModel.splitScreen.amountScreen))

    # UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: amountScreenDone())
    # UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x: switch_screen("Main Screen"))
    #
    # UserModel.splitScreen.amountScreen.doneButton.bind(on_press=lambda x:
    # UserModel.splitScreen.carouselWidget.load_slide(UserModel.splitScreen.sizeScreen))


# -------------------------------------------------------------------
#                       Carousel Functions
# -------------------------------------------------------------------
def initialize_carousel(split_screen):
    # add all the screens to the carousel
    split_screen.carouselWidget.add_widget(split_screen.sizeScreen)
    split_screen.carouselWidget.add_widget(split_screen.baseScreen)
    split_screen.carouselWidget.add_widget(split_screen.flavorScreen)
    split_screen.carouselWidget.add_widget(split_screen.amountScreen)


def resetStepButtons():
    UserModel.splitScreen.step2.disabled = True
    UserModel.splitScreen.step3.disabled = True
    UserModel.splitScreen.step4.disabled = True


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

    print(UserModel.splitScreen.baseScreen.baseList)


def resetBaseScreen():
    for button in UserModel.splitScreen.baseScreen.baseToggleList:
        button.state = 'normal'
        button.disabled = False

    UserModel.splitScreen.baseScreen.baseList = []
    UserModel.splitScreen.baseScreen.baseToggleList = []
    UserModel.splitScreen.baseScreen.nextButton.disabled = True
    UserModel.splitScreen.baseScreen.nextButton.colour = (0, 0, 0, 0)


# setup the base screen by getting cylinders(bases) from the database


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

    print(UserModel.splitScreen.flavorScreen.flavorList)


# # TODO: uncomment
# def reloadAmountScreen():
#     splitScreen = UserModel.splitScreen
#     amountScreen = UserModel.splitScreen.amountScreen
#     # Remove slider if only 1 base chosen
#     if len(splitScreen.baseScreen.baseList) <= 1:
#         amountScreen.sliderTemplateGrid.remove_widget(amountScreen.slider)
#         amountScreen.sliderExist = False
#         # print(len(splitScreen.baseScreen.baseList))
#     # Add slider when slider was removed and chosen bases becomes 2
#     elif len(splitScreen.baseScreen.baseList) == 2 and amountScreen.sliderExist == False:
#         amountScreen.sliderTemplateGrid.add_widget(amountScreen.slider)
#         amountScreen.sliderExist = True
#         # print("Added slider")
#
#     # Delete or add pie chart
#     if len(splitScreen.baseScreen.baseList) <= 1:
#         amountScreen.baseChartLayout.remove_widget(amountScreen.baseChart)
#         amountScreen.baseChartExist = False
#         print("Removed chart")
#     elif len(splitScreen.baseScreen.baseList) == 2 and amountScreen.baseChartExist == False:
#         amountScreen.baseChartLayout.add_widget(amountScreen.baseChart)
#         amountScreen.baseChartExist = True
#
#     try:
#         amountScreen.base1.text = splitScreen.baseScreen.baseList[0]
#     except:
#         amountScreen.base1.text = ""
#         print("Nothing inside list")
#
#     try:
#         amountScreen.base2.text = splitScreen.baseScreen.baseList[1]
#     except:
#         amountScreen.base2.text = ""
#         print("No second base was chosen")
#
#     # Show flavors based on user selection
#     for i, flavor in enumerate(splitScreen.flavorScreen.flavorList):
#         try:
#             amountScreen.flavorLayoutList.append(UserModel.FlavorsLayout(flavor))
#             amountScreen.sliderTemplateGrid.add_widget(amountScreen.flavorLayoutList[i])
#         except:
#             print("Flavor already added")


def deleteAmountScreen():
    amountScreen = UserModel.splitScreen.amountScreen
    # Delete flavors when user deselects flavors
    for i, flavor in enumerate(UserModel.splitScreen.flavorScreen.flavorList):
        try:
            amountScreen.sliderTemplateGrid.remove_widget(amountScreen.flavorLayoutList[i])
            amountScreen.flavorLayoutList.remove(UserModel.FlavorsLayout(flavor))
        except:
            print("Flavor already removed")


def resetFlavorScreen():
    for button in UserModel.splitScreen.flavorScreen.flavorToggleList:
        button.state = 'normal'
        button.disabled = False

    UserModel.splitScreen.flavorScreen.flavorList = []
    UserModel.splitScreen.flavorScreen.flavorToggleList = []


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
                       (UserModel.splitScreen.amountScreen.flavorLayoutList[i].label_text.text,
                        UserModel.splitScreen.amountScreen.flavorLayoutList[i].flavorName.text))
    # Update flavor cylinder_id in temporary table
    for flavor in UserModel.splitScreen.flavorScreen.flavorList:
        DatabaseController.update_temporary_cylinder(flavor)

    # When 1 base is chosen (slider defaults to 180)
    if len(baseList) == 1 and UserModel.splitScreen.amountScreen.slider.value == 180:
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
            elif sizeList[0] == "MEDIUM":
                for i, base in enumerate(baseList):
                    cursor.execute("UPDATE temporary "
                                   "SET ml = ?"
                                   "WHERE ingredient = ?",
                                   (baseProportionList[i] * 50 / 360, baseList[i]))
                    print(baseProportionList[i] * 50 / 360)
                    print(baseList[i])
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
        DatabaseController.update_temporary_cylinder(base)

    connect.commit()
    cursor.close()

    # Deselect all previous options
    resetStepButtons()
    resetSizeScreen()
    resetBaseScreen()
    resetFlavorScreen()


def printOut():
    print('called')


def buildAmountScreen(amountScreen):
    amountScreen.scroll.clear_widgets()
    if Window.width < 770:
        if not amountScreen.built:
            button = UserModel.DoneRoundedButton1()
            button.bind(on_press=lambda x: amountScreenDone())
            button.bind(on_press=lambda x: switch_screen("Main Screen"))
            amountScreen.box.add_widget(button)
        buildAmountScreenGridLayout(amountScreen)
    else:
        if not amountScreen.built:
            button = UserModel.DoneRoundedButton2()
            button.bind(on_press=lambda x: amountScreenDone())
            button.bind(on_press=lambda x: switch_screen("Main Screen"))
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

    # check how many flavors and add flavor templates
    for f in flavorList:
        grid.add_widget(UserModel.FlavorsLayout(name=f))

    amountScreen.scroll.add_widget(grid)


def buildAmountScreenStackLayout(amountScreen):
    amountScreen.scroll.clear_widgets()

    # TODO: replace baselist with actual baselist
    baseList = UserModel.splitScreen.baseScreen.baseList
    flavorList = UserModel.splitScreen.flavorScreen.flavorList

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
        baseTemplate.baseLabel1.text = baseList[0]
        baseTemplate.baseLabel1.width = Window.width * 0.5
        stack.add_widget(baseTemplate)
        totalHeight += 50 + (2 * space)
    else:
        # Bases
        baseTemplate = UserModel.BaseStackTemplate2()
        baseTemplate.width = Window.width * 0.5
        baseTemplate.baseLabel1.text = baseList[0]
        baseTemplate.baseLabel2.text = baseList[1]
        stack.add_widget(baseTemplate)
        totalHeight += 50 + 75 + 70 + (2 * space)

    # check how many flavors and add flavor templates
    for f in flavorList:
        flavor = UserModel.FlavorsLayout(name=f)
        flavor.size_hint_x = None
        flavor.width = Window.width * 0.5
        stack.add_widget(flavor)
        totalHeight += flavor.height + (2 * space)

    pieChart = UserModel.AmountPieChart()
    pieChart.width = (Window.width * 0.5) - (5 * padding)

    if len(baseList) == 1:
        pieChart.pie_chart_value = 360
    else:
        pieChart.pie_chart_value = baseTemplate.slider.value
        baseTemplate.pie = pieChart
        baseTemplate.slider.bind(value=updatePie)

    print("width:")
    print(pieChart.width)
    stack.add_widget(pieChart)

    stack.height = totalHeight

    grid.add_widget(stack)

    amountScreen.scroll.add_widget(grid)
    pass


def updatePie(instance, value):
    instance.parent.pie.pie_chart_value = instance.value


# -------------------------------------------------------------------
#                       Amount Screen Functions
# -------------------------------------------------------------------

def header_font_size():
    fontSize = Window.width * 0.05
    if fontSize < 23:
        fontSize = 23
    if fontSize > 36:
        fontSize = 36

    return fontSize
