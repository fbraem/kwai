-- migrate:up

alter table training_definitions add column timezone varchar(255) default 'Europe/Brussels' not null;

-- migrate:down
