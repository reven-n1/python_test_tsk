create database if not exists test_task;

use test_task;

create table if not exists statistics
(
    id     int auto_increment
        primary key,
    date   date                        not null comment 'event date',
    views  int            default 0    not null comment 'views num',
    clicks int            default 0    not null comment 'clicks num',
    cost   decimal(19, 2) default 0.00 not null comment 'click cost'
);
