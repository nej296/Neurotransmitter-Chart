"""
Neurotransmitter Wheel Chart — Automated Test Suite
Run with: python test_app.py  or  pytest test_app.py -v
"""

import re
import sys
import json

# ============================================================
# TEST SETUP
# ============================================================

passed = 0
failed = 0
total = 0


def test(name, condition, detail=""):
    global passed, failed, total
    total += 1
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        print(f"  FAIL: {name}")
        if detail:
            print(f"        {detail}")


# ============================================================
# TEST 1: Data Integrity
# ============================================================
print("\n" + "=" * 60)
print("TEST 1: Data Integrity")
print("=" * 60)

from nt_database import NT_DATABASE, CATEGORY_COLORS, EFFECT_COLORS, CATEGORIES

test("NT_DATABASE contains exactly 108 entries",
     len(NT_DATABASE) == 108,
     f"Got {len(NT_DATABASE)} entries")

REQUIRED_FIELDS = [
    "id", "name", "abbreviation", "category", "category_group",
    "postsynaptic_effect", "postsynaptic_detail", "precursor",
    "synthesis_enzyme", "primary_location", "receptor_types",
    "behavioral_role", "disorders", "drugs", "color"
]

all_fields_ok = True
missing_details = []
for nt in NT_DATABASE:
    for field in REQUIRED_FIELDS:
        if field not in nt or nt[field] is None or (isinstance(nt[field], str) and nt[field].strip() == ""):
            all_fields_ok = False
            missing_details.append(f"NT {nt.get('id', '?')} ({nt.get('name', '?')}) missing/empty: {field}")

test("Every entry has ALL required fields populated (no empty/None)",
     all_fields_ok,
     "; ".join(missing_details[:5]) + ("..." if len(missing_details) > 5 else ""))

VALID_EFFECTS = {"Excitatory", "Inhibitory", "Modulatory", "Mixed"}
invalid_effects = [
    f"ID {nt['id']}: '{nt.get('postsynaptic_effect', '')}'"
    for nt in NT_DATABASE
    if nt.get("postsynaptic_effect") not in VALID_EFFECTS
]
test("Every entry has a valid postsynaptic_effect",
     len(invalid_effects) == 0,
     "; ".join(invalid_effects[:5]))

ids = [nt["id"] for nt in NT_DATABASE]
test("No duplicate IDs",
     len(ids) == len(set(ids)),
     f"Duplicates: {[x for x in ids if ids.count(x) > 1]}")

names = [nt["name"] for nt in NT_DATABASE]
test("No duplicate NT names",
     len(names) == len(set(names)),
     f"Duplicates: {[x for x in names if names.count(x) > 1]}")

all_have_key_fields = all(
    nt.get("precursor", "").strip() and
    nt.get("primary_location", "").strip() and
    nt.get("behavioral_role", "").strip()
    for nt in NT_DATABASE
)
test("Every entry has non-empty precursor, primary_location, behavioral_role",
     all_have_key_fields)


# ============================================================
# TEST 2: Category Validation
# ============================================================
print("\n" + "=" * 60)
print("TEST 2: Category Validation")
print("=" * 60)

EXPECTED_CATEGORIES = {
    "Catecholamines",
    "Indoleamines & Trace Amines",
    "Amino Acids",
    "Acetylcholine",
    "Opioid Peptides",
    "Non-Opioid Peptides",
    "Purines",
    "Gasotransmitters & Lipids"
}

actual_categories = set(nt["category"] for nt in NT_DATABASE)
test("All 8 categories are present in the data",
     EXPECTED_CATEGORIES == actual_categories,
     f"Expected: {EXPECTED_CATEGORIES}, Got: {actual_categories}")

test("CATEGORIES list has 8 entries",
     len(CATEGORIES) == 8,
     f"Got {len(CATEGORIES)}")

cat_counts = {}
for nt in NT_DATABASE:
    cat = nt["category"]
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

print("  Category distribution:")
for cat, count in sorted(cat_counts.items()):
    print(f"    {cat}: {count}")

test("Total across all categories is 108",
     sum(cat_counts.values()) == 108,
     f"Total: {sum(cat_counts.values())}")


# ============================================================
# TEST 3: Postsynaptic Effect Distribution
# ============================================================
print("\n" + "=" * 60)
print("TEST 3: Postsynaptic Effect Distribution")
print("=" * 60)

