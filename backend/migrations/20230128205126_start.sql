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
alter table users rename column member_id to person_id;

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
alter table user_recoveries drop column expired_at_timezone;


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
    name                varchar(255)                         not null,
    uuid                varchar(255)                         not null,
    expired_at          datetime                             not null,
    expired_at_timezone varchar(255)                         not null,
    remark              text                                 null,
    user_id             int                                  not null,
    created_at          datetime   default CURRENT_TIMESTAMP not null,
    updated_at          datetime                             null,
    revoked             tinyint(1) default 0                 not null,
    confirmed_at        datetime                             null
) charset = utf8mb3;
alter table user_invitations drop column expired_at_timezone;
alter table user_invitations drop column name;

alter table user_invitations add (
    mailed_at           datetime                             null,
    first_name          varchar(255)                         not null,
    last_name           varchar(255)                         not null
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
) charset = utf8mb3;
alter table applications add constraint uq_name unique(name);
insert ignore applications
(
  title,
  description,
  remark,
  short_description,
  name,
  news,
  pages,
  events,
  weight
) values
( 'Club', '', '', '', 'club', 1, 1, 1, 0 ),
( 'Trainings', '', '', '', 'trainings', 1, 1, 1, 0 ),
( 'Tournaments', '', '', '', 'tournaments', 1, 1, 1, 0 ),
( 'Activities', '', '', '', 'activities', 1, 1, 1, 0 ),
( 'Judo', '', '', '', 'judo', 1, 1, 1, 0 ),
( 'Shop', '', '', '', 'shop', 1, 1, 1, 0 ),
( 'News', '', '', '', 'news', 0, 0, 0, 0 ),
( 'Calendar', '', '', '', 'events', 0, 0, 0, 0 )
;

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
) charset = utf8mb3;
alter table news_stories drop column timezone;

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
) charset = utf8mb3;

-- Move news_contents_2 back to news_contents
drop table if exists news_contents;
CREATE TABLE news_contents LIKE news_contents_2;
INSERT INTO news_contents SELECT * FROM news_contents_2;
drop table if exists news_contents_2;

create table if not exists trainings (
    id                  int unsigned auto_increment          primary key,
    definition_id       int unsigned                         null,
    season_id           int unsigned                         null,
    created_at          timestamp default current_timestamp  not null,
    updated_at          timestamp                            null,
    start_date          datetime                             not null,
    end_date            datetime                             not null,
    time_zone           varchar(255)                         not null,
    active              tinyint(1) default 1                 not null,
    cancelled           tinyint(1) default 0                 not null,
    location            varchar(255)                         null,
    remark              text                                 null
) charset = utf8mb3;
alter table trainings drop column time_zone;

create table if not exists training_definitions (
    id int unsigned auto_increment  primary key,
    name varchar(255)               not null,
    description text                not null,
    season_id int unsigned          null,
    team_id int                     null,
    weekday int                     not null,
    start_time time                 not null,
    end_time time                   not null,
    time_zone varchar(255)          not null,
    active tinyint(1)               not null default 1,
    location varchar(255)           null,
    remark text                     null,
    user_id int unsigned            not null,
    created_at timestamp            not null default current_timestamp,
    updated_at timestamp            null
) charset = utf8mb3;
alter table training_definitions drop column time_zone;

create table if not exists training_contents (
    training_id int unsigned        not null,
    locale varchar(255)             not null,
    format varchar(255)             not null,
    title varchar(255)              not null,
    content text                    null,
    summary text                    not null,
    user_id int unsigned            not null,
    created_at timestamp            not null default current_timestamp,
    updated_at timestamp            null,
    primary key (training_id, locale)
) charset = utf8mb3;

create table if not exists teams (
    id int unsigned auto_increment      primary key,
    name varchar(255)                   null,
    season_id int unsigned              null,
    team_category_id int unsigned       null,
    active tinyint(1)                   not null default 1,
    remark text                         null,
    created_at timestamp                not null default current_timestamp,
    updated_at timestamp                null
) charset = utf8mb3;

create table if not exists training_teams (
    training_id                         int unsigned NOT NULL,
    team_id                             int unsigned NOT NULL,
    created_at timestamp                not null default current_timestamp,
    updated_at timestamp                null,
    primary key(training_id, team_id)
) charset = utf8mb3;

create table if not exists team_categories (
    id int unsigned auto_increment      primary key,
    name varchar(255)                   not null,
    start_age int                       null,
    end_age int                         null,
    competition tinyint(1)              not null default 0,
    gender tinyint(1)                   not null default 0,
    active tinyint(1)                   not null default 1,
    remark text                         null,
    created_at timestamp                not null default current_timestamp,
    updated_at timestamp                null
) charset = utf8mb3;

create table if not exists coaches (
    id int unsigned auto_increment      primary key,
    member_id int unsigned              not null,
    description text                    null,
    diploma varchar(255)                null,
    active tinyint(1)                   not null default 1,
    remark text                         null,
    user_id int unsigned                null,
    created_at timestamp                not null default current_timestamp,
    updated_at timestamp                null
) charset = utf8mb3;
alter table coaches rename column member_id to person_id;

create table if not exists training_coaches (
    training_id int unsigned            not null,
    coach_id int unsigned               not null,
    coach_type tinyint(1)               not null default 0,
    present tinyint(1)                  not null default 0,
    payed tinyint(1)                    not null default 0,
    remark text                         null,
    user_id int unsigned                not null,
    created_at timestamp                not null default current_timestamp,
    updated_at timestamp                null,
    primary key(training_id, coach_id)
) charset = utf8mb3;

