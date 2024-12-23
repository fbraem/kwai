-- migrate:up

alter table coaches rename column person_id to member_id;
alter table team_members rename column person_id to member_id;

-- migrate:down
