Parkle v0.1 
=========== 

Parkle is an open-source [Farkle](http://en.wikipedia.org/wiki/Farkle)
implementation that allows for human versus human, human versus AI, 
and AI versus AI games.

Parkle started as a means of easily putting competing AI bots head to head
in a game that offers a good balance between luck and strategy.

The v0.1 release of Parkle only allows human versus human games, but
it will be trivial to plug in AI in the v0.2 release.

To play, clone/download the repository, `cd` to the parkle directory, and run:

    python play.py

Requires Python 2.x.

How to Play:
============

If you do not know how to play Farkle, read the rules [here](http://en.wikipedia.org/wiki/Farkle).

After you create the players, the first player will "roll". That player
then selects dice and continues rolling.

When selecting dice, it is important to group together the dice. For
example:

    [5] [5] [5] = 150 points
    [5, 5, 5] = 500 points

At the beginning of your turn, a group is created for you. To enter a
die into the group, type a numer and then hit enter.

To create a new group, enter "n".

When you are satisfied with the groups that you have created for that
roll, you can either:

    "c" - roll again
    "s" - end turn

If you want to start over for the current roll, press "p". This will
only undo what you have selected for the current roll. You cannot
change what you have selected in previous rolls.

The first player to reach 10,000 points wins.