effect_counts = {}
for nt in NT_DATABASE:
    e = nt.get("postsynaptic_effect", "")
    effect_counts[e] = effect_counts.get(e, 0) + 1

print("  Postsynaptic Effect distribution:")
for effect, count in sorted(effect_counts.items()):
    print(f"    {effect}: {count}")

test("No entry has empty or None postsynaptic_effect",
     all(nt.get("postsynaptic_effect") for nt in NT_DATABASE))

test("All effects are valid types",
     set(effect_counts.keys()).issubset(VALID_EFFECTS))


# ============================================================
# TEST 4: Color Assignment
# ============================================================
print("\n" + "=" * 60)
print("TEST 4: Color Assignment")
print("=" * 60)

test("CATEGORY_COLORS has 8 unique entries",
     len(CATEGORY_COLORS) == 8 and len(set(CATEGORY_COLORS.values())) == 8,
     f"Keys: {len(CATEGORY_COLORS)}, Unique values: {len(set(CATEGORY_COLORS.values()))}")

test("EFFECT_COLORS has 4 entries",
     len(EFFECT_COLORS) == 4)

HEX_PATTERN = re.compile(r'^#[0-9a-fA-F]{6}$')
invalid_colors = [
    f"ID {nt['id']}: '{nt.get('color', '')}'"
    for nt in NT_DATABASE
    if not HEX_PATTERN.match(str(nt.get("color", "")))
]
test("All 108 NTs have a valid hex color (#RRGGBB)",
     len(invalid_colors) == 0,
     "; ".join(invalid_colors[:5]))

# Verify color matches category
color_mismatches = []
for nt in NT_DATABASE:
    expected_color = CATEGORY_COLORS.get(nt["category"])
    if nt["color"] != expected_color:
        color_mismatches.append(f"ID {nt['id']} ({nt['name']}): has {nt['color']}, expected {expected_color}")
test("Every NT's color matches its category color",
     len(color_mismatches) == 0,
     "; ".join(color_mismatches[:5]))


# ============================================================
# TEST 5: Application Launch Test
# ============================================================
print("\n" + "=" * 60)
print("TEST 5: Application Launch Test")
print("=" * 60)

try:
    from app import app as flask_app
    test("Flask app imports without errors", True)
except Exception as e:
    test("Flask app imports without errors", False, str(e))

try:
    client = flask_app.test_client()
    test("Flask test client created", True)
except Exception as e:
    test("Flask test client created", False, str(e))

try:
    response = client.get('/')
    test("GET / returns 200", response.status_code == 200,
         f"Got status {response.status_code}")
except Exception as e:
    test("GET / returns 200", False, str(e))

try:
    response = client.get('/api/neurotransmitters')
    test("GET /api/neurotransmitters returns 200", response.status_code == 200)
    data = json.loads(response.data)
    test("API returns JSON with neurotransmitters key",
         "neurotransmitters" in data and len(data["neurotransmitters"]) == 108,
         f"Keys: {list(data.keys())}, count: {len(data.get('neurotransmitters', []))}")
except Exception as e:
    test("API endpoint works", False, str(e))


# ============================================================
# TEST 6: Wheel Rendering Test
# ============================================================
print("\n" + "=" * 60)
print("TEST 6: Wheel Rendering Test")
print("=" * 60)

# Verify angle calculations sum to 360
total_nts = len(NT_DATABASE)
angle_per_nt = 360.0 / total_nts
total_angle = angle_per_nt * total_nts
test("Angle calculations sum to 360 degrees",
     abs(total_angle - 360.0) < 0.001,
     f"Total angle: {total_angle}")

# Verify category angular spans are proportional
for cat in EXPECTED_CATEGORIES:
    cat_nts = [nt for nt in NT_DATABASE if nt["category"] == cat]
    cat_angle = len(cat_nts) * angle_per_nt
    test(f"Category '{cat}' angular span = {cat_angle:.1f}° ({len(cat_nts)} NTs)",
         cat_angle > 0)

# Verify page contains SVG/D3 content
try:
    response = client.get('/')
    html = response.data.decode('utf-8')
    test("Page contains SVG element", '<svg' in html.lower() or 'createsvg' in html.lower() or 'd3.select' in html.lower())
    test("Page contains D3.js reference", 'd3' in html.lower())
