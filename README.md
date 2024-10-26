### BTSH

This is a website for Black Top Street Hockey League.

# Apps

## api

Built with: Django, Django REST Framework, Postgres.

### Getting Started

* Install docker
* `$ cp .env.example .env`
* Build the docker images
  * `$ make build`
* Apply django migrations
  * `$ make migrate`
* Create a superuser
  * `$ make manage C="createsuperuser"`
  * You can use this user to log into the django admin
* Start your local server
  * `$ make up`
* Go to your local admin http://localhost:8000/admin/
  * Under `Sites` change `Domain name` to `localhost:8000` and `Display name` to `BTSH`
  * Under `Users` find the superuser you created and set your first name and last name
* Seed some data
  * `$ make manage C="seed_data"`

### Development

* Use the makefile, it has a bunch of make targets for common development tasks
  * Run `$ make help` to view all commands
* Remember to run `$ make makemigrations` after making changes to models and commit the generated migration files
* Remember to update the relevant `*Admin` class if you modify the models

### TODO

* AWS Deployment
  * Migrations
  * Collectstatic
* Configure django-storages and django-import-export to store user uploaded files in s3
  * Until we have a deployment to AWS these are stored on the file system (works for local dev but won't work for a real deployment)

## mobile

## web

## Getting Started

1. Clone the repository
2. Run `npm install`
3. Run `npm run dev`

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Create a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
