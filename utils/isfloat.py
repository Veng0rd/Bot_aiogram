def isfloat(string) -> bool:
    """ Функция проверять string является ли она числом, возвращает bool """
    try:
        float(string)
    except ValueError:
        return False
    return True
