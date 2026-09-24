from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from github_service import get_repository

app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cicd.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    repository = db.Column(db.String(300), nullable=False)

    branch = db.Column(db.String(100), nullable=False)

    app_type = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():

    return "Cloud-Native CI/CD Platform Backend Running!"


@app.route("/api/health")
def health():

    return {
        "status": "healthy",
        "service": "CI/CD Platform"
    }


@app.route("/api/projects", methods=["POST"])
def create_project():

    data = request.get_json()

    project = Project(
        name=data["name"],
        repository=data["repository"],
        branch=data["branch"],
        app_type=data["app_type"]
    )

    db.session.add(project)

    db.session.commit()

    return jsonify({
        "message": "Project created successfully",
        "project": {
            "id": project.id,
            "name": project.name,
            "repository": project.repository,
            "branch": project.branch,
            "app_type": project.app_type
        }
    }), 201


@app.route("/api/projects", methods=["GET"])
def get_projects():

    projects = Project.query.all()

    result = []

    for project in projects:

        result.append({
            "id": project.id,
            "name": project.name,
            "repository": project.repository,
            "branch": project.branch,
            "app_type": project.app_type
        })

    return jsonify(result)


@app.route("/api/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):

    project = db.session.get(Project, project_id)

    if not project:

        return jsonify({
            "error": "Project not found"
        }), 404

    return jsonify({
        "id": project.id,
        "name": project.name,
        "repository": project.repository,
        "branch": project.branch,
        "app_type": project.app_type
    })


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):

    project = db.session.get(Project, project_id)

    if not project:

        return jsonify({
            "error": "Project not found"
        }), 404

    db.session.delete(project)

    db.session.commit()

    return jsonify({
        "message": "Project deleted successfully"
    })
@app.route("/api/github/repository", methods=["POST"])
def github_repository():

    data = request.get_json()

    repository_url = data.get("repository")

    if not repository_url:
        return jsonify({
            "error": "Repository URL is required"
        }), 400

    try:

        repository = get_repository(repository_url)

        return jsonify(repository)

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 400


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001
    )