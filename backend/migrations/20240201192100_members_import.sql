-- migrate:up
rename table judo_member_imports to imports;

create table judo_member_imports (
    member_id int unsigned not null,
    import_id int unsigned not null,
    created_at  datetime default CURRENT_TIMESTAMP not null,
    primary key (import_id, member_id)
);

alter table judo_members drop column import_id;
alter table judo_members add index judo_members_license_index(license);
alter table judo_members add column uuid varchar(255) not null;
update judo_members set uuid=uuid();
alter table judo_members add index judo_members_uuid_index(uuid);
alter table persons drop column active;
-- migrate:down
