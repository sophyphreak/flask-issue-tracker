from flask_restful import Resource, reqparse
import datetime
import arrow

from models.issue import IssueModel


class Issue(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "_id", type=int,
    )
    parser.add_argument(
        "issue_title", type=str,
    )
    parser.add_argument(
        "issue_text", type=str,
    )
    parser.add_argument(
        "created_by", type=str,
    )
    parser.add_argument(
        "assigned_to", type=str,
    )
    parser.add_argument(
        "status_text", type=str,
    )
    parser.add_argument(
        "open", type=str,
    )

    def post(self, project_name):
        data = Issue.parser.parse_args()

        issue_title = data["issue_title"]
        if not issue_title:
            return {"error": "issue_title is required"}
        issue_text = data["issue_text"]
        if not issue_text:
            return {"error": "issue_text is required"}
        created_by = data["created_by"]
        if not created_by:
            return {"error": "created_by is required"}
        assigned_to = data["assigned_to"] or ""
        status_text = data["status_text"] or ""
        created_on = datetime.datetime.utcnow()
        _open = data["open"] or True

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

    def put(self, project_name):
        data = Issue.parser.parse_args()

        _id = data["_id"]
        if _id is None:
            return {"error": "_id is required"}
        issue = IssueModel.find_by_id(_id)

        if issue is None:
            return {
                "error": f"could not update {_id}",
                "message": f"issue with id of {_id} does not exist",
            }

        issue_title = data["issue_title"]
        issue_text = data["issue_text"]
        created_by = data["created_by"]
        assigned_to = data["assigned_to"]
        status_text = data["status_text"]
        _open = data["open"]

        if not _open is None:
            _open = _open == 'True' or _open == 'true'
        if issue_title:
            issue.issue_title = issue_title
        if issue_text:
            issue.issue_text = issue_text
        if created_by:
            issue.created_by = created_by
        if assigned_to:
            issue.assigned_to = assigned_to
        if status_text:
            issue.status_text = status_text
        if not _open is None:
            issue._open = _open
        issue.updated_on = datetime.datetime.utcnow()

        issue.save_to_db()

        if (
            not issue_title
            and not issue_text
            and not created_by
            and assigned_to is None
            and status_text is None
            and _open is None
        ):
            return {
                "error": f"could not update {_id}",
                "message": "no updated field sent",
            }

        return {"success": f"successfully updated {_id}"}

    def delete(self, project_name):
        data = Issue.parser.parse_args()

        _id = data["_id"]
        if _id is None:
            return {"error": "_id is required"}
        issue = IssueModel.find_by_id(_id)
        if issue:
            issue.delete_from_db()
            return {"success": f"deleted {_id}"}
        else:
            return {"failed": f"could not delete {_id}"}

    def get(self, project_name):
        data = Issue.parser.parse_args()

        issue_title = data["issue_title"]
        issue_text = data["issue_text"]
        created_by = data["created_by"]
        assigned_to = data["assigned_to"]
        status_text = data["status_text"]
        _open = data["open"]
        _id = data["_id"]

        if not _open is None:
            _open = _open == 'True' or _open == 'true'

        raw_issue_list = IssueModel.find_by_filter(
            project_name=project_name,
            issue_title=issue_title,
            issue_text=issue_text,
            created_by=created_by,
            assigned_to=assigned_to,
            status_text=status_text,
            _open=_open,
            _id=_id,
        )
        return list(map(lambda raw_issue: raw_issue.json(), raw_issue_list))
