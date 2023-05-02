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
    member_id               int                                  null
) charset = utf8mb3;

alter table users add (
    revoked                 tinyint(1) default 0                 not null,
    last_unsuccessful_login datetime                             null,
    admin                   tinyint(1) default 0                 not null
);

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
    confirmed_at        datetime                             null
)
    charset = utf8mb3;

alter table user_invitations add (
    mailed_at           datetime                             null
);

create table if not exists applications
(
  id                    int unsigned auto_increment          primary key,
  title                 varchar(255)                         not null,
  description           text                                 null,
  remark                text                                 null,
  created_at            datetime default CURRENT_TIMESTAMP   not null,
  updated_at            datetime                             null,
  short_description     varchar(255)                         not null,
  name                  varchar(255)                         not null,
  news                  tinyint(1) default 1                 not null,
  pages                 tinyint(1) default 1                 not null,
  events                tinyint(1) default 1                 not null,
  weight                int default 0                        not null
);

create table if not exists news_stories (
  id                    int unsigned auto_increment          primary key,
  enabled               tinyint(1) default 0                 not null,
  promotion             int default 0                        not null,
  promotion_end_date    datetime                             null,
  publish_date          datetime                             not null,
  timezone              varchar(255)                         not null,
  end_date              datetime                             null,
  remark                text                                 null,
  application_id        int unsigned                         not null,
  created_at            datetime default current_timestamp   not null,
  updated_at            datetime                             null
);

-- In kwai_api the table for news_contents was called news_contents_2,
create table if not exists news_contents_2 (
  news_id               int unsigned                         not null,
  locale                varchar(255)                         not null,
  format                varchar(255)                         not null,
  title                 varchar(255)                         not null,
  content               text,
  summary               text                                 not null,
  user_id               int                                  not null,
  created_at            datetime default CURRENT_TIMESTAMP   not null,
  updated_at            datetime                             null,
  primary key (news_id, locale)
);
-- Move news_contents_2 back to news_contents
drop table if exists news_contents;
CREATE TABLE news_contents LIKE news_contents_2;
INSERT INTO news_contents SELECT * FROM news_contents_2;
drop table if exists news_contents_2;
-- migrate:down
