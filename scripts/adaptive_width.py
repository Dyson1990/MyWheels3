def adaptive_width(file_path):
    """
    将Excel中所有sheet的所有列设为宽度自适应
    中文的话，需要encode('gbk')才能正确找到合适宽度，目前只支持调整文本
    """
    wb = openpyxl.load_workbook(file_path)
    for worksheet in wb.worksheets:
        for col in worksheet.columns:
            column_letter = col[0].column_letter
            try:
                max_len = max((len(row.value) for row in col if isinstance(row.value, str)))
                worksheet.column_dimensions[column_letter].width = max_len + 2
            except:
                pass
    wb.save(file_path)
