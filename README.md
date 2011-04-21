Parkle v0.2.1 
============= 

Parkle is an open-source [Farkle](http://en.wikipedia.org/wiki/Farkle)
implementation that allows for human versus human, human versus AI, 
and AI versus AI games.

Parkle started as a means of easily putting competing AI bots head to head
in a game that offers a good balance between luck and strategy.

To play, clone/download the repository, `cd` to the parkle directory, and run:

    python play.py

Requires Python 2.x.

How to Play Parkle:
===================

If you do not know how to play Farkle, read the rules [here](http://en.wikipedia.org/wiki/Farkle).
The basic rules of Farkle are used in Parkle. For a list of possible
point values, read [this](http://www.github.com/bradzeis/parkle/master/rules.md)
document.

After you create the players, the first player will "roll". That player
then selects dice and continues rolling.

When selecting dice, it is important to group together the dice into
sets. For example:

    [5] [5] [5] = 150 points
    [5, 5, 5] = 500 points

Create a separate set for 3-, 4-, 5-, and 6-of-a-kinds, straights,
three pairs, and two 3-of-a-kinds. To add all of the current dice
into the current set, enter "a".

At the beginning of your turn, a set is created for you. To enter a
die into the group, type a numer and then hit enter.

To create a new set, enter "n".

When you are satisfied with the sets that you have created for that
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

Then, implement the `decide(dice, all_scores, round_score)` method.

- `dice` - the dice rolled that turn (output by `Parkle.roll(n)`)
- `all_scores` - a copy of the game's list of scores. You can
determine your position with `all_scores[player.n]`
- `round_score` - the points accumulated this turn, minus the
current sets that you construct in the `decide()` method.

The best way to do that is:

1. Create a copy of the `dice` argument (using `parkle.copy_dice(d)`).
2. Create an empty list (this is a group of sets) called `group`.
3. Create another empty list (this is the current set) `keptset`.
4. Analyze the dice copy/round score/score of other players.
5. Add dice to the current set. After each set is complete, add it to the group
and create another empty set.
6. Append the group to `self.kept`.
7. Return 1 to roll again, 0 to end turn.

Parkle v0.2.1 comes with a sample AI bot, JimmyBot. Note that this is just a
proof of concept, it is not intended to be a real opponent.

To load a bot into the game, select "a" when adding players, enter the
name of the python file where your class resides (with the .py extension),
and the name of your class.

Documentation:
==============

[Point Values/Rules](http://wwww.github.com/bradzeis/parkle/master/docs/rules.md)
[API Reference](http://www.github.com/bradzeis/parkle/master/docs/api.md)
[Bot Creation](http://www.github.com/bradzeis/parkle/master/docs/bots.md)

