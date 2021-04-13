import re
from datetime import datetime, timedelta
from calendar import monthrange
from word2number import w2n


sales = [{"year_month": ["Month", "month", "year_month"],
          "by year_month": ["monthly", "year_month"],
          "by Year": ["yearly", "Year"],
          "by Week": ["weekly", "Week"],
          "Year": ["Year", "year", "Year"],
          "Week": ["week", "Week", "Week"],
          "Day": ["day", "Day", "Day"],
          "by Day": ["daily", "Day"],
          "hour": ["hour", "Hour", "hour"],
          "email": ["customer", "Customer", "Customers", "customers", "client", "Client", "buyer", "Buyer", "email"],
          "name": ["product", "Product", "products", "Products", "name"],
          "country_iso2, by cc_code, by region": ["state", "State", "country_iso2, cc_code, region"],
          "country_iso2": ["location", "Location", "country_iso2"],
          "": ["sum", ""],
          "average": ["average", "Average", ""],
          "minimum": ["minimum", "Minimum", ""],
          "maximum": ["maximum", "Maximum", ""],
          "defaults": [" sum total", " of sales", ""]},
         {"just_date after": ["after", "After", "just_date"],
          "just_date before": ["before", "before", "just_date"],
          "just_date is": ["today", "Today", "yesterday", "Yesterday", "just_date"],
          "just_date between": ["last", "previous", "Last", "Previous", "this", "current", "just_date"],
          "defaults": [" total", " of sales", " order total decreasing"],
          "req": [" sum ", ", just_date", " by just_date, by total"]}]
orders = [{"year_month": ["Month", "month", "year_month"],
           "by year_month": ["monthly", "year_month"],
           "Year": ["Year", "year", "Year"],
           "Week": ["week", "Week", "Week"],
           "Day": ["day", "Day", "Day"],
           "hour": ["hour", "Hour", "hour"],
           "email": ["customer", "Customer", "client", "email"],
           "name": ["product", "Product", "name"],
           "country_iso2, by cc_code, by region": ["state", "State", "country_iso2, cc_code, region"],
           "country_iso2": ["location", "Location", "country_iso2"],
           "count unique ": ["sum", ""],
           "defaults": ["count order_id", " of sales", ""]},
          {"just_date after": ["after", "After", "just_date"],
           "just_date before": ["before", "before", "just_date"],
           "just_date is": ["today", "Today", "yesterday", "Yesterday", "just_date"],
           "just_date between": ["last", "previous", "Last", "Previous", "just_date"],
           "defaults": ["order_id", " of sales", ""],
           "req": [" count unique ", ", just_date", " by just_date"]}]
forecasting = [{"ds, yhat of sales_forecasting": ["sales", ""],
                "": ["predicted", "Predicted", "forecasted", ""],
                "ds after": ["after", "After", ""],
                "ds before": ["before", "before", ""],
                "ds is": ["today", "Today", "yesterday", "Yesterday", "tomorrow", ""],
                "ds between": ["last", "previous", "Last", "Previous", "this", "current", "next", ""],
                "defaults": ["", "", ""]},
               {"ds, yhat of churn_forecasting": ["churn", ""],
                "": ["predicted", "Predicted", "forecasted", ""],
                "ds after": ["after", "After", ""],
                "ds before": ["before", "before", ""],
                "ds is": ["today", "Today", "yesterday", "Yesterday", "tomorrow", ""],
                "ds between": ["last", "previous", "Last", "Previous", "this", "current", "next", ""],
                "defaults": ["", "", ""],
                "req": ["", "", ""]}]
