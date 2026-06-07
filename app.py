from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------- Config ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///saas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- Tenant Model ----------
class Tenant(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_name = db.Column(
        db.String(100),
        unique=True
    )

# ---------- Task Model ----------
class Task(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200)
    )

    tenant_id = db.Column(
        db.Integer,
        db.ForeignKey("tenant.id")
    )

with app.app_context():
    db.create_all()

# ---------- Create Tenant ----------
@app.route(
    "/tenant",
    methods=["POST"]
)
def create_tenant():

    data = request.get_json()

    tenant = Tenant(
        company_name=data["company_name"]
    )

    db.session.add(tenant)
    db.session.commit()

    return jsonify({
        "message": "Tenant created"
    })

# ---------- Add Task ----------
@app.route(
    "/task",
    methods=["POST"]
)
def create_task():

    data = request.get_json()

    task = Task(
        title=data["title"],
        tenant_id=data["tenant_id"]
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created"
    })

# ---------- Get Tenant Tasks ----------
@app.route(
    "/tenant/<int:tenant_id>/tasks"
)
def tenant_tasks(tenant_id):

    tasks = Task.query.filter_by(
        tenant_id=tenant_id
    ).all()

    return jsonify([
        {
            "id": task.id,
            "title": task.title
        }
        for task in tasks
    ])

# ---------- List Tenants ----------
@app.route("/tenants")
def tenants():

    data = Tenant.query.all()

    return jsonify([
        {
            "id": t.id,
            "company_name":
            t.company_name
        }
        for t in data
    ])

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
