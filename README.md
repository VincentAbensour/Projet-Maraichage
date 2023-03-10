# Farm-Commerce

### About the project

This project is an e-commerce site designed to help farmers to sell their products. It's mainly a training project for myself.
Every week they can propose to their customers a stock of vegetables.
The customers will then create a cart in the limit of this stock and then confirm their choice.
The farmer will then access to a dashboard where he will find a summary of the harvest he need to do and a summary of how to dispatch it in every cart with the related customer's informations and price.


### Built With

This app is developped with Django, HTML, CSS and Javascript.

The frontend part has been set up with a free bootsrtap template:
https://www.free-css.com/free-css-templates/page279/tropiko

## Getting Started

### Prerequisites

You will need Python >= 3.11

### Installation

Clone the repo at

> https://github.com/VincentAbensour/Projet-Maraichage.git

In your folder create a virtual environment:

`py -m venv env `

and activate it

`env\Scripts\activate`

Install the required packages

`pip install -r requirements.txt`

Make the necessaries migrations

`py manage.py migrate`

### Usage

You will need an admin account to set up items available for purchase, as would do the farmer.
Create a superuser account, in your terminal write:

`py manage.py createsuperuser`

Then you can connect on the admin panel, ending your localhost adress with /admin and connect with your superuser credentials.

You can then set a new "Week object" that will represent the time that customers have to purchase items linked to this week.

You can set new products (might be vegetables!)

And finally set stockItems that represent the products that are avalaible for purchase during the related week.

Then coming back to the website you can create a new profile by clicking register. The account activation wont work because it's done with an email confirmation. You will need to set it up in src/setting.py and write a valid email adress and password to manage the send.

`EMAIL_HOST_USER =`
`EMAIL_HOST_PASSWORD = `

Alternatively, and for a quick test, you can modify the 'is_active' value of the created account to True in the admin panel. (You need to connect with your superuser account)

When it's done you can add products from the market in your cart and have a look at your cart. When your it's ready you can validate it wich will impact the avalaible stock. If you want to delete or add new items to your cart you will need to invalidate it.

If you connect with an admin account, you will have access to the dashboard where you will have a summary of the carts and what needs to be harvest. You can click on a particular cart and validate it to inform the customer that his cart is ready to be retrieved by sending him an email.

This website doesn't include a payment service.

### About the Code

The code is seprated in three apps.
- An account app with a custom account model and manager.
- A "Panier" app that manage the customer side of the app. Including the market view where the customer choose the vegetables he wants to add to his cart. And cart view to manage his cart.
- A "Producteur" app that manage the farmer side of the app. It includes a dashboard with the summary of the whole harvest and a detailed view of every cart.


