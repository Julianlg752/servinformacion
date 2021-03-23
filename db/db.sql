create database servi_votacion;

use servi_votacion;

create table departamento(
	id int auto_increment,
	nombre varchar(100),
	primary key(id)
);

create table municipio (
	id int auto_increment,
	departament_id int,
	nombre varchar(255),
	primary key(id),
	foreign key(departament_id) references departamento(id)
);

create table privilegio (
	id int auto_increment,
	privilegio varchar(255),
	primary key(id)
);

create table ubicacion (
	id int auto_increment,
	direccion varchar(500),
	lat float,
	lon float,
	primary key(id)
);


create table mesa_votacion (
	id int auto_increment,
	ubicacion_id int,
	municipio_id int,
	nombre varchar(255),
	direccion varchar(255),
	primary key(id),
	foreign key(ubicacion_id) references ubicacion(id),
	foreign key(municipio_id) references municipio(id)
);

create table usuario (
	id int auto_increment,
	privilegio_id int,
	ubicacion_id int,
	nombre varchar(255),
	apellido varchar(255),
	direccion varchar(255),
	ciudad varchar(255),
	celular varchar(255),
	tipo_documento varchar(19),
	documento varchar(500) unique,
	foto varchar(255),
	contrasenia text,
	primary key(id),
	foreign key(privilegio_id) references privilegio(id),
	foreign key(ubicacion_id) references ubicacion(id)
);

create table votante (
	id int auto_increment,
	usuario_id int,
	mesa_votacion_id int,
	municipio_id int,
	nombre varchar(255),
	apellido varchar(255),
	ciudad varchar(255),
	direccion varchar(255),
	telefono varchar(255),
	tipo_documento varchar(19),
	documento varchar(500) unique,
	fecha_creacion date,
	primary key(id),
	foreign key(usuario_id) references usuario(id),
	foreign key(mesa_votacion_id) references mesa_votacion(id),
	foreign key(municipio_id) references municipio(id)
);

insert into privilegio(privilegio) values('ADMIN'),('LEADER');
insert into usuario(privilegio_id, nombre, documento, contrasenia) values(1, 'admin', '90210', 'sha256$ol3QW3bI$5e58afa3d0850bdfd95f667b18af8be32098dcf17561fde73b170b8deb59fe4f')
