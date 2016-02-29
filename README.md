# Swiss
Swiss-system tournament manager in python 3. 

## Running
Prerequisites: python3.

To run, do `python3 swiss.py`, then input player data, matchups, et.c.

To run with input.txt as input, simply pipe it: `cat input.txt | python3 swiss.py`.

## Input syntax
Lines starting with # are comments

A command is written in the form of: [command name] [arg0] [arg1] [arg2] ...

Each command ends with newline

## Available commands

```
addplayer [name]
```
  Adds a new player with the given name. All added names must be unique.

```
delplayer [name]
```
  Remove an existing player. Wins against him/her will be kept. The player must exist. If a previously deleted player is added again, he will keep wins. and previous matchup data from before deletion. Useful if a player leaves the tournament, or wishes to skip a round.

```
result [name of winner] [name of loser]
```
  Registers that the two player have played each other, and increments the wins of the winner. Players must exist, and may not be the same player.

```
end
```
  Denotes end of input. Calculations will be made.
