USE obligatorio;

INSERT INTO
    obligatorio.login (correo, password, tipo_usuario)
VALUES
    ('agusm123@correo.com', '12345', 'admin'),
    ('matedif123@correo.com', 'abcd', 'admin'),
    ('fabrir123@correo.com', 'qwerty', 'usuario');

INSERT INTO
    obligatorio.participante (ci, nombre, apellido, email)
VALUES
    (
        '12345678',
        'Matias',
        'Hernandez',
        'matiher123@correo.com'
    ),
    (
        '87654321',
        'Jerónimo',
        'González',
        'jerogon123@correo.com'
    ),
    (
        '02345678',
        'José',
        'Abadie',
        'joaba123@correo.com'
    );
    
INSERT INTO
    obligatorio.facultad (nombre)
VALUES
    ('Facultad de Ingeniería'),
    ('Facultad de Ciencias'),
    ('Facultad de Medicina');

INSERT INTO
    obligatorio.edificio (nombre_edificio, direccion, departamento)
VALUES
    ('Central', '8 de octubre', 'Montevideo'),
    ('Campo', 'Rural 123', 'Salto'),
    ('UTP', 'Gorlero 123', 'Rocha');

INSERT INTO
    obligatorio.turno (hora_inicio, hora_fin)
VALUES
    ('08:00', '09:00'),
    ('09:00', '10:00'),
    ('10:00', '11:00'),
    ('11:00', '12:00'),
    ('12:00', '13:00'),
    ('13:00', '14:00'),
    ('14:00', '15:00'),
    ('15:00', '16:00'),
    ('16:00', '17:00'),
    ('17:00', '18:00'),
    ('18:00', '19:00'),
    ('19:00', '20:00'),
    ('20:00', '21:00'),
    ('21:00', '22:00'),
    ('22:00', '23:00');

INSERT INTO
    obligatorio.programa_academico (nombre_programa, id_facultad, tipo)
VALUES
    ('Ingeniería informática', 1, 'grado'),
    ('Experto en ciberseguridad', 1, 'posgrado'),
    ('Científico', 2, 'grado');

INSERT INTO
    obligatorio.participante_programa_academico (ci_participante, nombre_programa, rol)
VALUES
    ('12345678', 'Experto en ciberseguridad', 'alumno'),
    ('87654321', 'Científico', 'alumno'),
    ('02345678', 'Ingeniería informática', 'docente');

INSERT INTO
    obligatorio.sala (nombre_sala, edificio, capacidad, tipo_sala)
VALUES
    ('Sala 1', 'Central', 10, 'libre'),
    ('Sala 2', 'Campo', 5, 'posgrado'),
    ('Sala 3', 'UTP', 3, 'docente');

INSERT INTO
    obligatorio.reserva (nombre_sala, edificio, fecha, id_turno, estado)
VALUES
    ('Sala 1', 'Central', '2025-11-10', 1, 'activa'),
    ('Sala 2', 'Campo', '2025-12-01', 2, 'cancelada'),
    (
        'Sala 3',
        'UTP',
        '2025-12-25',
        3,
        'sin asistencia'
    );

INSERT INTO
    obligatorio.reserva_participante (
        ci_participante,
        id_reserva,
        fecha_solicitud_reserva,
        asistencia
    )
VALUES
    ('12345678', 1, '2025-11-05 09:30:00', true),
    ('87654321', 2, '2025-12-10 14:00:00', false),
    ('02345678', 3, '2025-12-31 23:00:00', true);

INSERT INTO
    obligatorio.sancion_participante (ci_participante, fecha_inicio, fecha_fin)
VALUES
    ('12345678', '2025-10-30', '2025-11-05'),
    ('87654321', '2025-11-15', '2025-11-25'),
    ('02345678', '2025-12-10', '2025-12-20');