from tournament import Tournament

print("Letsago")
t = Tournament()

print("Adding")
t.add_result_by_names("foo", "bar", 3, 0)
t.add_result_by_names("foo", "baz", 0, 3)
t.add_result_by_names("zorg", "baz", 1, 1)
t.add_result_by_names("zorg", "foo", 2, 1)
t.add_result_by_names("baz", "bar", 2, 1)

print("Adding done")
t.print_round_matchups()
