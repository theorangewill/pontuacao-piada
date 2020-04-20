# pontuacao-piada

This is a script that uses the Twitter API to score jokes from friends.

To use, you only need to mention the profile you want to notify about these scores plus the points of the mentioned joke.

For example:

Someone: Today, my son asked "Can I have a book mark?" and I burst into tears. 11 years old and he still doesn't know my name is Brian.


You mention this tweet as:
\@PROFILE_TO_NOTIFY 10

of
\@PROFILE_TO_NOTIFY -1000

This script must detect new masters (those who give points) and new players (those who receive points)

At the end of the week (every Sunday), \@PROFILE_TO_NOTIFY tweets the scoreboard of each master. It is not possible yet to send tweets longet than 280 characters.
