from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import Application
from models import db, VolunteerProject
from flask import request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volunteer_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/projects")
def projects():
    projects = VolunteerProject.query.all()
    return render_template("projects.html", projects=projects)

@app.route("/projects/create")
def create_project():
    project = VolunteerProject(
        title="Clean City",
        description="Join us to clean up the city.")
    db.session.add(project)
    db.session.commit()
    return "Project created successfully"

@app.route("/reset-db")
def reset_db():
    db.drop_all()
    db.create_all()
    return "Database reset successfully"

@app.route("/projects/new")
def new_project():
    return render_template("new_project.html")

@app.route("/projects/save", methods=["POST"])
def save_project():
    title = request.form["title"]
    description = request.form["description"]
    project = VolunteerProject(title=title, description=description)
    db.session.add(project)
    db.session.commit()
    return redirect(url_for("projects"))

@app.route("/projects/edit/<int:project_id>")
def edit_project(project_id):
    project = VolunteerProject.query.get_or_404(project_id)
    return render_template("edit_project.html", project=project)

@app.route("/projects/update/<int:project_id>", methods=["POST"])
def update_project(project_id):
    project = VolunteerProject.query.get_or_404(project_id)
    project.title = request.form["title"]
    project.description = request.form["description"]
    db.session.commit()
    return redirect(url_for("projects"))

@app.route("/projects/delete/<int:project_id>")
def delete_project(project_id):
    project = VolunteerProject.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("projects"))

@app.route("/projects/apply/<int:project_id>", methods=["GET", "POST"])
def apply_project(project_id):
    project = VolunteerProject.query.get_or_404(project_id)
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        organisation = request.form["organisation"]
        application = Application(name=name, email=email, organisation=organisation, project_id=project.id)
        db.session.add(application)
        db.session.commit()
        return redirect(url_for("projects"))
    return render_template("apply.html", project=project)

@app.route("/admin")
def admin_panel():
    applications = Application.query.order_by(Application.created_at.desc()).all()
    return render_template("admin.html", applications=applications)

@app.route("/admin/accept/<int:app_id>")
def accept_application(app_id):

    app_obj = Application.query.get_or_404(app_id)
    app_obj.status = "accepted"
    db.session.commit()
    return redirect(url_for("admin_panel"))


@app.route("/admin/reject/<int:app_id>")
def reject_application(app_id):
    app_obj = Application.query.get_or_404(app_id)
    app_obj.status = "rejected"
    db.session.commit()
    return redirect(url_for("admin_panel"))
    
if __name__ == '__main__':
    app.run(debug=True)
