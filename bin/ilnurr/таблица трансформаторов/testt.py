import xlsxwriter

new_list = [['first', 'second'], ['third', 'four'], [1, 2, 3, 4, 5, 6]]

with xlsxwriter.Workbook('test.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(new_list):
        worksheet.write_row(row_num, 0, data)