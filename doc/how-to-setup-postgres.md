# DB PostgreSQL

> psycopg is not supported by OpenBSD. 
> I've rolled back the code to 3cf3414ec74afdc8a5d0ae59e309c728e41ce243.
> Claude offer tips on how it may work : https://claude.ai/chat/6a315fd7-4b48-4f22-b161-7f11835be420.
> Put this on hold for now.

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
