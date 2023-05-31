-- Creación de la tabla "Imagen"
CREATE TABLE Imagen (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    archivo VARCHAR,
    CONSTRAINT archivo_unique UNIQUE (archivo)
);

-- Creación de la tabla "HistorialProcesamiento"
CREATE TABLE HistorialProcesamiento (
    id SERIAL PRIMARY KEY,
    imagen_id INTEGER REFERENCES Imagen(id) ON DELETE CASCADE,
    paso VARCHAR(100),
    estado VARCHAR(20),
    tiempo_inicio TIMESTAMP,
    tiempo_fin TIMESTAMP,
    duracion INTERVAL
);

-- Creación de la tabla "RegistroError"
CREATE TABLE RegistroError (
    id SERIAL PRIMARY KEY,
    imagen_id INTEGER REFERENCES Imagen(id) ON DELETE CASCADE,
    paso VARCHAR(100),
    descripcion TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);