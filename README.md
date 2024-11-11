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

### Django Admin

Instead of building out a whole management frontend we're going to grant folks access to the django admin to manage
the data they need (teams, games, etc).

Django supports basic permissioning (and groups for reusable sets of permissions) but we can always add in our own
permissions if need be. See https://docs.djangoproject.com/en/5.1/topics/auth/default/#permissions-and-authorization

### API

We have setup read only endpoints so the frontend can display data. The API follows normal REST conventions
and can be found at `/api`.

#### Endpoints

You can run `$ make manage C="show_urls" | grep api` to see what endpoints are available.

Access the endpoints in your browser for some basic api docs, you'll be able to see what the query params are, if the
endpoint supports search, what fields you can filter and order by.

If anything is unclear you can always checkout the relevant `*ViewSet` and `*FilterSet` (if applicable) classes for more
info as to what fields are used in search, etc.

#### Pagination

See https://www.django-rest-framework.org/api-guide/pagination/#pagenumberpagination for more info.

We can easily create our own pagination response format if we'd like (i.e. to include the total number of pages) however
for starters the out of the box pagination seemed fine.

#### Ordering

See https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter for more info.

#### Searching

See https://www.django-rest-framework.org/api-guide/filtering/#searchfilter for more info.

#### Filtering

See https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend for more info.

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
