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
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# create table function
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# insert function for Cylinder table
def insert_cylinder(conn, cylinder):
    sql = ''' INSERT INTO cylinder(ingredient, amount)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, cylinder)
    return cur.lastrowid

def main():
    database = r"C:\sqlite\db\pysqlite.db"

    sql_create_cylinder_table = """ CREATE TABLE IF NOT EXISTS cylinder (
                                            id integer PRIMARY KEY,
                                            ingredient text,
                                            amount integer
                                    ); """

    # create database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_cylinder_table)

    else:
        print("Error! Cannot create the connection")

    with conn:
        # create new row
        cylinderRow = ('Ketchup', 500);
        insert_cylinder(conn, cylinderRow)



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