customers = [{"cust_segment is 'High Spending-Loyal Customer'": ['High Spending-Loyal Customer', "cust_segment"],
              "cust_segment is 'High Spending-New Customer'": ['High Spending-New Customer', "cust_segment"],
              "cust_segment is 'Low Spending-New Customer'": ['Low Spending-New Customer', "cust_segment"],
              "cust_segment is 'Low Spending-Loyal Customer'": ['Low Spending-Loyal Customer', "cust_segment"],
              "cust_segment is 'High Spending-Potential Loyalist'": ['High Spending-Potential Loyalist', "cust_segment"],
              "cust_segment is 'Low Spending-Potential Loyalist'": ['Low Spending-Potential Loyalist', "cust_segment"],
              "cust_segment is 'High Spending-Promising Customer'": ['High Spending-Promising Customer', "cust_segment"],
              "cust_segment is 'Low Spending Promising Customer'": ['Low Spending Promising Customer', "cust_segment"],
              "cust_segment is 'High Spent-Attention Seekers'": ['High Spent-Attention Seekers', "cust_segment"],
              "cust_segment is 'Low Spent-Attention Seeker'": ['Low Spent-Attention Seeker', "cust_segment"],
              "cust_segment is 'High Spent-Likely to Churn'": ['High Spent-Likely to Churn', "cust_segment"],
              "cust_segment is 'Low Spent-Likely to Churn'": ['Low Spent-Likely to Churn', "cust_segment"],
              "cust_segment is 'High Spent-Churn Best Customer'": ['High Spent-Churn Best Customer', "cust_segment"],
              "cust_segment is 'Low Spent-Churn Best Customer'": ['Low Spent-Churn  Best Customer', "cust_segment"],
              "cust_segment is 'Churn Customer'": ['Churn Customer', "cust_segment"],
              "quad_segment is 'Platinum'": ['Platinum', "quad_segment"],
              "quad_segment is 'Gold'": ['Gold', "quad_segment"],
              "quad_segment is 'Silver'": ['Silver', "quad_segment"],
              "quad_segment is 'Bronze'": ['Bronze', "quad_segment"],
              "frequency, by email": ["order", "orders", "Order", "Orders", "frequency"],
              "monetary, by email": ["sales", "value", "monetary"],
              "count unique ": ["sum", "many", ""],
              "defaults": [" email", " of rfm", " order frequency decreasing"]},
             {"defaults": [" email", " of rfm", " order frequency decreasing"],
              "req": ["", ", frequency, monetary, avg_order_value", ""]}]
products = [{"qty_ordered, ": ["order", "orders", "Order", "Orders", "ordered", "sum qty_ordered"],
             "price, by qty_ordered order price decreasing": ["price", "value", "price"],
             "price_total, by qty_ordered ": ["sales", "Sales", "sum price_total"],
             "count unique ": ["sum", ""],
             "defaults": [" name", " of payments", " by name, order qty_ordered decreasing"]},
            {"defaults": [" unique name", " of payments", ""],
             "req": ["", ", price, qty_ordered", " order qty_ordered decreasing"]}]
dict_ = {"sale": sales, "sales": sales, "revenue": sales, "value": sales, "business": sales, "Business": sales,
         "order": orders, "orders": orders,
         "predicted": forecasting, "Predicted": forecasting, "forecasted": forecasting, "forecasting": forecasting, "expected": forecasting,
         "customer": customers, "customers": customers, "clients": customers, "client": customers, "buyer": customers, "Buyer": customers,
         "products": products, "product": products}


