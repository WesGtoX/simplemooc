<h1 align="center">
  Simplemooc
  <br />
  <img alt="Simplemooc CI" src="https://github.com/WesGtoX/simplemooc/workflows/Simplemooc%20CI/badge.svg" />
</h1>

<p align="center">
  <a href="#about-the-project">About</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#technology">Technology</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#getting-started">Getting Started</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#usage">Usage</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#license">License</a>
</p>

<p align="center">
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/wesgtox/simplemooc?style=plastic" />
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/wesgtox/simplemooc?style=plastic" />
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/wesgtox/simplemooc?style=plastic" />
  <img alt="GitHub issues" src="https://img.shields.io/github/issues/wesgtox/simplemooc?style=plastic" />
  <img alt="License" src="https://img.shields.io/github/license/wesgtox/simplemooc?style=plastic" />
  <!-- Build Status --> <!-- <a href="https://app.netlify.com/sites/XXXXXXXXXX/deploys" alt="Netlify Status"><img src="https://api.netlify.com/api/v1/badges/XXXXX_ID_HASH_XXXXX/deploy-status" /></a> -->
</p>


# Simplemooc

Simple MOOC is a simple distance learning platform for MOOC (Massive Open Online Course) courses. 
The "Simple" is related to the simplicity and minimalistic of the design and the objectivity of its functionalities.

Made in the [Python 3 na Web com Django (Básico e Intermediário)](https://www.udemy.com/python-3-na-web-com-django-basico-intermediario/) course by [Gileno Filho](https://github.com/gileno)"

Author: [Wesley Mendes](https://github.com/WesGtoX)

## About the Project

### Simple MOOC Features ##

> - General:
>
>   - Home with ceatured courses;
>   - CRUD of courses and instructors;
>   - Student registration;
>   - Listing of available courses and a way for students to enroll.
>
> - Functionalities related to the Course:
>
>   - Ad System (bulletin board);
>   - Classroom System (Video classroom + any digital material such as slides, pdf's,...);
>   - Forums;
>   - Tracking of the contents accessed by the students (both for administrators to know what was access, and for students to know what will come from the course);
>   - System of exercises (exercises of submission and exercises online).


## Technology 

This project was developed with the following technologies:

- [Python 3.9.1](https://www.python.org/)
- [Django Framework 3.1.6](https://www.djangoproject.com/)
- [Heroku](https://www.heroku.com/)
- [AWS S3](https://aws.amazon.com/s3/)


## Getting Started

### Prerequisites

- [Python 3.9.1](https://www.python.org/downloads/)

- Create a virtualenv
```bash
python -m venv .venv
```

- Activate virtualenv
```bash
source .venv/bin/activate
```


### Install and Run

1. Clone the repository:
```bash
git clone https://github.com/WesGtoX/simplemooc.git
```
2. Install the dependencies:
```bash
pip install -R requirements-dev.txt
```
3. Do the migrations
```bash
python manage.py migrate
```
4. Run:
```bash
python manage.py runserver
```


## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

Made with ♥ by [Wesley Mendes](https://wesleymendes.com.br/) :wave:
