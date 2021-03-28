from enum import unique
from flask import Flask, render_template, request, redirect, flash
from flask.helpers import url_for
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import count
from send_email import send
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = 'heightcheck'
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/height_calculator'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://myxbyvdzbwswrh:cd00391eb7d06563800ca77f52337373cbba2f318c5837a6afb5ef8fec13fa73@ec2-54-167-168-52.compute-1.amazonaws.com:5432/dcf565vdpiuk7n?sslmode=require'
db = SQLAlchemy(app)

class Data(db.Model):
   __tablename__="data"
   id=db.Column(db.Integer, primary_key=True)
   email_=db.Column(db.String(120), unique=True)
   height_=db.Column(db.Integer)

   def __init__(self, email_, height_):
      self.email_ = email_
      self.height_ = height_


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
   if request.method=='POST':
      email = request.form["email_name"]
      height = request.form["height_name"]
      if db.session.query(Data).filter(Data.email_==email).count() == 0:
         data = Data(email, height)
         db.session.add(data)
         db.session.commit()

         average = db.session.query(func.avg(Data.height_)).scalar()
         average = round(average, 1)
         count = db.session.query(Data.height_).count()
         send(email, height, average, count)
         return render_template("success.html")
      else:
         # return render_template("index.html")
         flash("Seems like your email is already registered !!!", "info")
         return redirect(url_for("index"))

if __name__ == '__main__':
   db.create_all()
   app.run(debug=True, port=5001)