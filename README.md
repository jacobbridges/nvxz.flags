<div align="center">
  <a href="https://github.com/jacobbridges/nvxz.flags">
    <img src="https://github.com/jacobbridges/nvxz.flags/blob/main/_docs/assets/logo.jpg?raw=true" alt="Repo Logo" height="150">
  </a>
</div>

<h3 align="center"><pre>nvxz.flags</pre></h3>

<div align="center"><i>Tiny feature flag server.</i></div>
&nbsp;

<div align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg?labelColor=003694&color=ffffff" alt="License">
  <img src="https://img.shields.io/github/contributors/jacobbridges/nvxz.flags?labelColor=003694&color=ffffff" alt="GitHub contributors" >
  <img src="https://img.shields.io/github/stars/jacobbridges/nvxz.flags.svg?labelColor=003694&color=ffffff" alt="Stars">
  <img src="https://img.shields.io/github/forks/jacobbridges/nvxz.flags.svg?labelColor=003694&color=ffffff" alt="Forks">
  <img src="https://img.shields.io/github/issues/jacobbridges/nvxz.flags.svg?labelColor=003694&color=ffffff" alt="Issues">
</div>

----

## Features

* **Fast:** Built with [FastAPI](https://github.com/fastapi/fastapi) and [SQLite](https://www.sqlite.org/).
* **Tiny:** Less than 1k lines of code.
* **No external dependencies:** Uses SQLite database
* **Easy deployment:** Deploy with [coolify](#) or grab the [docker image](#).

## Getting Started

I currently run nvxz.flags on [coolify](https://coolify.io/), but you can grab the [alpine image](#) and run it wherever you like.


## API Docs

More detailed API docs are available on swagger at `/docs/` after install.

#### 🔌 Register New User

<details>
 <summary><code>POST</code> <code><b>/users/</b></code></summary>

##### Example Body

```json
{
  "username": "john",
  "password": "jingleheimersmith"
}
```

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | username  |  required | string                  | Username on the platform |
> | password  |  required | string                  | Password for login |


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `201`         | `application/json`                | `<User object returned>`                                |
> | `400`         | `application/json`                | `{"detail": "Bad Request"}`                                         |
> | `409`         | `application/json`                | `{"detail": "Username is taken"}`                                   |

##### Example cURL

> ```shell
>  curl -X POST -H "Content-Type: application/json" --data @post.json http://localhost:8000/users/
> ```

</details>


#### 🔌 Login

_OAuth2 scheme._

<details>
 <summary><code>POST</code> <code><b>/auth/token/</b></code></summary>

##### Parameters

> | name       |  type     | data type               | description                                                           |
> |------------|-----------|-------------------------|-----------------------------------------------------------------------|
> | grant_type |  required | string                  | Part of OAuth2 scheme. Set to "password" |
> | username   |  required | string                  | Username on the platform |
> | password   |  required | string                  | Password for login |


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `<session token returned>`                                |
> | `400`         | `application/json`                | `{"detail": "Invalid username or password"}`                                         |

##### Example cURL

> ```shell
> curl -X 'POST' \
  'https://localhost:8000/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=test&password=test'
> ```

</details>


## Built With

[![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](#)
[![SQLite](https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](#)
[![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=Pydantic&logoColor=white)](#)