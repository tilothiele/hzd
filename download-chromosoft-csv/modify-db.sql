CREATE TABLE members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    person_id INT,
    access TINYINT(1),
    salutation VARCHAR(10),
    title VARCHAR(50),
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    language VARCHAR(20),
    street VARCHAR(100),
    zipcode VARCHAR(20),
    city VARCHAR(50),
    oblast VARCHAR(50),
    country VARCHAR(50),
    organization VARCHAR(100),
    mobile VARCHAR(50),
    phone VARCHAR(50),
    email VARCHAR(100),
    internet VARCHAR(100),
    type_of_person VARCHAR(50),
    is_breeder TINYINT(1),
    is_member TINYINT(1),
    is_subscriber TINYINT(1),
    type_of_subscription VARCHAR(200),
    is_active_breeder TINYINT(1),
    breeding_station VARCHAR(100),
    given_name_first VARCHAR(50),
    membership_number INT,
    membership_status VARCHAR(50),
    role_in_association VARCHAR(50),
    other_roles VARCHAR(100),
    date_of_birth DATE,
    date_of_death DATE,
    date_of_joining DATE,
    date_of_leaving DATE,
    iban VARCHAR(34),
    bic VARCHAR(12)
);

alter table members add column begruesst_am DATE;

-- erstmal alle einträge aktualisieren
update members set begruesst_am = CURRENT_DATE();

create unique index idx_membership_number on members (membership_number);
