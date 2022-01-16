import os.path

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy     #pip install flask_sqlalchemy    pip install sqlalchemy==1.3.23

# import sqlite3
# db = sqlite3.connect("books-collection.db")
# cursor= db.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
                                                                                                                    #
# cursor.execute("INSERT OR IGNORE INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
#  db.commit()


app = Flask(__name__)

        ##________CREATE DATABASE_________##

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
                                                               #Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


       ##__________CREATE TABLE_________##

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),unique=True,nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)

                                                                #Optional: this will allow each book object to be identified by its title,... when printed.
    def __repr__(self):
        return f'<Book {self.title} rated: {self.rating}>'

db.create_all()

       ##_________CREATE RECORD_______##

new_book = Book( title="boynextdoor", author="Jimin", rating=9.5)
# db.session.add(new_book)
# db.session.commit()                                           #  moving it ito add function bcuz its causing eror for creating same for multiple times while its being run




all_books = []                                                   # this was createed for normal sql ..like for old db file books-collction


@app.route('/')
def home():
    all_boks=db.session.query(Book).all()                        # now this is created again(we might give another name too but i didt ) just for new sqlal
    return render_template('index.html',books=all_boks)


@app.route("/add",methods=["GET","POST"])
def add():
        if request.method =="POST":
            sqlalbook = Book(
                    title=request.form["Title"],
                    author=request.form["author"],
                    rating=request.form["rating"])
            db.session.add(sqlalbook)
            db.session.commit()
            all_books.append(sqlalbook)
            print(sqlalbook)
            return redirect(url_for('home'))

        return render_template('add.html')


     #    newbook={
     #        "title":request.form["title"],
     #        "author":request.form["author"],
     #        "rating":request.form["rating"]
     #    }
     #    all_books.append(newbook)
     #    print(all_books)
     #    NOTE: we can use the redirect method from flask to redirect to another route
     #    e.g. in this case to the home page after the form has been submitted.
     #
     #     return redirect(url_for('home'))
     # return render_template('add.html')

@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method=="POST":                                      #{
        bookid=request.form["id"]                           #ig only this line comes from index.html id
        bookuptoupdate=Book.query.get(bookid)
        bookuptoupdate.rating = request.form["rating"]             # this works after clicking on edit rating then edits , updating and returning to home page
        db.session.commit()
        return redirect(url_for('home'))                            #}
    bookid=request.args.get('Id')                                   # this is for opening edit url after knowing  which book id no. to be editted
    bookselected=Book.query.get(bookid)
    return render_template("edit.html",selectedbook=bookselected)

@app.route("/delete")
def delete():
    book_id=request.args.get('id')
    print(book_id)

    booktobedeleted=Book.query.get(book_id)
    db.session.delete(booktobedeleted)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

