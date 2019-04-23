import numpy as np
from PIL import Image
from flask import current_app as app
from pytesseract import image_to_string
import sqlite3
from flask import g
import os
from flask import (
        Flask, Blueprint, render_template, request
)
from werkzeug.utils import secure_filename

bp = Blueprint('label', __name__, url_prefix='/label')

global words
words = []
results = {}
DATABASE = 'ingredients-label/static/database/ingredients.db'
#connect to database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        print("connect successful")
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT name,description FROM ingredients")
        #2D array.
        rows = cur.fetchall()
        for row in rows:
            print(row)
    return db


#end

@bp.route('/')
def index():
    return render_template('index.html',results=results)


@bp.route('/uploader', methods = ['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            #return redirect(request.url)
            #if file not fould redirect to index page and ask to re-upload
            results={}
            return results(results)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:
            #config the folder for upload image and rename it
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],"img.png"))

            img = Image.open('ingredients-label/static/img/img.png')

            img = img.convert('L')

            text = image_to_string(img)
            print("raw text")
            print (text)
            #print text
            #if found these ingredients words
            if((text.find("INGREDIENTS:")!=-1) or (text.find("ingredients:")!=-1) or (text.find("Ingredients:")!=-1)):
                print("Found it")
                indexOfIn = 0
                #set the index of the word ingredients depends on whihch one is found
                if(text.find("INGREDIENTS:")!=-1):
                    indexOfIn = text.find("INGREDIENTS:")
                elif(text.find("ingredients:")!=-1):
                    indexOfIn = text.find("ingredients:")
                elif(text.find("Ingredients:")!=-1):
                    indexOfIn = text.find("Ingredients:")
                else:
                    print("Not found")

                index = indexOfIn + 12
                startIndex = index
                #iterate until we get the period if not stop if index exceed the string length
                # while(text[index]!="."):
                #     index = index +1
                #     if(index < len(text)):
                #         if(text[index] == "."):
                #             break
                #     else:
                #         break
                #get the string into the list
                while (index!=len(text)-1):
                    index = index +1

                dictlist = text[startIndex: index]
                dictlist = dictlist.strip()
                words = dictlist.split(",") #list of words
                #try to print out on terminal to check
                print("print list: ")
                #test database
                #get_db()
                #connect to database
                db = getattr(g, '_database', None)
                if db is None:
                    db = g._database = sqlite3.connect(DATABASE)
                    print("connect successful")
                    db.row_factory = sqlite3.Row
                    cur = db.cursor()
                    cur.execute("SELECT name,description FROM ingredients")
                    #2D array.
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
                    results = {}
                    print("found in database")
                    for word in words:
                        word = word.lstrip()
                        for word2 in rows:
                            if word2[0].lower() == word.lower():
                                print(word2[0] + ": "+ word2[1])
                                results[word2[0]]=word2[1]
                    return results_page(results)
                    results ={}
                print("after searching")

            #if not found on the string text
            else:

                countRotate = 0
                #rotat until we can find it, if roate in more than 3 times =  not found
                while (text.find("INGREDIENTS:") == -1 or text == "" or (text.find("Ingredients:")==-1) or (text.find("ingredients:")==-1)):

                    # rotate it and check if we can find it
                    img = img.rotate(90)
                    text = image_to_string(img)
                    countRotate = countRotate + 1

                    #print countRotate
                    #print text

                    # if we find it put them in to the list to use for database.
                    if((text.find("INGREDIENTS:")!=-1) or (text.find("ingredients:")!=-1) or (text.find("Ingredients:")!=-1)):
                        indexOfIn = 0
                        print("if inside while loop")
                        if(text.find("INGREDIENTS:")!=-1):
                            indexOfIn = text.find("INGREDIENTS:")
                        elif(text.find("ingredients:")!=-1):
                            indexOfIn = text.find("ingredients:")
                        elif(text.find("Ingredients:")!=-1):
                            indexOfIn = text.find("Ingredients:")
                        else:
                            print("Not found")

                        #set the start index for the string
                        index = indexOfIn + 12
                        startIndex = index
                        #iterate it until find a period or when index exceed the string length we stop
                        # while(text[index]!="."):
                        #     index = index +1
                        #     if(index < len(text)):
                        #         if(text[index] == "."):
                        #             break
                        #     else:
                        #         break
                        #get the list of words for using on database
                        while (index!=len(text)-1):
                            index = index +1
                        dictlist = text[startIndex: index]
                        dictlist = dictlist.strip()
                        words = dictlist.split(",")
                        #print on terminal for testing purpose
                        #print "print list: "
                        #test database
                        #get_db()
                        #connect to database
                        db = getattr(g, '_database', None)
                        if db is None:
                            db = g._database = sqlite3.connect(DATABASE)
                            print("connect successful")
                            db.row_factory = sqlite3.Row
                            cur = db.cursor()
                            cur.execute("SELECT name FROM ingredients")
                            #2D array.
                            rows = cur.fetchall()
                            for row in rows:
                                print(row)
                            results ={}
                            for word in words:
                                word = word.lstrip()
                                for word2 in rows:
                                    if word2[0].lower() == word.lower():
                                        print(word2[0] + ": "+ word2[1])
                                        results[word2[0]]=word2[1]
                            return results_page(results)
                            results ={}
                        print("after searching")

                        break
                    #if we rotate more than 3 times meaning that we did not find it. Break out of loop.
                    if(countRotate >3):
                        text ="Not Found."
                        break
            return text
    else:
        results = {}
        return results_page(results)
    return "no file"

def results_page(ingredients=None):
    if ingredients is None:
        ingredients = {}
    return render_template('results.html', ingredients=ingredients)
