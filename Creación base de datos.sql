-- Crear base de datos
CREATE DATABASE PruebaLG;

-- Crear tabla para las ventas
-- (Tamaño de los campos de caracteres se decidió inspeccionando la longitud de 
-- la información registrada en dichas columnas en Python)
USE PruebaLG;
CREATE TABLE Ventas(
	VentasID INT IDENTITY(1,1) NOT NULL,
	Tipo VARCHAR(10),
	Tipo2 VARCHAR(2),
	Canal VARCHAR(10),
	Cadena VARCHAR(10),
	Subcadena VARCHAR(20),
	PuntoDeVenta VARCHAR(60),
	HomologaAlmacen VARCHAR(3),
	EAN VARCHAR(15),
	Modelo VARCHAR(100),
	ReferenciaHomologada VARCHAR(20),
	Categoria VARCHAR(3),
	Subcategoria VARCHAR(6),
	Linea VARCHAR(15),
	Sublinea VARCHAR(15),
	Unidades INT,
	ValorTotal DECIMAL(26, 15),
	Regional VARCHAR(20),
	Ciudad VARCHAR(20),
	NumeroSemana VARCHAR(3),
	Fecha DATE,
	Mes VARCHAR(10),
	CoreStore VARCHAR(3),
	Promoter VARCHAR(3),
	PRIMARY KEY (VentasID),
);
