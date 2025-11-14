DROP DATABASE IF EXISTS obligatorio;
CREATE DATABASE `obligatorio`
    DEFAULT CHARACTER SET utf8
    COLLATE utf8_spanish_ci;
USE obligatorio;

CREATE TABLE Login
(
    correo       VARCHAR(50) UNIQUE,
    password     VARCHAR(50) NOT NULL,
    tipo_usuario ENUM ('usuario', 'admin') DEFAULT 'usuario',
    PRIMARY KEY (correo)
);

CREATE TABLE Participante
(
    ci       CHAR(8)     NOT NULL,
    nombre   VARCHAR(30) NOT NULL,
    apellido VARCHAR(30) NOT NULL,
    email    VARCHAR(50) UNIQUE,
    PRIMARY KEY (ci)
);

CREATE TABLE Facultad
(
    id_facultad INT AUTO_INCREMENT,
    nombre      VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_facultad)
);

CREATE TABLE Edificio
(
    nombre_edificio VARCHAR(50)  NOT NULL,
    direccion       VARCHAR(100) NOT NULL,
    departamento    VARCHAR(50)  NOT NULL,
    PRIMARY KEY (nombre_edificio)
);

CREATE TABLE Turno
(
    id_turno    INT AUTO_INCREMENT,
    hora_inicio TIME NOT NULL,
    hora_fin    TIME NOT NULL,
    PRIMARY KEY (id_turno)
);

CREATE TABLE Programa_academico
(
    nombre_programa VARCHAR(100)               NOT NULL,
    id_facultad     INT,
    tipo            ENUM ('grado', 'posgrado') NOT NULL,
    PRIMARY KEY (nombre_programa),
    FOREIGN KEY (id_facultad) REFERENCES Facultad (id_facultad)
);

CREATE TABLE Participante_programa_academico
(
    id_alumno_programa INT AUTO_INCREMENT,
    ci_participante    CHAR(8)                    NOT NULL,
    nombre_programa    VARCHAR(100)               NOT NULL,
    rol                ENUM ('alumno', 'docente') NOT NULL,
    PRIMARY KEY (id_alumno_programa),
    FOREIGN KEY (ci_participante) REFERENCES Participante (ci),
    FOREIGN KEY (nombre_programa) REFERENCES Programa_academico (nombre_programa)
);

CREATE TABLE Sala
(
    nombre_sala VARCHAR(50) NOT NULL,
    edificio    VARCHAR(50) NOT NULL,
    capacidad   INT,
    tipo_sala   ENUM ('libre', 'posgrado', 'docente') DEFAULT 'libre',
    PRIMARY KEY (nombre_sala, edificio),
    FOREIGN KEY (edificio) REFERENCES Edificio (nombre_edificio)
);

CREATE TABLE Reserva
(
    id_reserva  INT AUTO_INCREMENT,
    nombre_sala VARCHAR(50) NOT NULL,
    edificio    VARCHAR(50) NOT NULL,
    fecha       DATE        NOT NULL,
    id_turno    INT         NOT NULL,
    estado      ENUM ('activa', 'cancelada', 'sin asistencia', 'finalizada') default 'activa',
    PRIMARY KEY (id_reserva),
    FOREIGN KEY (nombre_sala, edificio) REFERENCES Sala (nombre_sala, edificio),
    FOREIGN KEY (edificio) REFERENCES Edificio (nombre_edificio),
    FOREIGN KEY (id_turno) REFERENCES Turno (id_turno)
);

CREATE TABLE Reserva_participante
(
    ci_participante         CHAR(8),
    id_reserva              INT      NOT NULL,
    fecha_solicitud_reserva DATETIME NOT NULL,
    asistencia              BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (ci_participante, id_reserva),
    FOREIGN KEY (ci_participante) REFERENCES Participante (ci),
    FOREIGN KEY (id_reserva) REFERENCES Reserva (id_reserva)
);

CREATE TABLE Sancion_participante
(
    ci_participante CHAR(8) NOT NULL,
    fecha_inicio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin       DATE    NOT NULL,
    PRIMARY KEY (ci_participante, fecha_inicio, fecha_fin),
    FOREIGN KEY (ci_participante) REFERENCES Participante (ci)
);

CREATE USER 'obligatorio'@'%' IDENTIFIED BY 'obligatorio1234';
GRANT SELECT, INSERT, UPDATE, DELETE ON obligatorio.* TO 'obligatorio'@'%';
FLUSH PRIVILEGES;
