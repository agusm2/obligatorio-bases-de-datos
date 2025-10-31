USE obligatorio;

-- 1. Salas mas reservadas
SELECT s.nombre_sala,
       s.edificio,
       COUNT(*) AS cantidad_reservas
FROM Sala s
         JOIN
     reserva r
     ON s.nombre_sala = r.nombre_sala
         AND s.edificio = r.edificio
GROUP BY s.nombre_sala, s.edificio
ORDER BY cantidad_reservas DESC;

-- 2. Turnos mas demandados
SELECT t.hora_inicio,
       t.hora_fin,
       COUNT(r.id_reserva) AS cantidad_reservas
FROM turno t
         JOIN
     reserva r ON t.id_turno = r.id_turno
GROUP BY t.hora_inicio,
         t.hora_fin
ORDER BY cantidad_reservas DESC;

-- 3. Promedio de participantes por sala
SELECT reservas.nombre_sala,
       reservas.edificio,
       AVG(reservas.num_participantes) AS promedio_participantes
FROM (
         -- Cuenta cuántos participantes tuvo cada reserva.
         SELECT id_reserva,
                nombre_sala,
                edificio,
                COUNT(ci_participante) AS num_participantes
         FROM reserva r
                  JOIN
              reserva_participante rp ON r.id_reserva = rp.id_reserva
         GROUP BY id_reserva, nombre_sala, edificio) AS reservas
GROUP BY nombre_sala, edificio
ORDER BY promedio_participantes DESC;

-- 4. Cantidad de reservas por carrera y facultad
SELECT f.nombre                     AS facultad,
       ppa.nombre_programa          AS carrera,
       COUNT(DISTINCT r.id_reserva) AS cant_reservas
FROM reserva_participante rp
         JOIN reserva r
              ON r.id_reserva = rp.id_reserva
         JOIN participante_programa_academico ppa
              ON ppa.ci_participante = rp.ci_participante
         JOIN programa_academico pa
              ON pa.nombre_programa = ppa.nombre_programa
         JOIN facultad f
              ON f.id_facultad = pa.id_facultad
GROUP BY f.nombre, ppa.nombre_programa
ORDER BY f.nombre, cant_reservas DESC;

-- 5. Porcentaje de ocupación de salas por edificio
SELECT r.edificio                                  AS Edificio,
       SUM(r.estado = 'activa') * 100.0 / COUNT(*) AS Porcentaje
FROM reserva r
         JOIN edificio e
              ON e.nombre_edificio = r.edificio
GROUP BY Edificio;

-- 6. Cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado)
SELECT ppa.rol                             AS rol,
       pa.tipo                             AS tipo,
       COUNT(DISTINCT r.id_reserva)        AS cant_reservas,
       SUM(IF(rp.asistencia = TRUE, 1, 0)) AS asistencia
FROM reserva_participante rp
         JOIN reserva r
              ON r.id_reserva = rp.id_reserva
         JOIN participante_programa_academico ppa
              ON ppa.ci_participante = rp.ci_participante
         JOIN programa_academico pa
              ON pa.nombre_programa = ppa.nombre_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY pa.tipo, ppa.rol;

-- 7. Cantidad de sanciones para profesores y alumnos (grado y posgrado)
SELECT ppa.rol                             AS rol,
       pa.tipo                             AS tipo,
       COUNT(DISTINCT san.ci_participante) AS cant_sanciones
FROM sancion_participante san
         JOIN participante_programa_academico ppa
              ON ppa.ci_participante = san.ci_participante
         JOIN programa_academico pa
              ON pa.nombre_programa = ppa.nombre_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY pa.tipo, ppa.rol;

-- 8. Porcentaje de reservas efectivamente utilizadas vs. canceladas/no asistidas
SELECT IF(estado IN ('cancelada', 'sin asistencia'), 'Canceladas/ no asisitdas', 'Utilizadas') AS Categoria,
       COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reserva)                                       AS Porcentaje
FROM reserva
GROUP BY categoria;

-- Consultas sugeridas:
-- Permite identificar cuántos participantes fueron sancionados más de una vez
SELECT 
    ci_participante,
    COUNT(*) AS cantidad_sanciones
FROM sancion_participante
GROUP BY ci_participante
HAVING COUNT(*) > 1;

-- Detecta los usuarios que más cancelan o no asisten a sus reservas.
SELECT 
    rp.ci_participante,
    COUNT(*) AS reservas_no_utilizadas
FROM reserva_participante rp
JOIN reserva r ON rp.id_reserva = r.id_reserva
WHERE r.estado IN ('cancelada', 'sin asistencia')
GROUP BY rp.ci_participante
ORDER BY reservas_no_utilizadas DESC;

-- Permite identificar qué salas tienen menor uso
SELECT 
    s.nombre_sala,
    s.edificio,
    COUNT(r.id_reserva) AS cantidad_reservas
FROM sala s
LEFT JOIN reserva r 
    ON s.nombre_sala = r.nombre_sala AND s.edificio = r.edificio
GROUP BY s.nombre_sala, s.edificio
ORDER BY cantidad_reservas ASC;
