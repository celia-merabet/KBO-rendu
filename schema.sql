CREATE TABLE activity (
    code VARCHAR(20) PRIMARY KEY,
    label TEXT
);

CREATE TABLE enterprise (
    enterprise_number BIGINT PRIMARY KEY,
    status VARCHAR(50),
    juridical_form TEXT,
    type TEXT,
    language VARCHAR(5),
    start_date DATE,
    activity_code VARCHAR(20) REFERENCES activity(code)
);

CREATE TABLE establishment (
    establishment_number BIGINT PRIMARY KEY,
    enterprise_number BIGINT REFERENCES enterprise(enterprise_number) ON DELETE CASCADE,
    status VARCHAR(50),
    start_date DATE
);

CREATE TABLE denomination (
    id SERIAL PRIMARY KEY,
    enterprise_number BIGINT REFERENCES enterprise(enterprise_number) ON DELETE CASCADE,
    text TEXT,
    language VARCHAR(5),
    type TEXT
);

CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    entity_number BIGINT,
    entity_type VARCHAR(20),
    country TEXT,
    zip TEXT,
    city TEXT,
    street TEXT,
    number TEXT,
    box TEXT
);

CREATE TABLE branch (
    id SERIAL PRIMARY KEY,
    enterprise_number BIGINT REFERENCES enterprise(enterprise_number) ON DELETE CASCADE,
    nace_code VARCHAR(20)
);

CREATE TABLE contact (
    id SERIAL PRIMARY KEY,
    entity_number BIGINT,
    type TEXT,
    value TEXT
);
