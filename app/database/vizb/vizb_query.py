create_magento_table = """
CREATE TABLE IF NOT EXISTS magento (
	company_Id varchar PRIMARY KEY,
	CMS varchar,
	Access_Token varchar,
	Cleint_ID varchar,
	Client_Secret varchar, 
	Url varchar,
	Server varchar
);
"""

create_bigcomm_table = """
CREATE TABLE IF NOT EXISTS bigcommerce (
	company_Id varchar PRIMARY KEY,
	CMS_Store_Hash varchar,
	Access_Token varchar,
	Cleint_ID varchar,
	Client_Secret varchar,
	Server varchar
);
"""

create_mailchimp_table = """
CREATE TABLE IF NOT EXISTS mailchimp (
	company_Id varchar PRIMARY KEY,
	user_name varchar,
	api_key varchar
);
"""

create_status_table = """
CREATE TABLE IF NOT EXISTS status (
	company_Id varchar PRIMARY KEY,
	order_percentage varchar,
	customer_percentage varchar,
	status varchar
);
"""

create_kpi_table = """
CREATE TABLE IF NOT EXISTS kpi (
	company_Id varchar PRIMARY KEY,
	target_value float,
	current_value float,
	value_diff float,
	param_name varchar,
	year int,
	month varchar,
	month_num int,
	week_num float,
	from_date date,
	to_date date,
	is_current boolean
);
"""

create_table_query = [create_magento_table, create_bigcomm_table, create_status_table, create_kpi_table,
                      create_mailchimp_table]
