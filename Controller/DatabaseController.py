import sqlite3
from Model import Cylinder

# connect to the database called example.db
conn = sqlite3.connect('Model/Cylinder.db')
cursor = conn.cursor()


# function that inserts new ingredients
def update_cylinders():
    # clear the cylinder array
    Cylinder.cylinderArray.clear()

    cursor.execute("SELECT cylinderID, ingredient, amount FROM Cylinder")
    result = cursor.fetchall()

    for x in result:
        Cylinder.cylinderArray.append(Cylinder.Cylinder(x[0], x[1], x[2]))


def get_cylinder(cylinder_id):
    for i in Cylinder.cylinderArray:
        if i.cylinderID == cylinder_id:
            return i


def database_close():
    conn.close()
