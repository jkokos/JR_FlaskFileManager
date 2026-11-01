

create table dokuments(
                 id serial primary key,
                 store_name varchar(128) not null unique,
                 original_name varchar(128) not null,
                 size_bytes bigint,
                 uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 extention VARCHAR(20)
                 
                 );