# Swiss
A library for managing Swiss-style tournaments in Python 3.

Use it as a backend for your application, or just call Python code interactively to manage your own local Tournaments.

## Prerequisites

Install prerequisites:

    python -m pip install networkx

## Usage example

    import matchup_strategies.min_cost
    from match_log import MatchLog

    # Create a MatchLog, which will keep track of results
    match_log = MatchLog()

    # Register your players
    match_log.add_player("Lina")
    match_log.add_player("Mia")
    match_log.add_player("Ina")
    match_log.add_player("Kajsa")

    # Generate first round of matchups and print them
    # Swiss-style tournaments have multiple variations with different ways to break ties.
    # In this case we use matchup_stategies.min_cost, a good default.
    matchups = matchup_strategies.min_cost.pairings(match_log)
    print("Round 1 Pairings:")
    print(matchups.string())

The code above will print a list of who faces who.

Output:

    Round 1 Pairings:
    Lina VS. Mia
    Ina VS. Kajsa

Let's say you play a round of Swiss according to these pairings. You could then register the results and generate matchups for the next round by appending this code to the Python code above:

    # Let's say that Lina defeated Mia 1 point to 0
    match_log.add_result("Lina", "Mia", 1, 0)
    # ... and that Kajsa defeated Ina 1 point to 0
    match_log.add_result("Kajsa", "Ina", 1, 0)

    matchups = matchup_strategies.min_cost.pairings(match_log)
    print("Round 2 Pairings:")
    print(matchups.string())

The matchup strategy we choose will try to make sure that players don't face each other twice, and that they face players with a similar number of wins (among some other things to resolve tiebreakers and an odd number of players).
