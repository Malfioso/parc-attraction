DROP TABLE IF EXISTS attraction;

CREATE TABLE attraction (
    attraction_id int auto_increment,
    primary key(attraction_id),
    nom varchar(255) not null,
    description varchar(255) not null,
    difficulte int,
    visible bool default true
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    users_id int auto_increment,
    primary key(users_id),
    name varchar(255) not null,
    password varchar(255) not null
);

CREATE TABLE critiques (
    critique_id int auto_increment,
    primary key(critique_id),
    note int,
    commentaire varchar(255),
    attraction_id int,
    foreign key(attraction_id) references attraction(attraction_id),
    users_id int,
    foreign key(users_id) references users(users_id)
);