from flask_restful import Resource, reqparse
import datetime
import arrow

from models.issue import IssueModel


class Issue(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("_id", type=int, location="form")
    parser.add_argument(
        "issue_title",
        type=str,
        location="form",
        required=True,
        help="issue_title cannot be empty",
    )
    parser.add_argument(
        "issue_text",
        type=str,
        location="form",
        required=True,
        help="issue_text cannot be empty",
    )
    parser.add_argument(
        "created_by",
        type=str,
        location="form",
        required=True,
        help="created_by cannot be empty",
    )
    parser.add_argument("assigned_to", type=str, location="form")
    parser.add_argument("status_text", type=str, location="form")

    def post(self, project_name):
        data = Issue.parser.parse_args()

        issue_title = data["issue_title"]
        issue_text = data["issue_text"]
        created_by = data["created_by"]
        assigned_to = data["assigned_to"] or ""
        status_text = data["status_text"] or ""
        created_on = datetime.datetime.utcnow()
        _open = True

        new_issue = IssueModel(
            issue_title=issue_title,
            issue_text=issue_text,
            created_by=created_by,
            assigned_to=assigned_to,
            status_text=status_text,
            _open=_open,
            created_on=created_on,
            project_name=project_name,
        )
        new_issue.save_to_db()
        return new_issue.json(), 201
