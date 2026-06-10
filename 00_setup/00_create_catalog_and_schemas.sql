CREATE CATALOG IF NOT EXISTS banklens;

CREATE SCHEMA IF NOT EXISTS banklens.bronze;

CREATE SCHEMA IF NOT EXISTS banklens.silver;

CREATE SCHEMA IF NOT EXISTS banklens.gold;

CREATE SCHEMA IF NOT EXISTS banklens.data_quality;

CREATE VOLUME IF NOT EXISTS banklens.bronze.raw_files;