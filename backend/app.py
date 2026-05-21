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
    search = request.args.get("search")
    discipline = request.args.get("discipline")
    tag = request.args.get("tag")
    planned_date = request.args.get("planned_date")
    sort_by = request.args.get("sort_by", "created_at")
    order = request.args.get("order", "desc")
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    query = LessonPlan.query

    if search:
        query = query.filter(LessonPlan.title.ilike(f"%{search}%"))

    if discipline:
        query = query.filter(LessonPlan.discipline.ilike(f"%{discipline}%"))

    if tag:
        query = query.filter(LessonPlan.tags.ilike(f"%{tag}%"))

    if planned_date:
        query = query.filter(LessonPlan.planned_date == planned_date)

    if sort_by == "title":
        sort_column = LessonPlan.title
    else:
        sort_column = LessonPlan.created_at

    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "items": [lesson_plan.to_dict() for lesson_plan in pagination.items],
        "total": pagination.total,
        "page": page,
        "limit": limit,
        "pages": pagination.pages
    }), 200


@app.route("/lesson-plans/<int:lesson_plan_id>", methods=["GET"])
def get_lesson_plan(lesson_plan_id):
    lesson_plan = LessonPlan.query.get(lesson_plan_id)

    if not lesson_plan:
        return jsonify({
            "error": "Lesson plan not found."
        }), 404

    return jsonify(lesson_plan.to_dict()), 200


@app.route("/lesson-plans/<int:lesson_plan_id>", methods=["PUT"])
def update_lesson_plan(lesson_plan_id):
    lesson_plan = LessonPlan.query.get(lesson_plan_id)

    if not lesson_plan:
        return jsonify({
            "error": "Lesson plan not found."
        }), 404

    data = request.get_json()

    lesson_plan.title = data.get("title", lesson_plan.title)
    lesson_plan.objective = data.get("objective", lesson_plan.objective)
    lesson_plan.summary = data.get("summary", lesson_plan.summary)
    lesson_plan.planned_date = data.get("planned_date", lesson_plan.planned_date)
    lesson_plan.discipline = data.get("discipline", lesson_plan.discipline)
    lesson_plan.contents = data.get("contents", lesson_plan.contents)
    lesson_plan.support_resources = data.get(
        "support_resources",
        lesson_plan.support_resources
    )
    lesson_plan.tags = data.get("tags", lesson_plan.tags)

    db.session.commit()

    return jsonify({
        "message": "Lesson plan updated successfully.",
        "lesson_plan": lesson_plan.to_dict()
    }), 200


@app.route("/lesson-plans/<int:lesson_plan_id>", methods=["DELETE"])
def delete_lesson_plan(lesson_plan_id):
    lesson_plan = LessonPlan.query.get(lesson_plan_id)

    if not lesson_plan:
        return jsonify({
            "error": "Lesson plan not found."
        }), 404

    db.session.delete(lesson_plan)
    db.session.commit()

    return jsonify({
        "message": "Lesson plan deleted successfully."
    }), 200


@app.route("/smart-assist", methods=["POST"])
def smart_assist():
    data = request.get_json()

    title = data.get("title")
    discipline = data.get("discipline")
    summary = data.get("summary")

    if not title or not discipline or not summary:
        return jsonify({
            "error": "The fields 'title', 'discipline' and 'summary' are required."
        }), 400

    recommendations = {
        "contents": [
            f"Introduction to {title}",
            f"Main concepts related to {discipline}",
            "Practical activity based on the lesson summary"
        ],
        "support_resources": [
            "Presentation slides",
            "Complementary reading material",
            "Practical exercises"
        ],
        "related_topics": [
            "Basic concepts",
            "Practical examples",
            "Review questions"
        ],
        "recommended_tags": [
            discipline.lower().replace(" ", "-"),
            "lesson-plan",
            "education"
        ]
    }

    return jsonify({
        "message": "AI recommendations generated successfully.",
        "recommendations": recommendations
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
