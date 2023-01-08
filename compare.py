import sys
import ast
import numpy as np


def levenshtein(text_base: list, text_compared: list) -> int:
    distances = np.zeros((len(text_base) + 1, len(text_compared) + 1))

    for j in range(1, len(text_compared) + 1):
        distances[0][j] = j

    for i in range(1, len(text_base) + 1):
        distances[i][0] = i

    for i in range(1, len(text_base) + 1):
        for j in range(1, len(text_compared) + 1):
            if text_base[i - 1] == text_compared[j - 1]:
                distances[i][j] = distances[i - 1][j - 1]
            else:
                distances[i][j] = min(distances[i][j - 1], distances[i - 1][j], distances[i - 1][j - 1]) + 1

    return distances[len(text_base)][len(text_compared)]


def get_text(file_path: str):
    with open(file_path, 'r') as file:
        return file.read()


def get_prepared_text(text: str) -> list:
    """
        Удалим все комментарии в коде, заменим названия переменных на одно,
        чтобы они не влияли на расстояние Левенштейна.
    """

    ast_module = ast.parse(text)
    all_variables_name = [node.id for node in ast.walk(ast_module) if
                          isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load)]
    all_functions_name = [node.name for node in ast.walk(ast_module) if isinstance(node, ast.FunctionDef)]

    result = ast.unparse(ast_module)

    for t in sorted(set(all_variables_name +
                        all_functions_name), key=len, reverse=True):
        result = result.replace(t, '~~$$eqexpr~~$$')

    return result.split()


def compare(file_path_1: str, file_path_2: str):
    file_text_1 = get_text(file_path_1)
    file_text_2 = get_text(file_path_2)

    text_list_1 = get_prepared_text(file_text_1)
    text_list_2 = get_prepared_text(file_text_2)

    max_len = max(len(text_list_1), len(text_list_2))

    result = 1 - (levenshtein(text_list_1, text_list_2) / max_len)

    return round(result, 2)


def main(input_filename, output_filename):
    raw = open(input_filename, 'r').read()
    result = []
    for t in raw.strip().split('\n'):
        file_1, file_2 = t.split()
        result.append(compare(file_1, file_2))
    result_text = '\n'.join(map(str, result))
    with open(output_filename, 'w') as output_file:
        output_file.write(result_text)


if __name__ == '__main__':
    input_str, output_str = sys.argv[1:3]
    main(input_str, output_str)