def text_clean(input_):
    tokens = [i.strip() for i in input_.strip().split(" ") if len(i.strip()) > 0]
    val = ["last", "previous", "today", "yesterday", "before", "this", "current", 'next', 'tomorrow']
    by_alt = ["monthly", "daily", "yearly", "weekly"]
    for e, i in enumerate(tokens):
        try:
            res = w2n.word_to_num(i)
            if type(res) == int:
                tokens[e] = str(res)
        except:
            continue
    r_1 = False
    for e, i in enumerate(tokens):
        if i in val:
            if True in [True for t in tokens[:e] if t in dict_.keys()]:
                for x, j in enumerate(tokens):
                    if j.lower() in dict_.keys() and j.lower() not in ["predicted", "forecasted", "forecasting",
                                                                       "expected"]:
                        if x + 1 < len(tokens) and tokens[x + 1] not in val:
                            r_1 = True
                            tokens = tokens[:x + 1] + tokens[e:] + tokens[x + 1:e]
                            break
            else:
                for x, j in enumerate(tokens):
                    if j.lower() in dict_.keys() and j.lower() not in ["predicted", "forecasted", "forecasting",
                                                                       "expected"]:
                        tokens = [" ".join(tokens[:e]).replace(tokens[x], "")] + [tokens[x]] + [
                            " ".join(tokens[e:]).replace(tokens[x], "")]
                        r_1 = True
                        break
            break
    if not r_1:
        for e, i in enumerate(tokens):
            if i in by_alt:
                for x, j in enumerate(tokens):
                    if j.lower() in dict_.keys() and j.lower() not in ["predicted", "forecasted", "forecasting",
                                                                       "expected"]:
                        tokens = [" ".join(tokens[:e]).replace(tokens[x], "")] + [tokens[x]] + [
                            " ".join(tokens[e:]).replace(tokens[x], "")]
                        r_1 = True
                        break
                break
    input_ = " ".join(tokens)
    input_ = re.sub("\s[pP]er", " by", input_)
    input_ = re.sub("[tT]otal\s|[gG]ross", "sum ", input_)
    if re.search("[cC]ustomer.{0,1}", input_) != None:
        input_ = re.sub("\s[gG]old", " 'Gold'", input_)
        input_ = re.sub("\s[sS]ilver", " 'Silver'", input_)
        input_ = re.sub("\s[bB]ronze", " 'Bronze'", input_)
        input_ = re.sub("\s[pP]latinum", " 'Platinum'", input_)
        input_ = re.sub("high spending-loyal customer", "'High Spending-Loyal Customer'", input_)
        input_ = re.sub("high spending-potential loyalist", "'High Spending-Potential Loyalist'", input_)
        input_ = re.sub("high spending-new customer", "'High Spending-New Customer'", input_)
        input_ = re.sub("high spending-loyal customer", "'High Spending-Loyal Customer'", input_)
        input_ = re.sub("high spending-promising customer", "'High Spending-Promising Customer'", input_)
        input_ = re.sub("high spent-attention seekers", "'High Spent-Attention Seekers'", input_)
        input_ = re.sub("high spent-likely to churn", "'High Spent-Likely to Churn'", input_)
        input_ = re.sub("high spent-churn best customer", "'High Spent-Churn Best Customer'", input_)
        input_ = re.sub("low spending-new customer", "'Low Spending-New Customer'", input_)
        input_ = re.sub("low spending-loyal customer", "'Low Spending-Loyal Customer'", input_)
        input_ = re.sub("low spending-potential loyalist", "'Low Spending-Potential Loyalist'", input_)
        input_ = re.sub("low spending promising customer", "'Low Spending Promising Customer'", input_)
        input_ = re.sub("low spent-attention seeker", "'Low Spent-Attention Seeker'", input_)
        input_ = re.sub("low spent-churn best customer", "'Low Spent-Churn Best Customer'", input_)
        input_ = re.sub("churn customer", "'Churn Customer'", input_)
    now = datetime.now().date()
    y = datetime.strptime(str(now.year) + "-01-01", "%Y-%m-%d").date()
    m = datetime.strptime(str(now.year) + "-" + str(now.month) + "-01", "%Y-%m-%d").date()
    y_d = abs((y - now).days)
    m_d = abs((m - now).days)
    p_md = 0
    check = re.search(
        r"[jJ]an.{0,4}|[fF]eb.{0,5}|[mM]ar.{0,2}|[aA]pr.{0,2}|[mM]ay|[jJ]un.{0,1}|[jJ]ul.{0,1}|[aA]ug.{0,3}|[sS]ep.{0,6}|[oO]ct.{0,4}|[nN]ov.{0,5}|[dD]ec.{0,5}",
        input_)
    if check:
        p_m = datetime.strptime(str(now.year - 1) + "-" + check.group().strip()[:3] + "-01", "%Y-%b-%d").date()
        p_md = abs((p_m - now).days)
    if True in list(map(lambda x: True if x in input_.lower() else False,
                        ["last", "previous", "today", "yesterday", "before", "this", "current", "next", "tomorrow"])):
        pattern = r"(\d+\s)*([yY]ear(?!ly)|[mM]onth(?!ly)|[wW]eek(?!ly)|[dD]ay.{0,1}|[hH]our.{0,1}|[tT]oday.{0}|[yY]esterday.{0}|[tT]omorrow.{0}|[jJ]an.{0,4}|[fF]eb.{0,5}|[mM]ar.{0,2}|[aA]pr.{0,2}|[mM]ay|[jJ]un.{0,1}|[jJ]ul.{0,1}|[aA]ug.{0,3}|[sS]ep.{0,6}|[oO]ct.{0,4}|[nN]ov.{0,5}|[dD]ec.{0,5})"
        values = {"year": 365 + y_d, "years": 365 + y_d, "month": 30 + m_d, "months": 30 + m_d, "week": 7, "weeks": 7,
                  "day": 1, "days": 1, "hour": 1, "hours": 1,
                  "today": 0, "yesterday": 1, "tomorrow": 1, "jan": p_md, "january": p_md, "feb": p_md,
                  "february": p_md, "mar": p_md, "march": p_md, "apr": p_md, "april": p_md, "may": p_md,
                  "jun": p_md, "june": p_md, "jul": p_md, "july": p_md, "aug": p_md, "august": p_md, "sep": p_md,
                  "september": p_md, "oct": p_md, "october": p_md, "nov": p_md, "november": p_md, "dec": p_md, "december": p_md}
        num = 0
        match = re.search(pattern, input_)
        if match != None:
            iden = match
            str_ = match.group().strip()
            match = match.group().split(" ")
            if "" in match: match.remove("")
            if len(match) == 2:
                if match[1][0].lower() != "h":
                    num = int(match[0]) * values[match[1].lower()]
                elif match[0] == "24":
                    num = values[match[1].lower()]
                if match[1].lower() in ["year", "years"]:
                    if "next" in input_.lower().split(" "):
                        input_ = re.sub(str_, str(y + timedelta(365)) + " and " + str(y + timedelta((int(match[0])+1)*365)), input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                    else:
                        input_ = re.sub(str_, str(now - timedelta(num)) + " and " + str(y - timedelta(1)), input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                elif match[1].lower() in ["month", "months"]:
                    if "next" in input_.lower().split(" "):
                        input_ = re.sub(str_, str(m + timedelta(30)) + " and " + str(m + timedelta((int(match[0])+1)*30)), input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                    else:
                        input_ = re.sub(str_, str(now - timedelta(num)) + " and " + str(m - timedelta(1)), input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                else:
                    input_ = re.sub(str_, str(now - timedelta(num)) + " and " + str(now), input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
            elif len(match) == 1:
                num = values[match[0]]
                if str_.lower() in ["today"]:
                    input_ = re.sub(str_, "today " + str(now - timedelta(num)) + " ", input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                elif True in list(map(lambda x: True if x in input_.lower() else False,
                                      ["this", "current"])) and str_.lower() in ["year", "years"]:
                    input_ = re.sub(str_, str(y) + " and " + str(now) + " ", input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                elif True in list(map(lambda x: True if x in input_.lower() else False,
                                      ["this", "current"])) and str_.lower() in ["month", "months"]:
                    input_ = re.sub(str_, str(m) + " and " + str(now) + " ", input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                elif str_.lower() in ["yesterday"]:
                    input_ = re.sub(str_, "yesterday " + str(now - timedelta(num)) + " ", input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                elif str_.lower() in ["tomorrow"]:
                    input_ = re.sub(str_, "tomorrow " + str(now + timedelta(num)) + " ", input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                elif str_.lower() in ["year", "years"]:
                    if "next" in input_.lower().split(" "):
                        input_ = re.sub(str_, str(y + timedelta(365)) + " and " + str(y + timedelta(2*365)), input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                    else:
                        input_ = re.sub(str_, str(now - timedelta(num)) + " and " + str(y - timedelta(1)), input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                elif str_.lower() in ["month", "months"]:
                    if "next" in input_.lower().split(" "):
                        input_ = re.sub(str_, str(m + timedelta(30)) + " and " + str(m + timedelta(2*30)), input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                    else:
                        if (now - timedelta(num)).day == 1:
                            t1 = now - timedelta(num)
                        else:
                            t = now - timedelta(num)
                            for i in range(1, 5):
                                if (t + timedelta(i)).day == 1:
                                    t1 = t + timedelta(i)
                                    break
                        input_ = re.sub(str_, str(t1) + " and " + str(m - timedelta(1)), input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                elif re.search(
                        r"[jJ]an.{0,4}|[fF]eb.{0,5}|[mM]ar.{0,2}|[aA]pr.{0,2}|[mM]ay|[jJ]un.{0,1}|[jJ]ul.{0,1}|[aA]ug.{0,3}|[sS]ep.{0,6}|[oO]ct.{0,4}|[nN]ov.{0,5}|[dD]ec.{0,5}",
                        str_.lower()):
                    d = now - timedelta(num)
                    input_ = re.sub(str_,
                                    str(d) + " and " + str(d + timedelta(monthrange(d.year, d.month)[1] - 1)) + " ",
                                    input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                elif str_.lower() in ["week", "weeks"]:
                    if "next" in input_.lower().split(" "):
                        con1 = (now + timedelta(num)).strftime("%A") == 'Monday'
                        if con1:
                            t1 = now + timedelta(num)
                            t2 = t1 + timedelta(num-1)
                        else:
                            num_day = (now + timedelta(num)).weekday()
                            for i in range(0, 7):
                                if num_day - i == 0:
                                    td_num = i
                                    break
                            t1 = now + timedelta(num) - timedelta(td_num)
                            t2 = t1 + timedelta(num-1)
                        input_ = re.sub(str_, str(t1) + " and " + str(t2) + " ",
                                        input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
                    else:
                        con1 = (now - timedelta(num)).strftime("%A") == 'Monday'
                        if con1:
                            t1 = now - timedelta(num)
                            t2 = t1 + timedelta(num - 1)
                        else:
                            num_day = (now - timedelta(num)).weekday()
                            for i in range(0, 7):
                                if num_day - i == 0:
                                    td_num = i
                                    break
                            t1 = now - timedelta(num) - timedelta(td_num)
                            t2 = t1 + timedelta(num - 1)
                        input_ = re.sub(str_, str(t1) + " and " + str(t2) + " ",
                                        input_[:iden.span()[1] + 1]) + input_[iden.span()[1]+1:]
                else:
                    input_ = re.sub(str_, str(now - timedelta(num)) + " and " + str(now) + " ",
                                    input_[:iden.span()[1]+1]) + input_[iden.span()[1]+1:]
        else:
            pass

    if re.search(r"['']", input_.strip()) != None:
        pos = input_.find("'")
        tokens_1 = [i.strip() for i in input_[pos:].strip().split("'") if len(i.strip()) > 0]
        tokens_2 = [i.strip() for i in input_[:pos].strip().split(" ") if len(i.strip()) > 0]
        tokens = tokens_2 + tokens_1
        input_ = " ".join(tokens)
    else:
        tokens = [i.strip() for i in input_.strip().split(" ") if len(i.strip()) > 0]

    cnt = 0
    for e, i in enumerate(tokens[::-1]):
        keys = list(tokens[::-1])
        keys.remove(i)
        num = len([True for d in tokens if d in dict_.keys()])
        for j in dict_.keys():
            c1 = re.search(r"^[pP]roduct.{0,1}|^[cC]ustomer.{0,1}|^[sS]ale.{0,1}|[oO]rder.{0,1}|"
                           r"^[rR]evenue|^[bB]uyer|^[cC]lient.{0,1}", i.strip()) == None
            c2 = len([True for c in keys if re.match(r"[pP]redict.*|[fF]orecast.*|by|per", c) != None]) == 0
            if i == j: cnt += 1
            if (i == j and c1 == True and c2 == True) or (i == j and c1 == True) or \
                    (i == j and c1 == False and c2 == False and cnt == num) or \
                    (i == j and len([True for u in tokens if u in dict_.keys()]) <= 1):
                cnt = 0
                start = dict_[i][0]["defaults"][0]
                chk = [True for i in tokens if i.lower().strip() in ("daily", "monthly", "weekly", "yearly")]
                if "by" not in tokens and "sum" not in tokens and True not in chk:
                    start = re.sub("sum\s", " ", start)
                end = dict_[i][0]["defaults"][1]
                end_ = dict_[i][0]["defaults"][2]
                final = ""
                for k in tokens:
                    for l in dict_[i][0].keys():
                        if k in dict_[i][0][l][:-1]:
                            input_ = input_.replace(k, l)
                            final += ", " + dict_[i][0][l][-1]
                if final:
                    for m in tokens:
                        for n in dict_[i][1].keys():
                            if m in dict_[i][1][n][:-1]:
                                input_ = input_.replace(m, n)
                    if "unique" not in input_:
                        input_ = re.sub(r"\s" + i + "|^" + i, start + final + end, input_) + end_
                    else:
                        input_ = re.sub(r"\s" + i + "|^" + i, start + final + end, input_)
                else:
                    start = dict_[i][1]["defaults"][0]
                    end = dict_[i][1]["defaults"][1]
                    mid_start = dict_[i][1]["req"][0]
                    mid = dict_[i][1]["req"][1]
                    mid_end = dict_[i][1]["req"][2]
                    end_ = dict_[i][1]["defaults"][2]
                    for m in tokens:
                        for n in dict_[i][1].keys():
                            if m in dict_[i][1][n][:-1]:
                                input_ = input_.replace(m, n)
                                final += ", " + dict_[i][1][n][-1]
                    if final:
                        input_ = re.sub(r"\s"+i+"|^"+i, start+final+end, input_) + end_
                    else:
                        input_ = re.sub(r"\s"+i+"|^"+i, mid_start+start+mid+end+mid_end, input_) + end_

    input_ = input_.strip()
    return input_
