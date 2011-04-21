Creating a Bot (parkle v0.2.3)
==============================

First, make sure you have read and understand the [framework](http://www.github.com/bradzeis/parkle/blob/master/docs/api.md).

To create a bot, just follow this method:

1. Implement `begin_turn()`, if necessary.<br />
2. Implement `decide()`.<br />
    1. Create an empty list `group`.<br />
    2. Create a copy of the dice passed in (`copy_dice()`) so that you have
       something to fall back upon if your bot messes up.<br />
    3. For each set, create a list `keptset` and append it to `group`.<br />
    4. At the exit point, append `group` to `ParklePlayer.kept` and return
       the correct return code.<br />
3. Implement `end_turn()`, if necessary.<br />

Look at the `RealPlayer` and `JimmyBot` source for examples.

Be sure to look at the API and use the `points_possible()` and `calculate_set()` method
to analyze your sets/dice.
