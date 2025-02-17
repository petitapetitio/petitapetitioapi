# DB

Créer la db sur OpenBSD
```shell
# Se connecter avec l'utilisateur postgres (à la base postgres)
psql -U postgres 
```

```psql
-- Créer l'utilisateur
CREATE USER petitapetitio_backend WITH PASSWORD '********';

-- Créer la db
CREATE DATABASE petitapetitio;

-- Se connecter à la db
\c petitapetitio

-- Permettre à l'utilisateur de se connecter à la db
GRANT CONNECT ON DATABASE petitapetitio TO petitapetitio_backend;

-- Autoriser à créer des tables et utiliser le schema
GRANT USAGE, CREATE ON SCHEMA public TO petitapetitio_backend;

-- Définir les permissions par défaut sur les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO petitapetitio_backend;

-- Vérifier les permissions
\du petitapetitio_backend

-- Pour nettoyer si besoin :
-- REVOKE ALL ON SCHEMA public FROM petitapetitio_backend;
-- DROP USER petitapetitio_backend;
-- DROP DATABASE petitapetitio;
```

Créer un utilisateur pour les tests :
```
createuser petitapetitio_tests_user
```