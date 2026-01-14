-- 1. Creación de la base de datos
CREATE DATABASE cenit_salud_db;
USE cenit_salud_db;

-- 2. Tabla de Pacientes
CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(100)
);

-- 3. Tabla de Médicos (Especialistas)
CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    especialidad VARCHAR(50) NOT NULL,
    correo_interno VARCHAR(100)
);

-- 4. Tabla de Citas (Relaciona pacientes y médicos)
CREATE TABLE citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT,
    id_medico INT,
    fecha_cita DATETIME NOT NULL,
    motivo VARCHAR(255),
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);

-- -----------------------------------------------------
-- 5. Inserción de registros de prueba
-- -----------------------------------------------------

-- Insertar Médicos
-- -----------------------------------------------------
-- REGISTROS PARA LA TABLA: medicos (8 registros)
-- -----------------------------------------------------
INSERT INTO medicos (nombre, especialidad, correo_interno) VALUES 
('Dr. Julián Martínez', 'Medicina General', 'jmartinez@clinica.com'),
('Dra. Elena Soler', 'Pediatría', 'esoler@clinica.com'),
('Dr. Roberto Sanz', 'Cardiología', 'rsanz@clinica.com'),
('Dra. Ana Belén', 'Dermatología', 'abelen@clinica.com'),
('Dr. Miguel Ángel', 'Traumatología', 'mangel@clinica.com'),
('Dra. Sofía Rivas', 'Ginecología', 'srivas@clinica.com'),
('Dr. Francisco Lara', 'Odontología', 'flara@clinica.com'),
('Dra. Laura Méndez', 'Nutrición', 'lmendez@clinica.com');

-- -----------------------------------------------------
-- REGISTROS PARA LA TABLA: pacientes (8 registros)
-- -----------------------------------------------------
INSERT INTO pacientes (nombre, apellido, telefono, email) VALUES 
('Carlos', 'Gómez', '555-0101', 'carlos.g@email.com'),
('Lucía', 'Fernández', '555-0202', 'lucia.f@email.com'),
('Marcos', 'Ruiz', '555-0303', 'marcos.r@email.com'),
('Silvia', 'Pérez', '555-0404', 'silvia.p@email.com'),
('Andrés', 'Castro', '555-0505', 'a.castro@email.com'),
('Isabel', 'Vargas', '555-0606', 'isavargas@email.com'),
('Javier', 'Soto', '555-0707', 'jsoto@email.com'),
('Marta', 'Ortega', '555-0808', 'm.ortega@email.com');

-- -----------------------------------------------------
-- REGISTROS PARA LA TABLA: citas (8 registros)
-- -----------------------------------------------------
-- Nota: Se asume que los IDs autoincrementales empiezan en 1
INSERT INTO citas (id_paciente, id_medico, fecha_cita, motivo) VALUES 
(1, 1, '2024-06-01 09:00:00', 'Chequeo anual de rutina'),
(2, 2, '2024-06-01 10:30:00', 'Consulta por fiebre persistente'),
(3, 3, '2024-06-02 11:00:00', 'Seguimiento de tensión arterial'),
(4, 4, '2024-06-02 16:00:00', 'Revisión de manchas en la piel'),
(5, 5, '2024-06-03 08:30:00', 'Dolor intenso en rodilla derecha'),
(6, 6, '2024-06-04 12:00:00', 'Control prenatal'),
(7, 7, '2024-06-05 17:30:00', 'Limpieza dental profunda'),
(8, 8, '2024-06-06 09:45:00', 'Diseño de plan nutricional');

----------------------------------------------------------------
SELECT 
    citas.fecha_cita,  
    pacientes.nombre AS nombre_paciente, 
    medicos.nombre AS nombre_medico
FROM citas
JOIN pacientes ON citas.id_paciente = pacientes.id_paciente
JOIN medicos ON citas.id_medico = medicos.id_medico;