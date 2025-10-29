-- Salas mas reservadas
SELECT 
    s.nombre_sala,
    s.edificio,
    COUNT(*) AS cantidad_reservas
FROM 
    sala s
JOIN 
    reserva r 
    ON s.nombre_sala = r.nombre_sala 
    AND s.edificio = r.edificio
GROUP BY 
    s.nombre_sala, s.edificio
ORDER BY 
    cantidad_reservas DESC;

-- Turnos mas demandados
SELECT
    t.hora_inicio,
    t.hora_fin,
    COUNT(r.id_reserva) AS cantidad_reservas
FROM
    turno t
JOIN 
    reserva r ON t.id_turno = r.id_turno
GROUP BY
    t.hora_inicio,
    t.hora_fin
ORDER BY
    cantidad_reservas DESC;

-- Promedio de participantes por sala
SELECT 
    reservas.nombre_sala,
    reservas.edificio,
    AVG(reservas.num_participantes) AS promedio_participantes
FROM (
	-- Cuenta cuántos participantes tuvo cada reserva.
    SELECT 
        id_reserva,
        nombre_sala,
        edificio,
        COUNT(ci_participante) AS num_participantes
    FROM 
        reserva r
    JOIN 
        reserva_participante rp ON r.id_reserva = rp.id_reserva
    GROUP BY 
        id_reserva, nombre_sala, edificio
) AS reservas
GROUP BY 
    nombre_sala, edificio
ORDER BY 
    promedio_participantes DESC;