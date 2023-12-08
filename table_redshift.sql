CREATE TABLE congress_data (
    prefix varchar(10),
    first_name varchar(30),
    last_name varchar(40),
    suffix varchar(10),
    name varchar(100),
    filling_date date,
    document_id int,
    year int,
    district varchar(20),
    source_ptr_link varchar(200),
    transcribed_by varchar(120),
    owner varchar(50),
    transaction_date  date,
    ticker varchar(20),
    description varchar(300),
    transaction_type varchar(50),
    amount varchar(100),
    cap_gains_over_200 boolean
)
;
