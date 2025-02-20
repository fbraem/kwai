-- migrate:up

create table user_logs
(
    id               int unsigned auto_increment primary key,
    email            varchar (255) default '',
    user_id          int unsigned,
    refresh_token_id int unsigned,
    success          tinyint(1) default 0 not null,
    client_ip        varchar (45) not null,
    user_agent       varchar (512) not null,
    openid_sub       varchar (255) default '',
    openid_provider  varchar (255) default '',
    remark           text,
    created_at       datetime default CURRENT_TIMESTAMP not null
) charset = utf8mb3;
create index user_logs_refresh_token
    on user_logs(refresh_token_id)
;
-- migrate:down
