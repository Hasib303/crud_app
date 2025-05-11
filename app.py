from flask import Flask, render_template, request
from flask_scss import Scss 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, redirect, url_for


#My app 
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

#Data class with rows 
class myTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

with app.app_context():
        db.create_all()


# Routes to webpages
# Homepage
@app.route("/", methods=["POST", "GET"])
def index():
    # return render_template("index.html")
    # Add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = myTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
        
    # see all current task
    else:
        tasks = myTask.query.order_by(myTask.created).all()
        return render_template('index.html', tasks=tasks)
 


#Delete an item
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = myTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"



# Edit an item
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id:int):
    task = myTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"

    else:
        return render_template('edit.html', task = task)




#Runner and debugger   
if __name__ == "__main__":
    # app.run(debug=True)
    # with app.app_context():
    #     db.create_all()

    app.run(debug=True)