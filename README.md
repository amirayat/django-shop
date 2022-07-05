<a href="#">
  <div align="center">
    <img src="https://i.morioh.com/2022/03/16/b8a72106.webp" width='154'/>
  </div>
</a>

<h1 align="center">Django shop</h1>
<h3 align="center"> The ultimate restfull api django shop for: <i>Businesses, Sales & Marketing People</i></h3>
<hr>

## Features 🚀

### 1) Authentication and Authorization
- User Registration with activation
- Login/Logout  
- Retrieve/Update the Django User model
- Password change
- Password reset via e-mail
- Social Media authentication

### 2) Supported use cases of coupons
This application supports different kind of coupons in the way how they can be redeemed.
The difference is defined by the number of possible redeems and if they are bound to a specific user (may even be a list of users) or not.
- single time (default), coupon can be used one time without being bound to an user.
- user limited, coupon can be used one time but only by a specific user.
- users list, coupon can be used by a defined list of users, each once.
- unlimited, coupon can be used unlimited times, but only once by the same user.

### 3) user wallet
- coupon chrges wallet

### 4) Admin panel
- {base_url}/admin/  

### 5) Api documentaion(swagger-redoc)
- {base_url}/swagger/ 
- {base_url}/redoc/  

<hr>

## .env format
```
DJANGO_SECRET_KEY = ***
DJANGO_ALLOWED_HOST = ***
CSRFORIGIN = http://***:80

SUPERUSER = ***
PASSWORD = ***
EMAIL = ***
```

<hr>

## To Do
- Product application
- Cart application















