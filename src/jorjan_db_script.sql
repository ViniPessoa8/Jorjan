create database Jorjan;
use Jorjan;

create table Usuario(
	id int not null auto_increment,
    nome varchar(60) not null,
    email varchar(255) not null,
    senha varchar(255) not null,
    primary key(id)
);

INSERT INTO Usuario(nome, email, senha)
VALUES ('Vinícius Cavalcante de Brito Pessoa', 'vini.pessoa7@gmail.com', SHA1('senha'));


SELECT * FROM Usuario WHERE senha=SHA1('senha');