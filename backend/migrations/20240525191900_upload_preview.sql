-- migrate:up

alter table imports add column preview tinyint(1) default 0 not null;

-- migrate:down
