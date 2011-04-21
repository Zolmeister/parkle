API Reference (parkle v0.2.1)
=============================

Concepts:
---------

### How Parkle Works
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

Each `ParkleView` has an attribute `players`. This is a list of `ParklePlayers`.
To start a game, instantiate a `ParkleView`, populate its `players` attribute
in an overridden `ParkleView.start_game()`, and call `ParkleView.begin_game()`.
`ParkleConsoleView` provides this functionality for free.

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

To recap:
1) Instantiate a `ParkleView`.
2) Populate the `ParkleView` `players` attribute.
3) Call `ParkleView.begin_game()`, which instantiates a `Parkle` game object.
4) The `Parkle` instance does some initialization.
5) The `Parkle` instance simulates player turns by asking the players
   what they want to keep.
6) The `Parkle` instance figures out scoring.
7) After each round, the `Parkle` instance checks if anyone has won.


### Dice
The dice are represented in two formats: nested and flattened.

Nested is the standard, and is used internally by Parkle. It looks like
this:

    [[value, number], ...]

For example, `[[2, 3], [4, 1], [6, 1]]` would be a roll with three twos,
one four, and one six. Note that there are not necessarily six values.
All of the dice that are passed in to the `ParklePlayer` from the
`Parkle` instance will be in the nested format.

Flattened is only provided in case an AI bot wants it. It looks like
this:
    
    [value, value, ...]

The previous example would look like `[2, 2, 2, 4, 6]` in a flattened state.

To convert between the two formats, use `nest_dice()` and `flatten_dice()`.

### Sets

The method that calculates points, `calculate_one_keptset()`, operates
on "sets" of kept dice.

The reason for this is simple: a triple of three fives is worth
500 points, but three separate fives are worth 150 points. There
is no way for `Parkle` to figure out the distinction unless
it is told.

So, when you play as a human (or an AI bot plays), sets of dice
*must* be grouped together properly.

Internally, a set is simply a list of integer values.

### Player Turns

Each `ParklePlayer` object has an attribute `n`, which is the index
in the player list that that object occupies.

These values are passed in to the `ParklePlayer` turn methods:

- `dice` - a copy of the "official" nested dice for the roll.
- `all_scores` - a list of the scores for all players.
- `round_score` - the number of points accumulated for the round up to the
  previous roll.

The current total score for a player is given be `all_scores[player.n]`.

The `decide()` method is responsible for returning a code to tell
the `Parkle` instance what to do next. Return `1` to continue rolling,
`0` to stop the turn, and `-1` to forfeit.

Since the decision itself is not returned to the `Parkle` instance,
it needs some way to figure out what the player wants to keep. The
solution is a `ParklePlayer` attribute `kept`.

`ParklePlayer.kept` is a list that is cleared at the beginning of each
turn. For each roll (each time `decide()` is called), there should
be a separate group in `ParklePlayer.kept`. After three rolls, it should
look like:

    [[group 1], [group 2], [group 3]]

Each group should be a list of sets.

Functions:
----------
`**copy_dice(**dice**)**`
Return a copy of the nested dice `dice`.

Returns: list

`**flatten_dice(**dice**)**`
Return a flattened copy of nested dice `dice`.

Returns: list

`**nest_dice(**flattened_dice**)**`
Return a nested copy of flattened dice `flattened_dice`.

Returns: list

`**roll(**n**)**`
Return a nested dice set of size `n`.

Returns: list

`**points_possible(**dice**)**`
Return whether it is possible to get points with a nested dice `dice`.

Returns: Boolean

`**calculate_one_keptset(**keptset**)**`
Return the points possible for a kept set `keptset`.

For the point values for sets, see [this](http://www.github.com/bradzeis/parkle/master/docs/rules.md) document.

Returns: int

Classes:
--------

### `ParklePlayer`
`**begin_turn(**all_scores, round_score**)**`
Called at the beginning of a player's turn.

`**end_turn(**all_scores, round_score**)**`
Called at the end of a player's turn.

`**decide(**dice, all_scores, round_score**)**`
Called for each roll. This is where the player decides what to keep.

Append a group of sets to `ParklePlayer.kept` for each roll.

Return: -1 to forfeit, 0 to stop, 1 to continue

### `ParkleView`
`**start_game()**`
Usually used as the entry point for the game. Create the
list of players here.

Always end this method with a call to `begin_game()`.

`**begin_game(**players=None**)**`
`**end_game()**`
`**start_round()**`
`**end_round()**`
`**start_turn()**`
`**end_turn()**`
`**roll(**dice**)**`
`**decide()**`
`**invalid_decision()**`

Implementations:
----------------
`ParkleConsoleView`
This implementation of `ParkleView` outputs the game state to `stdout`.

`RealPlayer`
This implementation of `ParklePlayer` allows users to specify what to
keep in the `decide()` method.

The output looks like this:

    Roll n:
        v v v v v

    [k, k, k] [k, k, k] | [v]

The "v, v, v, v, v" part is what is left on the table.
The "[k, k, k] [k, k, k]" part is what was kept from previous rolls.
The "[v]" part is what is in the current set for this roll so far.

The "k" and "v" parts are always separated by a pipe character ("|").

The controls for human players are simple:

- "[1-9]" - select a number from the current dice on the table
- "c" - continue rolling, keeping your current sets
- "s" - end your turn with your current sets
- "p" - clear the sets you have formed from the current roll (old sets stay)
- "n" - create new set
- "l" - forfeit the game

`JimmyBot`
This is an experimental implementation of an AI bot to test bot functionality.
It is not meant to be a real opponent.

