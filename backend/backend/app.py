from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lesson_plans.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class LessonPlan(db.Model):
    __tablename__ = "lesson_plans"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    objective = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    planned_date = db.Column(db.String(20), nullable=False)
    discipline = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.Text, nullable=True)
    support_resources = db.Column(db.Text, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "objective": self.objective,
            "summary": self.summary,
            "planned_date": self.planned_date,
            "discipline": self.discipline,
            "contents": self.contents,
            "support_resources": self.support_resources,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


with app.app_context():
    db.create_all()


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "Lesson Plan Manager API is running"
    }), 200


@app.route("/lesson-plans", methods=["POST"])
def create_lesson_plan():
    data = request.get_json()

    required_fields = [
        "title",
        "objective",
        "summary",
        "planned_date",
        "discipline",
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "error": f"The field '{field}' is required."
            }), 400

    lesson_plan = LessonPlan(
        title=data["title"],
        objective=data["objective"],
        summary=data["summary"],
        planned_date=data["planned_date"],
        discipline=data["discipline"],
        contents=data.get("contents"),
        support_resources=data.get("support_resources"),
        tags=data.get("tags"),
    )

    db.session.add(lesson_plan)
    db.session.commit()

    return jsonify({
        "message": "Lesson plan created successfully.",
        "lesson_plan": lesson_plan.to_dict()
    }), 201


@app.route("/lesson-plans", methods=["GET"])
def list_lesson_plans():
    lesson_plans = LessonPlan.query.order_by(LessonPlan.created_at.desc()).all()

    return jsonify({
        "items": [lesson_plan.to_dict() for lesson_plan in lesson_plans],
        "total": len(lesson_plans)
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
