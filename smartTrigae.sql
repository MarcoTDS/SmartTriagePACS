-- Active: 1768952423418@@127.0.0.1@5432@smarttriage
#TODAS AS COLUNAS DESTA TABELA ARMAZENAM INFORMAÇÕES SOBRE OS ESTUDOS REALIZADOS PELOS PACIENTES, PATIENT_ID TAMBÉM É UM DADO DICOM
CREATE TABLE IF NOT EXIST studies(
    id_study SERIAL,
    patient_id VARCHAR(100),
    patient_name VARCHAR(255),
    patient_sex CHAR(1),
    patient_birth_date DATE,
    body_part VARCHAR(255),
    modality VARCHAR(50),
    accession_number VARCHAR(100),
    study_instance_uid VARCHAR(100) UNIQUE,
    study_date TIMESTAMP NOT NULL,
    study_description TEXT,
    study_last_import TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    study_status VARCHAR(50) DEFAULT 'ANALISE PENDENTE',
    study_priority INTEGER DEFAULT 0,
    file_path VARCHAR(512),
    PRIMARY KEY (id_study)
);

CREATE TABLE IF NOT EXISTS userTypes(
    id_user_type SERIAL,
    user_type_name VARCHAR(100),
    PRIMARY KEY (id_user_type)
);

CREATE TABLE IF NOT EXISTS users(
    id_user SERIAL,
    user_email VARCHAR(255) UNIQUE,
    user_password VARCHAR(255),
    user_name VARCHAR(255),
    id_user_type INTEGER,
    crm VARCHAR(10),
    crm_uf CHARACTER(2),
    PRIMARY KEY (id_user),
    FOREIGN KEY (id_user_type) REFERENCES userTypes(id_user_type)
);

CREATE TABLE IF NOT EXISTS institutions(
    id_institution SERIAL,
    institution_name VARCHAR(255) UNIQUE,
    institution_guardin VARCHAR(255),
    CNPJ VARCHAR(20),
    PRIMARY KEY (id_institution)
);

CREATE TABLE IF NOT EXISTS userInstitutions(
    id_user_institution SERIAL,
    id_user INTEGER,
    id_institution INTEGER,
    PRIMARY KEY (id_user_institution),
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_institution) REFERENCES institutions(id_institution)
);

CREATE TABLE IF NOT EXISTS specialties(
    id_specialty SERIAL,
    specialty_name VARCHAR(100),
    specialty_code VARCHAR(10),
    PRIMARY KEY (id_specialty)
);

CREATE TABLE IF NOT EXISTS userSpecialties(
    id_user_specialty SERIAL,
    id_user INTEGER,
    id_specialty INTEGER,
    PRIMARY KEY (id_user_specialty),
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_specialty) REFERENCES specialties(id_specialty)
);
CREATE TABLE IF NOT EXISTS priorityRules(
    id_priority_rule SERIAL,
    priority_name VARCHAR(50),
    trigger_keyword VARCHAR(100),
    target_field VARCHAR(50),
    score INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_priority_rule)
);

CREATE TABLE IF NOT EXISTS routingRules(
    id_routing_rule SERIAL,
    id_specialty INTEGER,
    routing_name VARCHAR(100),
    condition_modality VARCHAR(50),
    condition_body_part VARCHAR(255),
    PRIMARY KEY (id_routing_rule),
    FOREIGN KEY (id_specialty) REFERENCES specialties(id_specialty)
);


    