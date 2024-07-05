# py -m eel main.py web --onefile --icon F:\PycharmProjects\sqlalchemy_models_generator\favicon.ico --hide-console minimize-late --name sa.models_generator
from eel import init, start, expose

from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, TIMESTAMP, DateTime, JSON, BigInteger


# Функция для маппинга типов данных
def map_column_type(column):
    if isinstance(column.type, Integer):
        return "Integer"
    elif isinstance(column.type, BigInteger):
        return "BigInteger"
    elif isinstance(column.type, String):
        if column.type.length:
            return f"String({column.type.length})"
        return "String"
    elif isinstance(column.type, Boolean):
        return "Boolean"
    elif isinstance(column.type, TIMESTAMP):
        return "TIMESTAMP"
    elif isinstance(column.type, DateTime):
        return "DateTime"
    elif isinstance(column.type, JSON):
        return "JSON"
    else:
        print(column.type)
        return "Other"


# Функция для генерации кода модели
def generate_model_code(table):
    class_name = table.name.capitalize()
    model_code = [f"class {class_name[:-1]}(Base):", f"    __tablename__ = '{table.name}'\n"]

    for column in table.columns:
        column_type = map_column_type(column)
        column_params = []

        # Проверяем, является ли колонка первичным ключом
        if column.primary_key:
            column_params.append("primary_key=True")

        # Проверяем, уникальная ли колонка
        if column.unique:
            column_params.append("unique=True")

        # Добавляем тип колонки
        column_params.append(f"{column_type}")

        # Проверяем, есть ли у колонки значение по умолчанию
        if column.default is not None:
            if callable(column.default.arg):
                default_value = column.default.arg.__name__ + '()'
            else:
                default_value = repr(column.default.arg)
            column_params.append(f"default={default_value}")

        # Проверяем, есть ли у колонки функция обновления
        if column.onupdate is not None:
            if callable(column.onupdate.arg):
                onupdate_value = column.onupdate.arg.__name__ + '()'
            else:
                onupdate_value = repr(column.onupdate.arg)
            column_params.append(f"onupdate={onupdate_value}")

        # Проверяем, является ли колонка внешним ключом
        if isinstance(column.foreign_keys, set) and column.foreign_keys:
            fk = list(column.foreign_keys)[0]
            column_params.append(f"ForeignKey('{fk.target_fullname}')")

        # Генерируем строку для колонки
        column_params_str = ", ".join(column_params)
        ct_mapped = "str" if column_type.startswith('String') else \
            "int" if column_type.startswith('Integer') else \
            "bool" if column_type.startswith('Boolean') else column_type
        model_code.append(f"    {column.name}: Mapped[{ct_mapped}] = mapped_column({column_params_str})")

    return "\n".join(model_code) + "\n"


@expose
def get_models(url):
    engine = create_engine(url, echo=True)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    models_code = []
    for table_name, table in metadata.tables.items():
        model_code = generate_model_code(table)
        models_code.append(model_code)

    return "\n".join(models_code)


def main():
    init('web')
    start('index.html', size=(900, 700), port=8008)


if __name__ == '__main__':
    main()
