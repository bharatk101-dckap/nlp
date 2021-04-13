from app.ln2sql.ln2sql import Ln2sql
from app.database.data.psql import psql_to_df
from app.ln2sql.clean import text_clean
import numpy as np
import pandas as pd
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from functools import lru_cache


@lru_cache(maxsize=32)
def text_to_sql(text=None):
    ln2sql = Ln2sql(
        database_path="tbl.sql",
        language_path="english.csv",
    ).get_query(text)
    return ln2sql


def sda(company_Id, query, type_=None):
    try:
        input_ = text_clean(query)
        input_ = text_to_sql(text=input_)
        df = psql_to_df(company_Id, input_)
        df = df.replace(to_replace='None', value=np.nan).dropna().reset_index(drop=True)
        df.dropna(axis=0, inplace=True)
        df.rename(columns={"sum": "sales", "ds": "date", "yhat": "predicted", "just_date": "date",
                           "cust_segment": "customer_segment", "frequency": "order count"}, inplace=True)
        n_col = df.shape
        day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        # print(df)
        if type_ == "Table":
                columns = df.columns.tolist()
                for col in df.columns:
                    if df[col].dtype == np.float64 or df[col].dtype == np.float32:
                        df[col] = df[col].round(2)
                data = df.values.tolist()
                title = "Report"
                chart_type = ["Table"]
                data = {'data': data, 'columns': columns, 'type': chart_type, 'title': title}
        elif (type_ == "Bar Chart" or type_ == "Line Chart") and n_col == 2:
            if n_col[1] == 2 and 1 < n_col[0] < 51 and (np.int64 in list(df.dtypes) or np.int32 in list(df.dtypes) or
                                                        np.float64 in list(df.dtypes) or np.float32 in list(df.dtypes)):
                if list(df.dtypes)[0] == object and list(df.dtypes)[1] != object:
                    x = df.dtypes.index[0]
                    y = df.dtypes.index[1]
                    df[y] = df[y].round(2)
                elif list(df.dtypes)[1] == object and list(df.dtypes)[0] != object:
                    x = df.dtypes.index[1]
                    y = df.dtypes.index[0]
                    df[y] = df[y].round(2)
                elif list(df.dtypes)[1] != object and list(df.dtypes)[0] != object:
                    if str(df.dtypes[0]) == "datetime64[ns]":
                        x = df.dtypes.index[0]
                        y = df.dtypes.index[1]
                        df[y] = df[y].round(2)
                    elif str(df.dtypes[1]) == "datetime64[ns]":
                        x = df.dtypes.index[1]
                        y = df.dtypes.index[0]
                        df[y] = df[y].round(2)
                    else:
                        x = df.dtypes.index[1]
                        y = df.dtypes.index[0]
                        df[y] = df[y].round(2)
                        df[x] = df[x].round(2)
                else:
                    pass
                df = df.sort_values(by=x)
                if x == "day" and n_col[1] == 2 and n_col[0] == 7:
                    df[x] = day
                data = df.values.tolist()
                if str(df.dtypes[0]) == "datetime64[ns]":
                    chart_type = ['Line Chart']
                    graph_data = [{"x": data[i][0], "y": float(data[i][1])} for i in range(len(data))]
                else:
                    chart_type = ['Bar Chart', 'Line Chart']
                    graph_data = [{"x": data[i][1], "y": float(data[i][0])} for i in range(len(data))]
                title = f'{y} by {x}'
                x_label = x
                y_label = y
                data = {'data': graph_data, 'type': chart_type, 'title': title, 'x_label': x_label,
                        'y_label': y_label}
        else:
            if n_col[1] == 2 and 1 < n_col[0] < 51 and (np.int64 in list(df.dtypes) or np.int32 in list(df.dtypes) or
                                                        np.float64 in list(df.dtypes) or np.float32 in list(df.dtypes)):
                if list(df.dtypes)[0] == object and list(df.dtypes)[1] != object:
                    x = df.dtypes.index[0]
                    y = df.dtypes.index[1]
                    df[y] = df[y].round(2)
                elif list(df.dtypes)[1] == object and list(df.dtypes)[0] != object:
                    x = df.dtypes.index[1]
                    y = df.dtypes.index[0]
                    df[y] = df[y].round(2)
                elif list(df.dtypes)[1] != object and list(df.dtypes)[0] != object:
                    if str(df.dtypes[0]) == "datetime64[ns]":
                        x = df.dtypes.index[0]
                        y = df.dtypes.index[1]
                        df[y] = df[y].round(2)
                    elif str(df.dtypes[1]) == "datetime64[ns]":
                        x = df.dtypes.index[1]
                        y = df.dtypes.index[0]
                        df[y] = df[y].round(2)
                    else:
                        x = df.dtypes.index[1]
                        y = df.dtypes.index[0]
                        df[y] = df[y].round(2)
                        df[x] = df[x].round(2)
                else:
                    pass
                df = df.sort_values(by=x)
                if x == "day" and n_col[1] == 2 and n_col[0] == 7:
                    df[x] = day
                data = df.values.tolist()
                if str(df.dtypes[0]) == "datetime64[ns]":
                    chart_type = ['Line Chart']
                    graph_data = [{"x": data[i][0], "y": float(data[i][1])} for i in range(len(data))]
                else:
                    chart_type = ['Bar Chart', 'Line Chart']
                    graph_data = [{"x": data[i][1], "y": float(data[i][0])} for i in range(len(data))]
                title = f'{y} by {x}'
                x_label = x
                y_label = y
                data = {'data': graph_data, 'type': chart_type, 'title': title, 'x_label': x_label,
                        'y_label': y_label}
                # print("chart")
            elif n_col == (1, 1):
                data = str(round(df[df.dtypes.index[0]][0], 2))
                title = df.dtypes.index[0]
                chart_type = ['Card']
                data = {'data': data, 'type': chart_type, 'title': title}
                # print("card")
            else:
                columns = df.columns.tolist()
                for col in df.columns:
                    if df[col].dtype == np.float64 or df[col].dtype == np.float32:
                        df[col] = df[col].round(2)
                data = df.values.tolist()
                title = "Report"
                chart_type = ["Table"]
                data = {'data': data, 'columns': columns, 'type': chart_type, 'title': title}
                # print("table")
        # print(data)
        return JSONResponse(jsonable_encoder(data), status_code=200)
    except Exception as e:
        # df = pd.DataFrame(columns=["company_Id", "queries"])
        # df.to_csv("app/ln2sql/queries.csv", index=False)
        df = pd.read_csv("app/ln2sql/queries.csv")
        df = df.append({'company_Id': company_Id, 'queries': query}, ignore_index=True)
        df.to_csv("app/ln2sql/queries.csv", index=False)
        # print(df)
        return JSONResponse(content=jsonable_encoder({"data": [], "title": "NLP"}), status_code=203)
