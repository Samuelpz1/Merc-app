USE MERCAPP;

Create TABLE canasta_basica(
prod_id INT AUTO_INCREMENT PRIMARY KEY,
prod_category VARCHAR(20)
);

CREATE TABLE resultados(
resultado_id INT AUTO_INCREMENT PRIMARY KEY,
nom_product VARCHAR(150) NOT NULL,
precio FLOAT NOT NULL,
tienda VARCHAR(15) NOT NULL,
prod_category_id INT NOT NULL,
fecha date NOT NULL
);

ALTER TABLE resultados
ADD CONSTRAINT fk_prod_category_id
FOREIGN KEY (prod_category_id) REFERENCES canasta_basica(prod_id);

INSERT INTO canasta_basica (prod_category) VALUES
('Leche'),
('Huevos'),
('Salchichas'),
('Arroz'),
('Banano'),
('Tomate'),
('Zanahoria'),
('Limon'),
('Cebolla'),
('Café'),
('Aceite'),
('Mantequilla');


SELECT * FROM canasta_basica;


show tables;
