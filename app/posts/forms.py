
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    DateTimeLocalField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):

    title = StringField(
        'Заголовок',
        validators=[
            DataRequired(),
            Length(min=3, max=150)
        ]
    )

    content = TextAreaField(
        'Текст публікації',
        validators=[
            DataRequired(),
            Length(min=5)
        ]
    )

    enabled = BooleanField(
        'Активний пост',
        default=True
    )

    publish_date = DateTimeLocalField(
        'Дата публікації',
        format='%Y-%m-%dT%H:%M',
        default=datetime.now
    )

    category = SelectField(
        'Категорія',
        choices=[
            ('news', 'Новини'),
            ('publication', 'Публікація'),
            ('tech', 'Технології'),
            ('other', 'Інше')
        ],
        default='other',
        validators=[DataRequired()]
    )

    submit = SubmitField('Зберегти')
