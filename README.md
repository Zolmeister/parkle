Parkle v0.3.0
============= 

Parkle is an open-source [Farkle](http://en.wikipedia.org/wiki/Farkle)
implementation that allows for human versus human, human versus AI, 
and AI versus AI games.

Parkle started as a means of easily putting competing AI bots head to head
in a game that offers a good balance between luck and strategy.

To play, clone/download the repository, `cd` to the parkle directory, and run:
at you construct in the `decide()` method.

The best way to do that is:

1. Create a copy of the `dice` argument (using `parkle.copy_dice(d)`).
2. Create an empty list (this is a group of sets) called `group`.
3. Create another empty list (this is the current set) `keptset`.
4. Analyze the dice copy/round score/score of other players.
5. Add dice to the current set. After each set is complete, add it to the group
and create another empty set.
6. Append the group to `self.kept`.
7. Return 1 to roll again, 0 to end turn.

Parkle v0.2.3 comes with a sample AI bot, JimmyBot. Note that this is just a
proof of concept, it is not intended to be a real opponent.

To load a bot into the game, select "a" when adding players, enter the
name of the python file where your class resides (without the .py extension or the 'ai/' path in front),
which should match the name of your class

Documentation:
--------------

[Point Values/Rules](http://www.github.com/bradzeis/parkle/blob/master/docs/rules.md)<br />
[API Reference](http://www.github.com/bradzeis/parkle/blob/master/docs/api.md)<br />
[Bot Creation](http://www.github.com/bradzeis/parkle/blob/master/docs/bots.md)<br />

