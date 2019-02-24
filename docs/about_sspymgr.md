# MINOR-SSPY-MGR WebServer Part

Last update time: 2019.02.24

This web application made by [BriFuture](https://github.com/brifuture) is based on flask. It is a developing program which aims to share our vps resource as well as the billings with our friends who want to use service lick shadowsocks. If you want to deploy a business application which aims profit, you may have to think another application instead. 

So, the following subsystems are built in the prerequirements that the users are our acquaintance. We have plenty ways to communicate with them, and ease the billing burden of vps.

## UI

[Bootstrap v4](https://getbootstrap.com/) is ultilized to build web UI. I am not skilled in making the User Interface, there are a lot of HTML code copied from Bootstrap Example. I do think that's a fussy thing to build UI, but Bootstrap helped me a lot and save much time for me as I build this web application.

Free svg resources used in the application are downloaded from [Font Awesome](https://fontawesome.com).

Now The frontend project is developed with [Vue](http://vuejs.org) which is a powerful frondend framework to build website in my views. Thans it a lot, I can finish this website application so quickly.

## Session

Session is a way to identify the user. Session should be stored on Server end, if visitors browser supports cookie, then key features of this Websites can be accessed by them, otherwise the visitor will never signup as well as signin.

### Session implemetation

At this term, session is stored in SQLite database table which named sessions. It has three columns, `sid` for identical, `expired` for expired time, `session` stores concrete content. 

I did not know redis until I implemented session stored in database, So there is no redis integration. What's more, I want to build this application as quick as I can, and it seems not so necessary to launch a redis service if you run this application on a low memory machine. But If I have got more time, maybe I will have a try with it.

## User

User here references accounts registerd in web gui program. (Don't miss it up with shadowsocks port identified account). The first one to signup becomes Manager by default. 

For example, if a visitor happens to register in this application before you register to be manager, then this one is the manager of your website application and could have all privileges defined by `minor-sspy-mgr`.

So, after deploying this program, you should visit your own sites and register as a user as quick as possible.

### Signup

Email should be provided for recieving check code and signin. User password should have a length limit which means password must consist of at least 6 characters/digits/signs and at most 32 characters/digits/signs.

When visitor visit `/home/signup` page, server will store a key `usersignup` with its value to be True. Then the visitor can click `Get code` button, and get the check code by his/her email address. Send check code action is done in section [Email](#email).

The user quantity is limited to 8 by default. If the user quantity registered in database has reached 8, then signup interface is not available any more. In other words, no visitor can signup to `minor-sspy-mgr` from then on. But new user can also register by `/home/strictsignup` routes which needs invitation code.

Manager can modify the default maximum quantity of registered user.

### Strict signup

User who has invitation code can register into `minor-sspy-mgr` through this route.

Only manager and the persons that are specified by manager can generate invitation code.
Manager can generate invitation code as many as he want. The specified man can only generate such a code once a month (or specified times as manager setting).

### Signin

Email is used as key factor for identity.

If a visitor has signined, he/she should be identified by session stored in database, then he can access shadowsocks if his identity is confirmed by manager. 

Normal user can have a view of:

- what his port and corresponding shadowsocks password is. 
- how much flow he has used during order effects.
- how many days before his order over.
- update shadowsocks account password

Manager can have a view of:

- normal user information (Who is registered and when he registered)
- normal user action 
- add/remove new shadowsocks account

### Reset password

User can change his password if he forget it. Password will be modified after accessing `/home/resetPassword` page and set new password. Visiting this page with email form finished and reset link sent to corresponding email, then click the link provided in your email box, put in new password will replace the old one with new one.

### Manager Generate Invitation Code

Manager con generation invitation code or url, then he can send it to its friends and invite them to be a user. The code will be a random string that consists of digits/lowerLetters/upperLetters with 32 chars length.

Invitation would contains at least following columns:

- expire time: when the code is invalid
- new user level ( default as 2 )
- used time: when the code is used for signup

Invitation feature will be implemented in later versions.

### User level

All user registered without invitation code have a default level as 1, the manager could rise as well as down the level (The least level is 1). User level only affects the order subsystem now. 

Order coming from user with level 9 will be confirmed after it is placed. In other words, the user can immediately use the shadowsocks service after he click the button on order page.

## Email

There only one way to send email in minor-sspy-mgr currently, which is `smtp`. Email feature is implemented with python build-in lib `smtplib`. Manager has to configure the `~/.sspy-mgr/config.yaml` file to enable this feature (Or You may fail to send email to visitors). The email is send by smtp server through SSL by default. Because I found that smtplib.SMTP class may not work on some vps if the vps is abroad, but the smtplib.SMTP_SSL class performs well for me. I do think it's a better way to connect to smtp server with SSL enabled, if you have a better solution, change the `mail.py` file under webserver package.

Email configuration should be set before you use the application. The application will throw an except currently if configuration file can not be found. When application starts, some module may take charge of creating a default configuration file in later version. 

Now, you have to make directory `~/.sspy-mgr` manually, the '~' stands for you home directory if you know some about linux shell. Then touch a file named `config.yaml` under the directory you just create. Place following content in the file, remaind that you have to replace account, password and host with your own ones:

```yaml
email:
  account: 'your-smtp-account'
  password: 'your-smtp-password'
  host: 'your-smtp-server-host'
# port: 465
```

Yeah you could set port or not, if your smtp server provide the smtp server in an unordinary port, you could change it. In most cases, just leave it commented.

## Product And Order

Each user will have a buffer period if he/she has been certified by Manager. By the way, if the user is not certified by manager, he/she will not be able to place an order.

By default, the product systems have 5 choice for different usage. The basic flow price is 10G/1￥, but you have noticed that it is not invariable. That is, the more a user paied, the more flow he will gain. Generally, The cheaptest one has the shortest duration by 7 days, any other order type is a little more efficient than that one.

Default product types with different price and flow:

| price | duration | flow | buffer period |
| :---- | :------- | :--- | :---------    |
| ￥1   | 7  days  |  8G  | 4 hours       |
| ￥2   | 15 days  |  18G | 8 hours       |
| ￥2.5 | 15 days  |  24G | 10 hours      |
| ￥4   | 30 days  |  40G | 1 day         |
| ￥5   | 30 days  |  55G | 1 day         |

When stored in database, `duration` and `buffer period` will be transfered into seconds by total_seconds provided by timedelta. `flow` will be transfered into equal quantity in the unit `Mb`.

The user level will have an effect on buffer peroid, for example, user with level 1 have 4 hours buffer period, but user with leve 2 could have 6 hours period( as the rate to be 1.5). The rate with corresponding level is not certain yet.

### Payment method

Manager have to enter settings page, upload his alipay or wechat pay qrcode. Then he can recieve money from users.

### Manage product types

Yeah, with manager previlige you can modify the duration or flow or buffer period of basical product types, manager can also add a new type or delete a existing type.

### Place an order

Because vps maintainer (who is also website manager) may have no alipay business interface or wechat business interface both of which required at least individual business qualification. But, how could we students gain such qualification? So it's better to change our mind into another way, we could place our alipay/wechat recipt qrcode on our websites. 

When our friends want to use shadowsocks service, he/she can pay it by recipt qrcode provided on websites. After finishing money transfering (user may have to click a button to inform the website application to know the user has paied), and then the user will have a buffer period to use the shadowsocks service before manager confirms that the money has been transfered into his account. 

For some reasons, we have to let user to choice whether he needs buffer period (Needs by default). If the user chooses to take the buffer period, he can access the shadowsocks service immedialtely. And the buffer time will be counted in the Total available time that his order corresponds. If not so, then the timer will be started after the next time he logined in our website and select start timer to gain shadowsocks service (Surely this order should be confirmed by the manager). 

I know the process is very complex for both manager and user, but there seems no better way to share our billing with our friends who want to share shadowsocks service. If you think that's too fussy, you may hvae to think about make order duration increasing as well as price rising.

The following situation has benn considered but may not be perfect:

- If the manager rejects the order for the reason that he has not recieved the money, the user may loss the buffer period until next month (namely 30 days, which starts from the time he place the order) if the user is the first time to pretend to have payed for responsible service. Each time the user fails to pay but still says he have payed will make corresponding times of 30 days period for him not able to gain buffer period. In other words, after he has ordered, he can not access the shadowsocks service until the manager accepts the order (Manager recieves responsible money).

- If the manager confirms and accepts the order, then the shadowsocks service duration will be the same as the database record. For example, if a user table the ￥1 order at 13:00, and then this guy can have an access to shadowsocks service for only 2 hours until 15:00. If manager confirms and accepts this order between 13:00 and 15:00, then shadowsocks service for this user will last till 13:00 next week.

- If the manager failed to confirm the order within the required time, the user may have no access to shadowsocks service when buffer period is over. Note, the timer should also pause before the manager confirms the order. For example, if a user take the ￥1 order at 13:00, and then this guy can have an access to shadowsocks service for only 2 hours until 15:00. After 15:00, the timer pauses. when manager confirms and accepts the order at 17:00, the service duration will end at 15:00 next week.

Before a user can start to place an order, he/she'd better contact with manager and make sure that the manager can confirm the order. Because Manager may not be able to response immediately (Manager will be noticed by email, of course he can check his alipay or wechat to know whether his friends takes an order).

### About cancling an order

What about cancling an order if a user do not want to access shadowsocks service, I do not think that is a good way to deal with that. First, as I have mentioned before, we assume that those users who is using our vps resources are our friends. You, the manager of the vps and provider of shadowcocks service, may want to make the order duration as longer as it could be, then you have no need to check for your email or wechat message and then confirm the order on the website. But your friends, the users of your vps resources may want to spend as little as he can. The two opposite demands are conflicts due to out of alipay or wechat pay interface. If you happens to own pay interface provided by alipay or wechat, you could consider using shadowsocks-manager instead which is better designed and more robust. To solve the conflicts, you and your friends should make an aggreement that he will not get refund after he/she has paied. That's out of the scope of this application's.

### After taking order and paied

After user have taken an order with the order paied, the shadowsocks ip address, port and password should be sent to his email address in case webserver thread is stopped.

## Manager

The manager's interface is much more complex than user's interface. Manager should have a total control on his website, so there will be much more pages for manager. But I want to make the order subsystem running at first, and later manager interface will be completed if time allows.

## Web GUI

### settings

Setting range currently include:

- aplipay
- wechat pay
- signup maxmium without invitation
