-- migrate:up
create table if not exists imports
(
    id         int unsigned auto_increment primary key,
    uuid       varchar(255)                        not null,
    filename   varchar(512)                        not null,
    remark     text                                null,
    user_id    int                                 not null,
    created_at timestamp default CURRENT_TIMESTAMP not null,
    updated_at timestamp                           null
)
charset = utf8mb3;
alter table imports add constraint uq_uuid unique(uuid);

create table if not exists judo_member_imports (
    member_id int unsigned not null,
    import_id int unsigned not null,
    created_at  datetime default CURRENT_TIMESTAMP not null,
    primary key (import_id, member_id)
)
charset = utf8mb3;

alter table judo_members drop column import_id;
alter table judo_members add index judo_members_license_index(license);
alter table judo_members add column uuid varchar(255) not null;
update judo_members set uuid=uuid();
alter table judo_members add index judo_members_uuid_index(uuid);
alter table persons drop column active;
-- migrate:down
