API Reference (parkle v0.2.1):
==============================

Concepts:
---------

A game of Parkle has two or more players with scores, and a set of six dice.
The players are represented by instances of the `ParklePlayer` class, and
the dice are represented as a flattened or nested list. More on the dice
later.

Instances of `ParklePlayer` are either real players or AI bots.

A `Parkle` class manages the game state and the players. It calls methods
the players can take turns, and keeps track of their score. Each `Parkle`
instance is required to have a `ParkleView`, which is updated periodically.
The `ParkleView` is responsible for drawing the game state to the screen
(the `ParkleConsoleView` class outputs the game state to `stdout`).

For each round, the `Parkle` instance calls methods to simulate a players
turn. First, it calls the players `begin_turn` method. Then, it rolls the
dice (nested) and passes the necessary information to the player with the
method `decide()`. At this point, the player must analyze the
roll and figure out what to keep. The `Parkle` instance is given control
again, and, depending on what the player did, analyzes the output, manipulates
the score, and potentially allows the player to repeat the process. At the
end of the turn, the player `end_turn()` method is called.

After each round, the `Parkle` object checks the highest player score. If
it is over the goal, it announces the winner and the game ends.

The dice are represented in two formats: nested and flattened.

Nested is the standard, and is used internally by Parkle. It looks like
this:

    [[value, number], ...]

For example, `[[2, 3], [4, 1], [6, 1]]` would be a roll with three twos,
one four, and one six. Note that there are not necessarily six values.

Flattened is only provided in case an AI bot wants it. It looks like
this:
    
    [value, value, ...]

The previous example would look like `[2, 2, 2, 4, 6]` in a flattened state.

To convert between the two formats, use `nest_dice()` and `flatten_dice()`.

Functions:
----------
`copy_dice()`
`flatten_dice(dice)`
`nest_dice(flattend_dice)`
`roll(n)`
`points_possible(dice)`
`calculate_one_keptset(keptset)`

Classes:
--------
`Parkle`
`ParklePlayer`
`ParkleView`


Implementations:
----------------
`RealPlayer`
`ParkleConsoleView`
