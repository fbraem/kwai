-- migrate:up

create table authors
(
    user_id          int unsigned primary key,
    name             varchar(255),
    remark           text,
    active           tinyint(1) default 1 not null,
    editor           tinyint(1) default 0 not null,
    created_at       datetime default CURRENT_TIMESTAMP not null,
    updated_at       datetime null
) charset = utf8mb3;

-- migrate:down
