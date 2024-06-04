from flask_wtf import FlaskForm
from wtforms import StringField

from src import db
from src.models.models import User, Posts, session_db, Group, user_group
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField, DateField, IntegerField
from wtforms.validators import DataRequired


def add_admin(app):
    admin = Admin(app, name="microblog", template_mode="bootstrap3")

    class PostForm(FlaskForm):
        @staticmethod
        def get_custom_choices():
            with app.app_context():
                with session_db() as s:
                    users = s.query(User).all()
                    return [(str(user.id), user.name) for user in users]

        title = StringField("Title", validators=[DataRequired()])
        body = StringField("Body", validators=[DataRequired()])
        user_id = SelectField(
            "User", choices=get_custom_choices, validators=[DataRequired()]
        )
        created = DateField("Created", validators=[DataRequired()])

    class GroupForm(FlaskForm):
        title = StringField("Title", validators=[DataRequired()])
        created = DateField("Created", validators=[DataRequired()])

    class UserGroupsForm(FlaskForm):
        user_id = IntegerField("User", validators=[DataRequired()])
        group_id = IntegerField("Group", validators=[DataRequired()])

    class PostAdminView(ModelView):
        can_view_details = True
        column_list = ["id", "title", "body", "user_id", "created"]
        form = PostForm  # Use the custom form class

    class UserAdminView(ModelView):
        can_view_details = True
        column_list = ["id", "name", "password", "comments", "groups"]
        form_columns = ["name", "password", "comments", "groups"]

    admin.add_view(PostAdminView(Posts, db.session))
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(ModelView(Group, db.session))
