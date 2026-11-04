from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ProductForm(FlaskForm):
    name = StringField('Назва товару', validators=[
        DataRequired(message="Введіть назву товару"),
        Length(min=2, max=50, message="Назва має бути від 2 до 50 символів")
    ])
    price = FloatField('Ціна (грн)', validators=[
        DataRequired(message="Введіть ціну"),
        NumberRange(min=0.01, message="Ціна повинна бути більше 0")
    ])
    amount = IntegerField('Кількість', validators=[
        DataRequired(message="Введіть кількість"),
        NumberRange(min=0, message="Кількість не може бути від'ємною")
    ])
    description = TextAreaField('Опис товару', validators=[
        Length(max=500, message="Опис не повинен перевищувати 500 символів")
    ])
    image = FileField('Зображення товару', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Дозволено тільки зображення (jpg, png, gif, webp)!')
    ])
    submit = SubmitField('Зберегти')