# Projet_DSIA_ESIEE_Paris_Nicolas_Charpentier
 Github for my project of full stack data application
 
 This API was made with FastAPI and run on docker with a docker-compose file. It's also made of a database postGreSql to store all the information.
 The Front-end is made of javascript with React.

## Subject
The objectives of this project was to create an API that could be use for a bank. We have 3 mains parts on it : 
 
A system to create new users (with the possibility to be an admin user if we put the good password (here it's 9999)) and to log in.

Several functionalities for the users, like a bank would propose :
   - See the balance
   - See the IBAN,
   - Register a deposit
   - Do a transfer toward another user
   - Register a subscription to another user (in this case the amount is withdraw every minute)
   - Block the account to deny transaction
   - Delete the account

 Several functionalities for the admin users :
 - Display all the registered members with their information
 - Do a deposit to a user by using the money of the bank
 - Delete all the users

 
## How to run and use it without Front End
 Go into the folder and execute :
 ```
 docker compose up --build
 ```

Then connect to :

 ```
http://localhost:8080/docs
 ```
To run the API without the front end and with the docs means all functionalities have to be operated by first clicking on "try it out", then filling the necessary information, and finally clicking on "executing".

Once you are there, you can create a new user on "/nouveau_user", then log in with the credentials used on "/connection". If you want to have a admin account, specify "9999" in "password_admin" when creating a user.
To create a new user, you need to file the json file with the information about the user.

When you execute the "/connection", you obtain a token, copy it without the quotation mark in the Authorize button. After that you will have access to the user part if you're only a user, and the user and admin part if you're an admin.

For the transfer and subscription part, you can use your own IBAN, but creating another user and using his IBAN is better to test.

In case you need more money, create an admin account and use the function "admin_transation" to transfer money to a user using his IBAN (Admin have infinite money).

When you delete your account as a user, or all the accounts as a Admin, you'll have to disconnect from the Authorize button before doing anything else.

If you create a subscription, the amount is transfered to the specify user every minutes until you delete the subcription using the ID, delete one of the user concerned, or don't have enough money to pay.

Finally in the historique part, all movements of money concerning the user are displayed in this order : 
- [deposit]
- [transfer from the user to another user]
- [transfer of another user toward this user]
- [subscription of the user toward another user]
- [subscription of another user toward this user]

## How to run and use it with Front End
 Go into the folder and execute :
 ```
 docker compose up --build
 ```

Then connect to :

 ```
http://localhost:3000
 ```

Once on the page you'll have to register a new user. Use the credentials to then connect in "Log in".

You'll be transported to the user dashboard part, were you can use all the functionalities. You can also navigate on the admin dashboard, but you'll only be able to use the services if your account is an admin one.

To have more information about all the services, it's recommended to read the in formation in "How to run and use it without Front End" that is more detailed.

## Difficulties

While doing this project I faced several problems.

The first was the creation of the file tree. Starting from my idea and the previous tp, I still got a hard time creating it, and had to modify it several times.

Then, the modification of my models in the model folder leads to several problem with the database. I had to delete all the image and container to solve the issue.

Third problem was the adaptation of the authentification from the TP to my code. Because of an error with GitHub, my tp got deleted and I had to use the one given in the GitHub of the class. I took me some times to remember how to use it to then be able to adapt it to my code.

The final functionaly implemented was the subscription. This lead to the question of how to do for the amount to be automatically transfer between 2 accounts every X time. For that I asked ChatGPT and he propose the idea of the scheduler. With his help I was able to implement it, to make the subscription work every minutes.

The final problem was the question of the Front end. I tried to do some HTML to create a HTML but didn't succeed. I then had to asked chatGPT and to generate one and was able to get a pretty good one with enough time. It's not totally finish but the result is good.

## Competences acquired

Thanks to this project I was able to learn a lot of things. The use of FastAPI and how an API work in general, with a concrete project done to really learn to use it. How to use Docker, a Docker File, a Docker Compose File, an Image an so on. How to connect a Database and an API to work together. And finally, more information about how to use GitHub.
