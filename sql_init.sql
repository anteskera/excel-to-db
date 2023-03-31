CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE weekly_report (
	id uuid DEFAULT uuid_generate_v4 (),
	store_no VARCHAR(20) UNIQUE NOT NULL,
	store_name VARCHAR(50) UNIQUE NOT NULL,
	ty_units INTEGER,
	ly_units INTEGER,
	tw_sales REAL,
	lw_sales REAL,
	lw_var_pct REAL,
	ly_sales REAL,
	ly_var_pct REAL,
	ytd_sales REAL,
	lytd_sales REAL,	
	lytd_var_pct REAL
)
