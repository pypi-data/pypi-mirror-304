from datetime import datetime
import re


class ConvertValueException(Exception): ...


class PreActionException(Exception): ...


class ConvertToFloatException(Exception): ...


class ConvertToIntException(Exception): ...


def pre_action(value, func, *args, **kwargs):
    """
    Запуск пользовательской функции

    :param value: данные
    :param func: пользовательская функция
    :return: обработанные пользовательской функцией данные
    """
    try:
        return func(value, *args, **kwargs)
    except Exception as e:
        raise PreActionException(e)


def to_float(
    value: str | bool | int | float,
    additional_info=None,
    pre_convert_func=None,
    *args,
    **kwargs,
):
    """
    Преревод значения в тип float
    Замена строковой запятой (,) на строковую точку.
    Удаляет пропуски

    :param pre_convert_func: пользовательская функция, вызываемая до конвертации
    :param value: строковое значение
    :return: float
    """

    if pre_convert_func:
        value = pre_action(value, pre_convert_func, *args, **kwargs)

    if value is None or value == "":
        return 0.0

    if isinstance(value, float):
        return value

    if isinstance(value, int):
        return float(value)

    if isinstance(value, bool):
        return 1, 0 if value else 0, 0

    if isinstance(value, str):
        if value.upper() == "TRUE":
            return 1.0
        elif value.upper() == "FALSE":
            return 0.0

        # Удаляем все пробелы и неразрывные пробелы
        value = re.sub(r"[\s\xa0\x20]+", "", value)

        # Заменяем первую запятую на точку
        value = re.sub(r",", ".", value, 1)

        try:
            return float(value)
        except Exception as e:
            raise ConvertToFloatException(e)


def to_int(
    value: str | bool | float | int,
    bankers_rounding: bool = True,
    pre_convert_func=None,
    *args,
    **kwargs,
):
    """
    Пререводит значение в тип int. Банковское округление.

    Значения с плавающей точкой нужно сначала перевести во float формат.


    :param value:
    :param pre_convert_func:
    :param bankers_rounding: алгоритм банковского округления
    :param args:
    :param kwargs:
    :return: int
    """
    if pre_convert_func:
        value = pre_action(value, pre_convert_func, *args, **kwargs)

    try:
        if bankers_rounding:
            return round(to_float(value, pre_convert_func, *args, **kwargs))
        else:
            return int(to_float(value, pre_convert_func, *args, **kwargs))
    except Exception as e:
        raise ConvertToIntException(e)


# TODO
def to_str(value, additional_info=None):
    return str(value)


# TODO
def to_bool(value, additional_info=None):
    return bool(value)


# TODO
def to_datetime(value, additional_info):
    try:
        return datetime.strptime(value, additional_info)  # .isoformat()
    except ValueError:
        return None


# TODO
# Основная функция для преобразования значений
def convert_value(value, column_type, additional_info=None):
    converters = {
        "float": to_float,
        "int": to_int,
        "str": to_str,
        "bool": to_bool,
        "datetime": to_datetime,
    }
    if column_type in converters:
        try:
            return converters[column_type](value, additional_info)
        except Exception as e:
            raise ConvertValueException(e)
    else:
        return value
