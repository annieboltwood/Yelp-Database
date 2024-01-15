# YELP DATABASE APPLICATION
This Yelp Database Application has a terminal interface for interacting with Yelp data stored in a SQL Server database. The application can be run directly on the workstations in CSIL without requiring compilation by the tester.

# Disclaimer on Database Access
Due to privacy, access to the database is restricted, and the application cannot be run with the actual database. However, you can watch a demonstration of the application in action by following the link to the video below.

[DEMO VIDEO](https://youtu.be/znOJ5ufpwRg) <br>

As well, I have included the .py file in the repository and the program functionalities below.

# Application Functions
LOGIN<br>
1. Lets user to log in to the interface to access all other functionalities<br>
2. Requires entering a valid user ID which then checks the database for validation<br>
3. Displays an appropriate message if the user ID is invalid<br>
4. Opens a menu with selections for the user to choose<br>
<br>
SEARCH BUSINESS<br>
1. Lets user search for businesses based on inputted filters<br>
2. Filters: minimum number of stars, city, and name<br>
3. Provides three ordering options: name, city, or number of stars<br>
4. Displays a list of search results with business information<br>
<br>
SEARCH USERS<br>
1. Lets user to search for other users based on inputted filters<br>
2. Criteria include name (case-insensitive), minimum review count, and minimum average stars<br>
3. Displays a list of search results with user information<br>
<br>
MAKE FRIEND<br>
1. Lets user select another user from the search results and create a friendship<br>
2. Records the friendship in the Friendship table<br>
<br>
REVIEW BUSINESS<br>
1. Allows a user to review business<br>
2. Enter the business ID<br>
3. Enter the number of stars<br>
4. Application records the review in the Review table<br>
5. Updates the number of stars and the count of reviews for the reviewed business (through trigger)<br>
<br>
