# Unofficial-Transfermarkt-API
THIS IS AN UNOFFICIAL API
This API is made with Python together with the Beautiful Soup library and uses Flask for the calls.

#Features 

##1. Get some general infos of a player
This will return a JSON object with:
- The club the footballer plays in
- The date of birth and age
- The height
- A link with their profile image
- Their nationality
- The position they play in
- Their value in euros
##2. Get the trophies the player won
This will return an array of all the trophies won in their career. If the same trophie is won more than once, you will recieve Xnumber Trophy Name.
##3. Get the career stats of the player
This will return a JSON object with:
- Their career matches 
- Goals
- Assists
- Yellow Cards
- Red Cards
