import inspect

def remove_comments_and_update_file():
    """
    Удаляет комментарии из файла, в котором вызвана функция, и перезаписывает его.
    """
    frame = inspect.currentframe().f_back
    file_path = frame.f_globals["__file__"]

    with open(file_path, "r", encoding="utf-8") as file:
        code_with_comments = file.read()

    cleaned_code = remove_hash_comments(code_with_comments)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cleaned_code)

    print(f"Файл {file_path} успешно перезаписан без комментариев.")


def remove_hash_comments(code):
    """
    Удаляет комментарии из кода Python, начинающиеся с символа #.

    :param code: Строка с кодом Python
    :return: Строка кода без комментариев
    """
    lines = code.splitlines()  
    cleaned_lines = []

    for line in lines:
        comment_index = line.find("#")
        if comment_index != -1:
            if not is_inside_string(line, comment_index):
                line = line[:comment_index].rstrip()
        
        if line.strip():
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def is_inside_string(line, index):
    """
    Проверяет, находится ли символ # внутри строки.

    :param line: Строка кода
    :param index: Индекс символа #
    :return: True, если символ # находится внутри строки, иначе False
    """
    in_single_quote = False
    in_double_quote = False

    for i in range(index):
        if line[i] == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif line[i] == '"' and not in_single_quote:
            in_double_quote = not in_double_quote

    return in_single_quote or in_double_quote


if __name__ == "__main__":
    remove_comments_and_update_file()
