import logging

import allure
import pandas as pd


@allure.step("Читаем таблицу и отдаем значение")
def read_exel():
    file = './downloads/products.xlsx'
    xl = pd.ExcelFile(file)
    df = xl.parse('products')
    filter_ = ["NaN", "NO NAME", "БЕЗ БРЕНДА"]
    test = df.loc[:, ['SAP ID', 'Название']].dropna()
    test2 = test.loc[~test["Название"].isin(filter_)].head()
    list_data = test2.to_dict('split').get('data')
    res = []
    for el in list_data:
        k = r'	'.join([str(elem) for elem in el])
        res.append(k)
    return res


@allure.step('Проверка что файл скачался и скачался корректно')
def check_download_excel(path, response, sheet=None):
    try:
        with open(path, "wb") as file:
            file.write(response.content)
        pd.ExcelFile(path)
    except Exception as e:
        logging.exception(e.__name__)
        raise AssertionError
