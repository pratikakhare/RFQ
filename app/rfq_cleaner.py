def process_rfq_file(uploaded_file):
    import pandas as pd
    from io import BytesIO

    valid_sheets = [
        'Aseem','Sunil','Samuel','Kajal',
        'Shraddha','Sonali','Sachin','Rohan','Krushna'
    ]

    xls = pd.ExcelFile(uploaded_file)
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        sheet_written = False

        for sheet in xls.sheet_names:
            if sheet in valid_sheets:
                df = xls.parse(sheet)

                # 🔥 IMPORTANT FIX
                if df.empty:
                    df = pd.DataFrame({'Message': ['No data available']})

                df.to_excel(writer, sheet_name=sheet, index=False)
                sheet_written = True

        # 🔥 FINAL SAFETY (VERY IMPORTANT)
        if not sheet_written:
            pd.DataFrame({'Message': ['No valid sheets found']}).to_excel(
                writer, sheet_name='Sheet1', index=False
            )

    output.seek(0)
    return output.getvalue()
