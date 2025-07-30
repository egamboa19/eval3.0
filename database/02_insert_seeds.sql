-- ===================================================
-- DATOS INICIALES DEL SISTEMA
-- ===================================================

-- Insertar roles
INSERT INTO roles (name, description) VALUES 
('admin', 'Administrador del sistema con acceso completo'),
('coordinador', 'Coordinador de area que evalua maestros'),
('maestro', 'Maestro que realiza autoevaluaciones');

-- Insertar departamentos
INSERT INTO departments (name, description) VALUES 
('Matematicas', 'Departamento de Ciencias Matematicas'),
('Ciencias', 'Departamento de Ciencias Naturales'),
('Humanidades', 'Departamento de Humanidades y Letras'),
('Ingles', 'Departamento de Idioma Ingles'),
('Educacion Fisica', 'Departamento de Educacion Fisica y Deportes'),
('Artes', 'Departamento de Artes y Cultura'),
('Tecnologia', 'Departamento de Tecnologia e Informatica'),
('Administracion', 'Departamento Administrativo');

-- Configuración del sistema
INSERT INTO system_config (key, value, description) VALUES 
('institution_name', 'prepa 25', 'Nombre de la institucion'),
('institution_short', 'eduardoaguirrepequeno', 'Nombre corto de la institucion'),
('network_mode', 'hybrid', 'Modo de red: local, hybrid, web'),
('default_evaluation_duration', '7', 'Duracion por defecto de evaluaciones en dias'),
('session_timeout', '480', 'Timeout de sesion en minutos');

-- Encuesta ejemplo
DO $$
DECLARE
    survey_uuid UUID;
BEGIN
    INSERT INTO surveys (title, description, instructions) 
    VALUES (
        'Evaluacion Docente Estandar',
        'Evaluacion integral del desempeno docente',
        'Califique cada aspecto del 1 al 10, donde 1 es deficiente y 10 es excelente'
    ) RETURNING id INTO survey_uuid;
    
    INSERT INTO questions (survey_id, question_text, order_number) VALUES 
    (survey_uuid, 'Dominio del contenido de la materia', 1),
    (survey_uuid, 'Claridad en la explicacion de conceptos', 2),
    (survey_uuid, 'Puntualidad y asistencia', 3),
    (survey_uuid, 'Preparacion de clases', 4),
    (survey_uuid, 'Uso de recursos didacticos', 5),
    (survey_uuid, 'Atencion a estudiantes', 6),
    (survey_uuid, 'Evaluacion justa y objetiva', 7),
    (survey_uuid, 'Fomento de la participacion estudiantil', 8),
    (survey_uuid, 'Actualizacion profesional', 9),
    (survey_uuid, 'Trabajo en equipo con colegas', 10);
END $$;
