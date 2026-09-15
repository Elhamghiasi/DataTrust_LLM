from datatrust.corruption import make_context


def test_clean_is_unchanged():
    context = "According to the periodic table, Iron has atomic number 26."
    assert make_context(context, "26", "clean", 42) == context


def test_missing_removes_answer_bearing_phrase():
    context = "According to the periodic table, Iron has atomic number 26."
    changed = make_context(context, "26", "missing", 42)
    assert "atomic number 26" not in changed


def test_contradictory_contains_gold_and_conflict():
    context = "According to the periodic table, Iron has atomic number 26."
    changed = make_context(context, "26", "contradictory", 42)
    assert "atomic number 26" in changed
    assert "Source B" in changed
