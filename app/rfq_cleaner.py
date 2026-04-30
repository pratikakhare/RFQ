def process_rfq_file(uploaded_file):
    import gc
    import os
    import tempfile
    import pandas as pd

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        temp_path = temp_file.name

    sheets = [
        'Aseem', 'Sunil', 'Samuel',
        'Kajal', 'Shraddha', 'Sonali',
        'Sachin', 'Rohan', 'Krushna'
    ]

    columns = None
    first = True

    try:
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx').name

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:

            for i, sheet in enumerate(sheets):

                if i == 0:
                    df = pd.read_excel(temp_path, sheet_name=sheet, header=7)
                    columns = list(df.columns)
                else:
                    df = pd.read_excel(temp_path, sheet_name=sheet, header=None, skiprows=8)

                    if df.shape[1] < len(columns):
                        for c in range(df.shape[1], len(columns)):
                            df[c] = None
                    elif df.shape[1] > len(columns):
                        df = df.iloc[:, :len(columns)]

                    df.columns = columns

                df.dropna(how='all', inplace=True)

                # CLEAN
                df = clean_rfq_dataframe(df)

                # WRITE (append style)
                df.to_excel(
                    writer,
                    index=False,
                    header=first,
                    startrow=writer.sheets['Sheet1'].max_row if not first else 0
                )

                first = False

                # free memory
                del df
                gc.collect()

        with open(output_path, 'rb') as out_file:
            content = out_file.read()

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(output_path):
            os.remove(output_path)

    return content
