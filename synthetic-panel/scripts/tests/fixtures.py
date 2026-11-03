"""Shared test fixtures: build small panel dicts in code."""


def persona(pid, choice, intent, order, traits=None):
    return {
        "id": pid,
        "name": f"Persona {pid}",
        "summary": "test persona",
        "traits": traits if traits is not None else [
            {"trait": "age 38", "basis": "grounded", "source": "G1"},
            {"trait": "shops weekly", "basis": "assumed"},
        ],
        "order": order,
        "response": {
            "choice": choice,
            "intent": intent,
            "objection": "too pricey",
            "quote": "I'd scroll past.",
        },
    }


def panel(choices, decoy_id="D", traits=None, single_context=False, orders=None):
    """choices: list of chosen stimulus ids, one per persona."""
    stimuli = [
        {"id": "A", "text": "Dinner sorted in 15 minutes", "decoy": False},
        {"id": "B", "text": "Fresh food, less waste", "decoy": False},
        {"id": "C", "text": "Chef-designed recipes", "decoy": False},
        {"id": decoy_id, "text": "Meal kits for everyone", "decoy": True},
    ]
    ids = [s["id"] for s in stimuli]
    people = []
    for i, c in enumerate(choices):
        order = orders[i] if orders else ids[i % 4:] + ids[:i % 4]
        intent = {s: (6 if s == c else 3 + (i % 3)) for s in ids}
        people.append(persona(f"P{i + 1:02d}", c, intent, order, traits))
    return {
        "run_id": "2026-11-01-test",
        "date": "2026-11-01",
        "project": "test",
        "question": "Which headline gets the most clicks?",
        "decision": "Pick the launch headline",
        "segment": "Busy Sydney parents",
        "metric": "click",
        "single_context": single_context,
        "grounding": [{"id": "G1", "source": "survey", "summary": "Parents 30-45"}],
        "stimuli": stimuli,
        "personas": people,
    }
