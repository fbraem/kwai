-- migrate:up
create table if not exists users (
    id                      int unsigned auto_increment          primary key,
    email                   varchar(255)                         not null,
    password                varchar(255)                         not null,
    last_login              datetime                             null,
    first_name              varchar(255)                         null,
    last_name               varchar(255)                         null,
    remark                  text                                 null,
    uuid                    varchar(255)                         not null,
    created_at              datetime   default CURRENT_TIMESTAMP not null,
    updated_at              datetime                             null,
    member_id               int                                  null,
    revoked                 tinyint(1) default 0                 not null,
    last_unsuccessful_login datetime                             null,
    admin                   tinyint(1) default 0                 not null
) charset = utf8mb3;

create table if not exists user_recoveries
(
    id                  int unsigned auto_increment         primary key,
    user_id             int                                 not null,
    uuid                varchar(255)                        not null,
    expired_at          datetime                            not null,
    expired_at_timezone varchar(255)                        not null,
    confirmed_at        datetime                            null,
    remark              varchar(255)                        null,
    created_at          datetime  default CURRENT_TIMESTAMP not null,
    updated_at          datetime                            null,
    mailed_at           datetime                            null
) charset = utf8mb3;

create table if not exists oauth_access_tokens
(
    id         int unsigned auto_increment          primary key,
    identifier varchar(128)                         not null,
    user_id    int                                  not null,
    expiration timestamp                            null,
    revoked    tinyint(1) default 0                 not null,
    created_at datetime   default CURRENT_TIMESTAMP not null,
    updated_at datetime                             null
) charset = utf8mb3;

create table if not exists oauth_refresh_tokens
(
    id              int unsigned auto_increment          primary key,
    identifier      varchar(128)                         not null,
    access_token_id int                                  not null,
    expiration      datetime                             null,
    revoked         tinyint(1) default 0                 not null,
    created_at      datetime   default CURRENT_TIMESTAMP not null,
    updated_at      datetime                             null
) charset = utf8mb3;

create table if not exists user_invitations
(
    id                  int unsigned auto_increment          primary key,
    email               varchar(255)                         not null,
    first_name          varchar(255)                         not null,
    last_name           varchar(255)                         not null,
    uuid                varchar(255)                         not null,
    expired_at          datetime                             not null,
    expired_at_timezone varchar(255)                         not null,
    remark              text                                 null,
    user_id             int                                  not null,
    created_at          datetime   default CURRENT_TIMESTAMP not null,
    updated_at          datetime                             null,
    revoked             tinyint(1) default 0                 not null,
    confirmed_at        datetime                             null,
    mailed_at           datetime                             null
)
    charset = utf8mb3;

-- migrate:down
