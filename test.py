'''
Canvas stress
=============

This example tests the performance of our Graphics engine by drawing large
numbers of small squares. You should see a black canvas with buttons and a
label at the bottom. Pressing the buttons adds small colored squares to the
canvas.

'''
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle
from random import random as r
from functools import partial

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    # create connection
    connect = None
    try:
        connect = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return connect


# create table function
def create_table():
    try:
        database = r"database\pysqlite.db"

        sql_create_cylinder_table = """ CREATE TABLE "cylinder" (
                                        id integer PRIMARY KEY,
                                        ingredient text NOT NULL DEFAULT 'NONE',
                                        type text NOT NULL,
                                        steps integer NOT NULL DEFAULT 0
                                    );"""

        sql_create_temporary_table = """ CREATE TABLE IF NOT EXISTS temporary (
                                                        ingredient text,
                                                        cylinder_id integer,
                                                        ml integer
                                                ); """

        sql_create_ingredient_table = """ CREATE TABLE IF NOT EXISTS ingredient (
                                                        "ID"	INTEGER,
                                                        "IngredientType"	TEXT NOT NULL DEFAULT 'None',
                                                        PRIMARY KEY("ID")
                                                        ); """

        # create database connection
        connect = create_connection(database)

        # create tables
        if connect is not None:
            cursor = connect.cursor()
            cursor.execute(sql_create_cylinder_table)
            cursor.execute(sql_create_temporary_table)
            cursor.execute(sql_create_ingredient_table)

        else:
            print("Error! Cannot create the connection")

        if (connect):
            connect.close()
            print("Closing SQLite connection")

    except Error as e:
        print(e)


# insert function for Cylinder table
def insert_cylinder(ingredient, steps):
    try:
        connect = sqlite3.connect(r"database\pysqlite.db")
        cursor = connect.cursor()
        sql = ''' INSERT INTO cylinder(ingredient, steps)
                  VALUES(?,?) '''
        cylinder = (ingredient, steps)
        cursor.execute(sql, cylinder)
        connect.commit()
        print("Inserted single row to cylinder table")
        cursor.close()
    except Error as e:
        print("Failed to insert into cylinder table. ", e)
    return cursor.lastrowid


# insert many function for Cylinder table
def insert_cylinder_many(cylinderList):
    try:
        connect = sqlite3.connect(r"database\pysqlite.db")
        cursor = connect.cursor()

        insert_many_query = """INSERT INTO cylinder(ingredient, type, steps)
                                VALUES(?,?,?)"""
        cursor.executemany(insert_many_query, cylinderList)
        connect.commit()
        print("Inserted ", cursor.rowcount, " of rows")
        cursor.close()

    except Error as e:
        print("Failed to insert multiple rows in cylinder table. ", e)

    finally:
        if (connect):
            connect.close()
            print("Closed connection")


# insert function for Temporary table
def insert_temporary(ingredient, ml):
    try:
        connect = sqlite3.connect(r"database\pysqlite.db")
        cursor = connect.cursor()

        cylinder_id = 0
        try:
            # select the cylinder id with base name
            cylinder_id = select_first_row_from_condition(ingredient)
            print("Base id", cylinder_id)

        except:
            print("No corresponding cylinder with this base name")

        sql = """INSERT INTO temporary(ingredient, cylinder_id, ml) VALUES(?,?,?);"""
        order = (ingredient, cylinder_id, ml)
        cursor.execute(sql, order)
        connect.commit()

        print("Inserted single row to temporary table")
        cursor.close()
    except Error as e:
        print("Failed to insert into temporary table. ", e)
    return cursor.lastrowid


def select_first_row_from_condition(ingredient):
    try:
        connect = sqlite3.connect(r"database\pysqlite.db")
        cursor = connect.cursor()

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

    except Error as e:
        print("Failed to select first row", e)

    finally:
        if (connect):
            connect.close()


def select_star_table(table):
    try:
        connect = sqlite3.connect(r"database\pysqlite.db")
        cursor = connect.cursor()

        sql = "SELECT * FROM " + table + ";"

        cursor.execute(sql)

        rows = cursor.fetchall()
        print("Table contents:")

        cursor.close()

        for row in rows:
            print(row)


    except Error as e:
        print("Failed to show table", e)

    finally:
        if (connect):
            connect.close()


def main():
    create_table()
    # print(select_first_row_from_condition('Ketchup'))

    # listToInsert = [("Ketchup", "Base", 500),
    #                 ("Mayonnaise", "Base", 10),
    #                 ("Mustard", "Base", 20),
    #                 ("Spice", "Flavor", 30)]
    # insert_cylinder_many(listToInsert)
    #
    insert_temporary("Ketchup", 20)
    insert_temporary("Spice", 10)

    # # create new row
    # insert_cylinder('Ketchup', 500)

    select_star_table("temporary")

    connect = sqlite3.connect(r"database\pysqlite.db")
    cursor = connect.cursor()

    sql = "SELECT * FROM cylinder;"

    cursor.execute(sql)

    bases = cursor.fetchall()
    print("Table contents:")

    for i, base in enumerate(bases):
        print("Base " + str(i) + ": " + base[1])

    cursor.close()


kivy_string = """
ScreenManagement
    BaseScreen:
        name: 'base'

    FlavorScreen:
        name: 'flavor'


<BaseScreen>:
    FloatLayout:
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: "images.jpg"

        Button:
            text: 'Base 1'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .2, 'y': .6}
        Button:
            text: 'Base 2'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .2, 'y': .4}
        Button:
            text: 'Base 3'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .2, 'y': .2}
        Button:
            text: 'Base 4'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .4, 'y': .6}
        Button:
            text: 'Base 5'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .4, 'y': .4}
        Button:
            text: 'Base 6'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .4, 'y': .2}

        Button:
            text: 'To Flavor'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .8, 'y': .1}
            on_release: 
                root.manager.current = 'flavor'

<FlavorScreen>:
    FloatLayout:
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: "images.jpg"

        Button:
            text: 'Flavor 1'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .2, 'y': .6}
        Button:
            text: 'Flavor 2'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .2, 'y': .4}
        Button:
            text: 'Flavor 3'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .2, 'y': .2}
        Button:
            text: 'Flavor 4'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .4, 'y': .6}
        Button:
            text: 'Flavor 5'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .4, 'y': .4}
        Button:
            text: 'Flavor 6'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .4, 'y': .2}        

        Button:
            text: 'To Base'
            size_hint_x : .1
            size_hint_y : .1
            pos_hint: {'x': .8, 'y': .1}
            on_release: 
                root.manager.current = 'base'
"""


class ScreenManagement(ScreenManager):
    pass


class BaseScreen(Screen):
    pass


class FlavorScreen(Screen):
    pass


class CustomLayout(FloatLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(CustomLayout, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 1, 0, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class StressCanvasApp(App):

    def add_rects(self, label, wid, count, *largs):
        label.text = str(int(label.text) + count)
        with wid.canvas:
            for x in range(count):
                Color(r(), 1, 1, mode='hsv')
                Rectangle(pos=(r() * wid.width + wid.x,
                               r() * wid.height + wid.y), size=(20, 20))

    def double_rects(self, label, wid, *largs):
        count = int(label.text)
        self.add_rects(label, wid, count, *largs)

    def reset_rects(self, label, wid, *largs):
        label.text = '0'
        wid.canvas.clear()

    def build(self):
        return Builder.load_string(kivy_string)


if __name__ == '__main__':
    main()
    # StressCanvasApp().run()
