# Farm-Commerce
This project is an e-commerce site desgined to help farmer to sell their products.
Every week they can propose to their customers a stock of vegetables.
The customers will then create a cart in the limit of this stock and then confirm their choice.
The farmer will then access to a dashboard where he will find a summary of the harvest he need to do and a summary of how to dispatch it in every cart with the related customer's informations and price.

This app is developped with Django, HTML, CSS and Javascript.

The code is seprated in three apps.
- An account app with a custom account model and manager. 
- A "Panier" app that manage the customer side of the app. Including the market view where the customer choose the vegetables he wants to add to his cart. And cart view to manage his cart.
- A "Producteur" app that manage the farmer side of the app. It includes a dashboard with the summary of the whole harvest and a detailed view of every cart.

The frontend part has been set up with a free bootsrtap template:
https://www.free-css.com/free-css-templates/page279/tropiko
