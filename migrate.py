#!/usr/bin/env python3

import yoyo

from configs import configs

# Load the configuration
config = configs.parseConfig()

# Load the migration files
migrations = yoyo.read_migrations(config['migrationsDir'])

print('Found a total of %d migrations' % len(migrations))

# Connect to the database.  This takes a connection string so we have to build it ourselves from
# the psycopg2 aruguments
dbc = config['database']
connString = 'postgres://%s:%s@%s:%s/%s' % (dbc['user'], dbc['password'], dbc['host'], dbc['port'], dbc['dbname'])
backend = yoyo.get_backend(connString)
with backend.lock():

    # Compute which migrations need applying
    toApply = backend.to_apply(migrations)

    # Log them
    print('Applying the following migrations: %s' % ([m.id for m in toApply]))

    # Apply them
    backend.apply_migrations(toApply)

print('Finished running migrations')
