# Keep-it-Up
http://morciu.pythonanywhere.com/login
a website that keeps track of activities
My final project for CS50 is a web application called Keep It Up.
It's mainly a To-Do-List Website with a few extra functionalities.

I've used Python with Flask and SQL for the backend part and decided not to use any Bootstrap to force myself to learn HTML, CSS and JavaScript better.

After you create an account and enter the currency you want to use you can do the following:

- Register a task together with its description, start date and deadline.
- Register an event with its description and date.
- Register a product warranty with its name, price, receipt nr, store and store link, and warranty dates.
- In the "Today" section there is a small daily form where you can register total money earned/spent in the selected currency and a slider with which you can rate your day from 0 to 100

There is a sidebar with the website sections 'Today', 'This Week', 'This Month', 'This Year'.
    In the sidebar there is a 'Warranties' section that will display all registered warranties.
    In the sidebar there are 'Log In', 'Log Out', 'Register' buttons.
    In the sidebar there are buttons to register new tasks, events, warranties.
    In the sidebar there is a section that displays information from your daily form; if you are in the 'Today' section it will display the total earned, total spent, total balance and rating entered on the current date.
    If the user is in 'This Week', 'This Month', 'This Year' the section that displays the daily user input in the sidebar wiill display total earned, total spent, total balance, average rating for the respective time intervals.
The website reads the information you registered from the SQL and displays it in tables in the correct section.
You can expand an element to read it's details and the website will scroll to that popup section.
You can delete tasks.
You can mark tasks as being 'Completed' or 'Not Completed'.
Completed tasks are hidden by default when the page loads, you can unhide them by clicking on the checkbox above.

I have used CS50 library for python to manipulate SQL.
I've implemented the same encryption hash method used for passwords in the previous problem set.
