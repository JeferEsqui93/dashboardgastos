-- database/schema.sql

-- 1. Activa el soporte para llaves foraneas (crucial para tus tablas relacionadas)
PRAGMA foreign_keys = ON;

-- Establece la codificacion a UTF-8 para evitar problemas con tildes en categorias
PRAGMA encoding = "UTF-8";

-- 2. LIMPIEZA (Opcional, util para desarrollo)
-- Estas lineas borran las tablas si ya existen para que el script siempre sea exitoso

DROP TABLE IF EXISTS Rol_Permisos;
DROP TABLE IF EXISTS Usuario_Rol;
DROP TABLE IF EXISTS Permisos;
DROP TABLE IF EXISTS Gasto;
DROP TABLE IF EXISTS Categoria;
DROP TABLE IF EXISTS Rol;
DROP TABLE IF EXISTS Usuario;

-- CREAR TABLAS

CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres_usuario VARCHAR(100),
    apellidos_usuario VARCHAR(100),
    documento VARCHAR(20) UNIQUE NOT NULL,
    celular VARCHAR(20),
    correo_usuario VARCHAR(150) UNIQUE NOT NULL,
    fecha_nacimiento DATE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Rol (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_rol VARCHAR(50) NOT NULL,
    descripcion_rol VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS Categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_categoria VARCHAR(100) NOT NULL,
    descripcion_categoria TEXT
);

CREATE TABLE IF NOT EXISTS Gasto (
    id_gasto INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    descripcion_gasto TEXT,
    fecha DATE NOT NULL,
    costo INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Permisos (
    id_permiso INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_permiso VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Usuario_Rol (
    id_usuario INTEGER NOT NULL,
    id_rol INTEGER NOT NULL,
    descripcion_usuario_rol TEXT,
    PRIMARY KEY (id_usuario, id_rol),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Rol_Permisos (
    id_rol INTEGER NOT NULL,
    id_permiso INTEGER NOT NULL,
    descripcion_rol_permisos TEXT,
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol) ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES Permisos(id_permiso) ON DELETE CASCADE
);

-- INSERTAR DATOS

-- 1. Insertar Roles
INSERT INTO Rol (nombre_rol, descripcion_rol) VALUES 
('Administrador', 'Acceso total'),
('Usuario_generico', 'Gestión de gastos personales');

-- 2. Insertar Permisos
INSERT INTO Permisos (nombre_permiso, slug) VALUES 
('Ver Gastos', 'gastos-ver'),
('Crear Gastos', 'gastos-crear'),
('Editar Gastos', 'gastos-editar'),
('Eliminar Gastos', 'gastos-eliminar'),
('Ver Dashboard', 'dashboard-ver'),
('Ver Usuarios', 'usuario-ver'),
('Editar Usuarios', 'usuario-editar'),
('Eliminar Usuarios', 'usuario-eliminar');

-- 3. Relacionar Rol_Permisos (Admin=1, Genérico=2)
-- Para Usuario_generico (ID 2)
INSERT INTO Rol_Permisos (id_rol, id_permiso) VALUES 
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5);

-- Para Administrador (ID 1) - Todos los permisos
INSERT INTO Rol_Permisos (id_rol, id_permiso) VALUES 
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8);

-- 4. Insertar Categorías
INSERT INTO Categoria (nombre_categoria, descripcion_categoria) VALUES 
('Arrendamiento', 'Pagos de alquiler o cuotas de vivienda.'),
('Servicios Públicos', 'Pagos de luz, agua, gas, internet y telefonía.'),
('Transporte', 'Gastos de combustible, transporte público, plataformas o mantenimiento de vehículo.'),
('Educación', 'Pensiones, cursos, libros y materiales académicos.'),
('Entretenimiento', 'Suscripciones (Netflix, Spotify), cine y eventos culturales.'),
('Deudas', 'Pago de tarjetas de crédito, préstamos bancarios o compromisos financieros.'),
('Alimentación', 'Mercado mensual y compras de víveres esenciales.'),
('Ocio y Diversión', 'Salidas a comer, viajes, hobbies y gastos no esenciales.');