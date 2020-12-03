# Money Transfer (Python)

This is a basic Python HTTP server to track users and their balances.  Your interviewer will explain the question to you; this README just contains usage hints.

The main libraries used in this server are [Flask](https://flask.palletsprojects.com/en/1.1.x/), an HTTP web framework, and [psycopg2](https://www.psycopg.org/), a PostgreSQL client.

## Getting Started

To get started, start the database with:
```bash
$ bin/start_db.sh
```

Then, in a separate window, install dependencies, run migrations, and start the server:
```bash
# It's important to source this so that your interactive shell gets into the venv
$ source bin/install_deps.sh
$ ./migrate.py
$ ./app.py
```

The server starts by default on `localhost:8080`.

To test further changes, you'll probably just want one of the following:
```bash
# Run the server
$ ./app.py
# Run migrations
$ ./migrate.py
```

You can see a test account in a third window with:
```bash
$ curl localhost:8080/accounts/1
```

Finally, you can get a PostgreSQL shell with:
```bash
$ bin/attach_db.sh
```


## Migrations

Migrations are run via [yoyo](https://ollycope.com/software/yoyo/latest/) package.  You can add new migrations in the `migrations` directory with a `number.name.sql` filename, and you can run migrations with the `./migrate.py` command.


## Making Changes

Your interviewer will probably ask you to add a new endpoint.  You should start in `app.py`, but be aware that that file is purposely long and should probably be split up before you do much more in it.
