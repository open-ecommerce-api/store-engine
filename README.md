<div align="center">
    <img alt="open-ecommerce-icon" src="https://user-images.githubusercontent.com/95884253/230792706-7a04c550-7eeb-4524-8244-cede6394abbc.png">
</div>

<div align="center">
  <h1>Django Ecommerce API</h1>
</div>
<div align="center">
        <a href="#"><img alt="licence" src="https://img.shields.io/github/license/open-ecommerce-api/backend?style=plastic" ></a>
        <a href="#"><img alt="forks" src="https://img.shields.io/github/forks/open-ecommerce-api/backend?style=plastic&color=yellow" ></a>
        <a href="https://github.com/open-ecommerce-api/backend/issues">
            <img alt="open-issues" src="https://img.shields.io/github/issues/open-ecommerce-api/backend?style=plastic&color=blue" >
        </a>
        <a href="https://github.com/open-ecommerce-api/backend/pulls">
            <img alt="pull-requests" src="https://img.shields.io/github/issues-pr/open-ecommerce-api/backend?color=success&style=plastic" >
        </a>
        <a href="#"><img alt="stars" src="https://img.shields.io/github/stars/open-ecommerce-api/backend?style=social" ></a>
</div>

<div align="center">
    <h3>An ecommerce backend-API created using Django and DRF (Django Rest Framework). </h3>
    <hr>

</div>

## Table of Contents

- [Description](#description)
- [Technologies](#technologies)
- [Collaboration-guidelines](#contribution-guidelines)
- [Installation](#installation)
- [Authentication](#authentication)
- [License](#license)

## Description

## Technologies

- Python v3.11.2
- Django v4.2
- DRF v3.14 (Django Rest Framework)
- Postgres v15.2 (Database)
- Docker

## Contribution guidelines

- Fork this repository
- Clone your forked repository
- Add your changes
- Commit and push
- Create a pull request
- Wait for pull request to merge

## Installation


## Authentication
We use the Simple JWT library for token-based authentication.

Usage:

### Obtain Token

First step is to authenticate and obtain the token. The endpoint is /api/token/ and it only accepts POST requests.
    
  url:
           http://domin/api/token/

  body: 
          {
          "username": "foo", 
          "password":  "foo"
          }
          
  resopnse:
          {
              "access": "token",
              "refresh": "token"
          }
          
After that you are going to store both the access token and the refresh token on the client side, usually in the localStorage.

You can use this access token for the next five minutes.

After five min, the token will expire, and if you try to access the view again, you are going to get the following error:

"message": "Token is invalid or expired"
          
### Refresh Token

To get a new access token, you should use the refresh token endpoint /api/token/refresh/ posting the refresh token:

  url:
          http://domin/api/token/refresh/

  body: 
          {
          "refresh":"token"
          }
          
  resopnse:
          {
              "access": "new token",
          }
          
The return is a new access token that you should use in the subsequent requests.

The refresh token is valid for the next 24 hours. When it finally expires too, the user will need to perform a full authentication again using their username and password to get a new set of access token + refresh token.
          
### Protected Views
In order to access the protected views on the backend (i.e., the API endpoints that require authentication), you should include the access token in the header of all requests, like this:

url:
          http://domin/hello/

  body: 
          {
          "Authorization":"Bearer Token"
          }
          
  resopnse:
          {
              "message": "hello world",
          }


## License

We decide to use **GPL v3.0 License** (Genu General Public License).
<br>

#### Explanation

The GNU General Public License is a series of widely used free software licenses that guarantee end users the four freedoms to run, study, share, and modify the software.