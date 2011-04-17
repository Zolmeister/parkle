Parkle v0.2 
=========== 

Parkle is an open-source [Farkle](http://en.wikipedia.org/wiki/Farkle)
implementation that allows for human versus human, human versus AI, 
and AI versus AI games.

Parkle started as a means of easily putting competing AI bots head to head
in a game that offers a good balance between luck and strategy.

To play, clone/download the repository, `cd` to the parkle directory, and run:

    python play.py

Requires Python 2.x.

How to Play:
============

If you do not know how to play Farkle, read the rules [here](http://en.wikipedia.org/wiki/Farkle).

After you create the players, the first player will "roll". That player
then selects dice and continues rolling.

When selecting dice, it is important to group together the dice into
sets. For example:

    [5] [5] [5] = 150 points
    [5, 5, 5] = 500 points

At the beginning of your turn, a set is created for you. To enter a
die into the group, type a numer and then hit enter.

To create a new set, enter "n".

When you are satisfied with the groups that you have created for that
roll, you can either:

    "c" - roll again
    "s" - end turn
    "l" - quit game

If you want to start over for the current roll, press "p". This will
only undo what you have selected for the current roll. You cannot
change what you have selected in previous rolls.

The first player to reach 10,000 points wins.

Creating a Bot:
===============

To create a bot, you need to create a subclass of `ParklePlayer`.

In the `__init__` method, define `name`.

Then, implement the `decide(dice, round_score)` method. The best way to
do that is:

1. Create a copy of the `dice` argument (using `parkle.copy_dice(d)`).
2. Create an empty list (this is a group of sets)
3. Create another empty list (this is the current set)
4. Analyze the dice copy/current score/score of other players. DO NOT CHANGE
ANY SCORES.
5. Add dice to the current set. After each set is complete, add it to the group
and create another empty set.
6. Append the group to `self.kept`.
7. Return 1 to roll again, 0 to end turn.

Parkle v0.2 comes with a sample AI bot, JimmyBot. Note that this is just a
proof of concept, it is not intended to be a real opponent.