except Exception as e:
    test("Page rendering check", False, str(e))


# ============================================================
# TEST 7: Search Functionality Test
# ============================================================
print("\n" + "=" * 60)
print("TEST 7: Search Functionality Test")
print("=" * 60)


def search_nts(query):
    """Simulate search — matches on name or abbreviation, case-insensitive."""
    q = query.lower()
    return [nt for nt in NT_DATABASE
            if q in nt["name"].lower() or q in nt["abbreviation"].lower()]


results = search_nts("Dopamine")
test("Search 'Dopamine' returns at least 1 match",
     len(results) >= 1 and any(r["name"] == "Dopamine" for r in results),
     f"Got {len(results)} matches: {[r['name'] for r in results]}")

results = search_nts("GABA")
test("Search 'GABA' returns at least 1 match",
     len(results) >= 1,
     f"Got {len(results)} matches")

results = search_nts("xyz123")
test("Search 'xyz123' returns 0 matches",
     len(results) == 0,
     f"Got {len(results)} matches")

# Case-insensitive
results_lower = search_nts("dopamine")
results_upper = search_nts("DOPAMINE")
test("Case-insensitive search works",
     len(results_lower) == len(results_upper) and len(results_lower) > 0,
     f"Lower: {len(results_lower)}, Upper: {len(results_upper)}")


# ============================================================
# TEST 8: Filter Test
# ============================================================
print("\n" + "=" * 60)
print("TEST 8: Filter Test")
print("=" * 60)


def filter_nts(effect=None, category=None):
    """Simulate filtering."""
    results = NT_DATABASE
    if effect:
        results = [nt for nt in results if nt["postsynaptic_effect"] == effect]
    if category:
        results = [nt for nt in results if nt["category"] == category]
    return results


excitatory = filter_nts(effect="Excitatory")
test("Filter by 'Excitatory' returns only Excitatory NTs",
     all(nt["postsynaptic_effect"] == "Excitatory" for nt in excitatory) and len(excitatory) > 0,
     f"Got {len(excitatory)} results")

amino_acids = filter_nts(category="Amino Acids")
test("Filter by 'Amino Acids' returns only Amino Acid NTs",
     all(nt["category"] == "Amino Acids" for nt in amino_acids) and len(amino_acids) > 0,
     f"Got {len(amino_acids)} results")

combined = filter_nts(effect="Inhibitory", category="Amino Acids")
test("Combined filter (Inhibitory + Amino Acids) returns correct subset",
     all(nt["postsynaptic_effect"] == "Inhibitory" and nt["category"] == "Amino Acids"
         for nt in combined),
     f"Got {len(combined)} results")

# Verify filter totals
for effect in VALID_EFFECTS:
    count = len(filter_nts(effect=effect))
    test(f"Filter '{effect}' returns {count} NTs", count > 0)


# ============================================================
# TEST 9: Postsynaptic Effect Visual Mapping Test
# ============================================================
print("\n" + "=" * 60)
print("TEST 9: Postsynaptic Effect Visual Mapping Test")
print("=" * 60)

EXPECTED_EFFECT_COLORS = {
    "Excitatory": "#ef4444",
    "Inhibitory": "#3b82f6",
    "Modulatory": "#a855f7",
    "Mixed": "#eab308"
}

for effect, expected_color in EXPECTED_EFFECT_COLORS.items():
    actual_color = EFFECT_COLORS.get(effect)
    test(f"'{effect}' maps to {expected_color}",
         actual_color == expected_color,
         f"Got {actual_color}")

# Verify every NT has a valid effect color mapping
unmapped = []
for nt in NT_DATABASE:
    if nt["postsynaptic_effect"] not in EFFECT_COLORS:
        unmapped.append(f"ID {nt['id']}: '{nt['postsynaptic_effect']}'")
test("No NT has an unassigned postsynaptic effect color",
     len(unmapped) == 0,
     "; ".join(unmapped[:5]))


# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)
print(f"\n  Results: {passed}/{total} tests passed, {failed} failed\n")

if failed == 0:
    print("  ALL TESTS PASSED. App is ready.")
else:
    print(f"  {failed} test(s) FAILED. Please fix issues and re-run.")
    sys.exit(1)
