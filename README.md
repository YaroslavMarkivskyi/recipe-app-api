# Recipe App

The Recipe App is an API-based project that allows users to manage recipes, tags, and ingredients. It is built using Python and Django Rest Framework (DRF), containerized with Docker, and uses PostgreSQL as the database. The application is designed with scalability and flexibility in mind, integrating Nginx as a reverse proxy and GitHub Actions for CI/CD.

## 🚀 Features

- **User Authentication:** Secure user registration and token-based authentication.
- **Recipe management:** Create, update, delete and view recipes.
- **Ingredient and Tag Management:** Organize recipes by managing ingredients and tags.
- **API Documentation:** Interactive Swagger documentation for easy API navigation.

## 🛠️ Tech Stack

- **Backend:** Python, Django Rest Framework (DRF)
- **Database:** PostgreSQL
- **Containerization:** Docker
- **Web Server:** Nginx
- **CI/CD:** GitHub Actions

## 🌐 URL Endpoints
#### Authentication & User Management
- **User Registration:** `/api/user/create/`
- **User Login (Token Creation):** `/api/user/token/`
- **User Profile:** `/api/user/me/`
#### Recipes
- **List & Create Recipes:** `/api/recipe/recipes/`
- **Retrieve, Update & Delete Recipe:** `/api/recipe/recipes/<uuid:id>/`
- **Clap Article:** `/api/v1/articles/<uuid:article_id>/clap/`
#### Tags
- **List & Create Tags:** `/api/recipe/tags/`
- **Retrieve, Update & Delete Tag:** `/api/recipe/tags/<uuid:id>/`
#### Ingredients
- **List & Create Ingredients:** `/api/recipe/ingredients/`
- **Retrieve, Update & Delete Ingredient:** `/api/recipe/ingredients/<uuid:id>/`
#### API Documentation
- **Swagger Documentation:** `/api/docs/`
- **API Schema:** `/api/schema/`

## 📦 Installation 
Clone the repository:
```bash
git clone https://github.com/YaroslavMarkivskyi/recipe-app-api.git
```
Navigate to the project directory:
```bash
cd recipe-app-api
```
Set up and run the application using Docker Compose:
```bash
docker-compose up --build
```
Access the application at:
- API Documentation - [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- Admin Panel - [http://localhost:8000/admin/](http://localhost:8000/admin/)
##### To create a superuser after setting up the application with Docker, follow these steps:
Run the following command to enter the Docker container for your Django application:
```bash
docker-compose run --rm app sh
```
Inside the container, create a superuser using Django's createsuperuser command:
```bash
python manage.py createsuperuser
```
Follow the prompts to enter your desired superuser credentials (username, email, and password).

Once complete, exit the container by typing:
```bash
exit
```
