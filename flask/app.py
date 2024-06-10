from flask  import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy  import SQLAlchemy
#time
import sys
from datetime import datetime

app = Flask(__name__)# the file
#config sqlalchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"

#initilaize the app with extension
db = SQLAlchemy(app)

#model
class Todo(db.Model):
    __tablename__ = 'todo'
    sno = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.Title}"

@app.route("/",methods=["GET","POST"])
def hello_world():
    if request.method== "POST":
        todo_title =request.form['title']
        desc_todo =  request.form['desc']
        data = Todo(Title=todo_title,desc=desc_todo)
        db.session.add(data)
        db.session.commit()

 

    alltodo = Todo.query.all()

    return render_template('index.html',alltodo=alltodo )

@app.route('/delete/<int:sno>')
def delete(sno):
    #all qquery
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
 
    return redirect('/') 

@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    #all qquery
    if request.method=='POST':
        todo_title = request.form['title']
        desc_todo =  request.form['desc']
        data = Todo.query.filter_by(sno=sno).first()
        data.Title = todo_title
        data.desc = desc_todo
        db.session.add(data)
        db.session.commit()
        return redirect("/")
         
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo) 



if __name__ == "__main__":
  
    app.app_context().push()
    db.create_all()
    app.run(debug = True)