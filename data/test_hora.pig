-- test_hora.pig

-- Cargar CSV completo
eventos = LOAD '/data/eventos.csv' USING PigStorage(',') AS (
    id:int,
    tipo:chararray,
    descripcion:chararray,
    lat:float,
    lon:float,
    fecha_extraccion:chararray,
    cuadrante:int,
    calle:chararray
);

-- Filtrar eventos válidos (puedes ajustar según necesites)
eventos_filtrados = FILTER eventos BY fecha_extraccion IS NOT NULL AND fecha_extraccion != '';

-- Extraer la hora (asumiendo formato "YYYY-MM-DD HH:MM:SS")
eventos_hora = FOREACH eventos_filtrados GENERATE 
    FLATTEN(STRSPLIT(fecha_extraccion, ' ')) AS (fecha_str:chararray, hora_str:chararray);

-- Cortar la hora completa "HH:MM:SS" para extraer solo "HH"
horas = FOREACH eventos_hora GENERATE SUBSTRING(hora_str, 0, 2) AS hora;

-- Agrupar por hora
agrupado = GROUP horas BY hora;

-- Contar cuántos eventos por hora
conteo = FOREACH agrupado GENERATE 
    group AS hora,
    COUNT(horas) AS cantidad;

-- Guardar salida
STORE conteo INTO '/data/output_por_hora.csv' USING PigStorage(',');