create table if not exists training_presences
(
    training_id int unsigned                        not null,
    member_id   int unsigned                        not null,
    remark      text                                null,
    user_id     int unsigned                        not null,
    created_at  timestamp default CURRENT_TIMESTAMP not null,
    updated_at  timestamp                           null,
    primary key (training_id, member_id)
)
charset = utf8mb3;


create table if not exists persons(
    id int unsigned auto_increment        primary key,
    lastname varchar(255)                 not null,
    firstname varchar(255)                not null,
    gender int(11)                        not null,
    active tinyint(1)                     not null default 1,
    birthdate date                        not null,
    remark text                           null,
    user_id int unsigned                  null,
    contact_id int unsigned               null,
    code varchar(255)                     null,
    nationality_id int unsigned           not null,
    created_at timestamp                  not null default current_timestamp,
    updated_at timestamp                  null
) charset = utf8mb3;

create table if not exists contacts (
    id int unsigned auto_increment        primary key,
    email varchar(255)                    not null,
    tel varchar(255)                      not null,
    mobile varchar(255)                   not null,
    address varchar(255)                  not null,
    postal_code varchar(255)              not null,
    city varchar(255)                     not null,
    county varchar(255)                   null,
    country_id int unsigned               not null,
    remark text                           null,
    created_at timestamp                  not null default current_timestamp,
    updated_at timestamp                  null
) charset = utf8mb3;

create table if not exists sport_judo_members (
    id int unsigned auto_increment        primary key,
    license varchar(255)                  not null,
    license_end_date date                 not null,
    person_id int unsigned                not null,
    remark text                           null,
    competition tinyint(1)                not null default 0,
    created_at timestamp                  not null default current_timestamp,
    updated_at timestamp                  null,
    import_id int unsigned                null,
    active tinyint(1)                     not null default 1
) charset = utf8mb3;

create table judo_members like sport_judo_members;
insert into judo_members select * from sport_judo_members;
drop table sport_judo_members;

create table if not exists member_imports
(
    id         int unsigned auto_increment primary key,
    filename   text                                null,
    remark     text                                null,
    user_id    int unsigned                        not null,
    created_at timestamp default CURRENT_TIMESTAMP not null,
    updated_at timestamp                           null
)
charset = utf8mb3;

create table if not exists seasons (
    id int unsigned auto_increment        primary key,
    name varchar(255)                     not null,
    start_date date                       not null,
    end_date date                         not null,
    remark text                           null,
    created_at timestamp                  not null default current_timestamp,
    updated_at timestamp                  null
) charset = utf8mb3;

create table if not exists countries (
    id int unsigned auto_increment        primary key,
    iso_2 varchar(2)                      not null,
    iso_3 varchar(3)                      not null,
    name varchar(255)                     not null,
    created_at timestamp                  not null default current_timestamp,
    updated_at timestamp                  null
) charset = utf8mb3;
-- Delete duplicate iso_2 countries
delete c1 from countries c1
inner  join countries c2
where c1.id > c2.id and c1.iso_2 = c2.iso_2
;

alter table countries add constraint uq_iso_3 unique(iso_3);

create table if not exists team_members(
    team_id int(11) not null,
    member_id int(11) not null,
    active tinyint(1) not null default 1,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp null default null,
    primary key (team_id, member_id)
) charset = utf8mb3;
alter table team_members rename column member_id to person_id;

create table if not exists pages(
    id             int unsigned auto_increment primary key,
    enabled        tinyint(1) not null default 0,
    remark         text default null,
    application_id int unsigned not null,
    priority       int not null,
    created_at     timestamp not null default current_timestamp,
    updated_at     timestamp null default null
) charset=utf8mb3;

create table if not exists page_contents_2(
  page_id               int unsigned                         not null,
  locale                varchar(255)                         not null,
  format                varchar(255)                         not null,
  title                 varchar(255)                         not null,
  content               text,
  summary               text                                 not null,
  user_id               int                                  not null,
  created_at            datetime default CURRENT_TIMESTAMP   not null,
  updated_at            datetime                             null,
  primary key (page_id, locale)
) charset = utf8mb3;

-- Move page_contents_2 back to page_contents
drop table if exists page_contents;
CREATE TABLE page_contents LIKE page_contents_2;
INSERT INTO page_contents SELECT * FROM page_contents_2;
drop table if exists page_contents_2;

-- Remove unused tables
drop table if exists abilities;
drop table if exists ability_rules;
drop table if exists children;
drop table if exists club_members;
drop table if exists clubs;
drop table if exists abilities;
drop table if exists contents;
drop table if exists events;
drop table if exists event_contents;
drop table if exists mail_recipients;
drop table if exists mails;
drop table if exists events;
drop table if exists events;
drop table if exists oauth_access_token_scopes;
drop table if exists oauth_auth_code_scopes;
drop table if exists oauth_auth_codes;
drop table if exists oauth_client_grants;
drop table if exists oauth_client_scopes;
drop table if exists oauth_clients;
drop table if exists oauth_grants;
drop table if exists oauth_scopes;
drop table if exists oauth_user_grants;
drop table if exists oauth_user_scopes;
drop table if exists phinxlog;
drop table if exists rule_actions;
drop table if exists rule_subjects;
drop table if exists rules;
drop table if exists sport_judo_grades;
drop table if exists sport_judo_member_grades;
drop table if exists user_abilities;
drop table if exists user_logs;
-- migrate:down
