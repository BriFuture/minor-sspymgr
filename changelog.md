# Change Log


## v0.0.14

1. plugin system finished
2. command line argument support

## v0.0.13

1. UI optimization
2. product system finished 

## v0.0.12

1. Flow Usage now could be viewed by User
2. order and email history now displayed in page, more detailed routes applied in frontend
3. announcement feature added
4. shadowsocks client can use qrcode to configure ss.

## v0.0.11

1. Vue Frontend Home is finished now. And Old UI is replaced by Vue
2. signup and singin page visible bug in mobile (Form is too large to view)
3. now admin can comment user
4. update and simplified routes of user and admin
5. email database and admin can view them

## v0.0.10

1. frontend is handled by Vue now, backend now provides api for display or operation
2. sidebar now can collapse/expand on mobile 
3. beautify UI
4. when ss account is timeout, notify the user with an email
5. signup checkcode send inform, after signup, inform user that he has an account 

## v0.0.08

1. add account chart display
2. optimize project structure
3. add email notifying feature when user account will be expired soon.

## v0.0.07

1. product page improvement: add new product 
2. improve url root
3. fix bug when communicating with shadowsock server, modify adapter buffer size
4. admin: account flow, expire update
5. user: take order have time limit now, order page optimized.


## v0.0.06

1. shadowsocks part, shadowsocks integrated into this application, but old application's reloader feature is not useable any more
2. utilize the blueprint feature to seperate module
3. admin: optimized account detail page, account password now can be either updated or randomized
4. home: signup password visible
5. user can reset password now( although it is need to be beautified)


## v0.0.05

1. admin product page: disable or enable a product (JSON and backend response)
2. user order modal ui
3. admin account view and new account ui
4. user account page: account infomation corresponding with shadowsocks
5. tests with shadowsocks


## v0.0.04

1. Manager can see webgui setting, products and orders page.
2. Image file upload completed
3. **qrcode stored in database** and display on admin page
4. use ssl method to send email, and email can be sent by smtp server now
5. signup maxmimum count limit
6. admin setting page, value display(according to type), default number can be changed

## v0.0.03

1. shadowsocks service interface completed, pyshadowsocks api can be called
2. user home page, admin home page
3. product and order subsystem 

## v0.0.02

1. send email and signup verification, signup ui
2. basic unit tests
3. login and ui, session stored in database
4. optimize code structure, update shadowsocks controller

## v0.0.01

1. Use flask as Web App Framework
2. Finish some web interfaces
3. Create Database Manager Models
