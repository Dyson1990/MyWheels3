def df_add2_excel(df0, output_path, sheet_name="data"):
    """
    输出数据为excel格式
    """
    if_exists = not os.path.exists(output_path)

    # 若文件不存在，则创建文件
    if if_exists:
        wb = openpyxl.Workbook()
        wb.create_sheet(index=0, title=sheet_name)
        wb.save(output_path)

    wb = openpyxl.load_workbook(output_path)
    sheet = wb[sheet_name]
    # 增加表头
    if if_exists:
        sheet.append(list(df0.columns))

    # 逐行插入
    for i0, row0 in df0.iterrows():
        sheet.append(row0.tolist())
    wb.save(output_path)
