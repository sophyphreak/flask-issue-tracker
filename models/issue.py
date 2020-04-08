from db import db
import datetime
import arrow


class IssueModel(db.Model):
    __tablename__ = "issue"
    _id = db.Column(db.Integer, primary_key=True)
    issue_title = db.Column(db.String(80))
    issue_text = db.Column(db.String(80))
    created_by = db.Column(db.String(80))
    assigned_to = db.Column(db.String(80))
    status_text = db.Column(db.String(80))
    _open = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    project_name = db.Column(db.String(80))

    def __init__(
        self,
        issue_title,
        issue_text,
        created_by,
        assigned_to,
        status_text,
        _open,
        created_on,
        project_name,
    ):
        self.issue_title = issue_title
        self.issue_text = issue_text
        self.created_by = created_by
        self.assigned_to = assigned_to
        self.status_text = status_text
        self._open = _open
        self.created_on = created_on
        self.updated_on = created_on
        self.project_name = project_name

    def json(self):
        return {
            "_id": self._id,
            "issue_title": self.issue_title,
            "issue_text": self.issue_text,
            "created_by": self.created_by,
            "assigned_to": self.assigned_to,
            "status_text": self.status_text,
            "open": self._open,
            "created_on": self.created_on.isoformat(),
            "updated_on": self.updated_on.isoformat(),
            "project_name": self.project_name,
        }

    @classmethod
    def find_by_filter(
        cls,
        project_name,
        issue_title,
        issue_text,
        created_by,
        assigned_to,
        status_text,
        _open,
        _id,
    ):
        query = cls.query.filter_by(project_name=project_name)
        if not issue_title is None:
            query = query.filter_by(issue_title=issue_title)
        if not issue_text is None:
            query = query.filter_by(issue_text=issue_text)
        if not created_by is None:
            query = query.filter_by(created_by=created_by)
        if not assigned_to is None:
            query = query.filter_by(assigned_to=assigned_to)
        if not status_text is None:
            query = query.filter_by(status_text=status_text)
        if not _open is None:
            query = query.filter_by(_open=_open)
        if not _id is None:
            query = query.filter_by(_id=_id)

        return query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
