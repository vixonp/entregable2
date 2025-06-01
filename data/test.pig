-- test.pig
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

-- No filtrar con regex que elimine palabras
eventos_filtrados = FILTER eventos BY 
    tipo IS NOT NULL AND
    tipo != '';

agrupado = GROUP eventos_filtrados BY (tipo, calle);

conteo = FOREACH agrupado GENERATE 
    group.tipo AS tipo,
    group.calle AS calle,
    COUNT(eventos_filtrados) AS cantidad;

STORE conteo INTO '/data/output_tipo_calle.csv' USING PigStorage(',');
