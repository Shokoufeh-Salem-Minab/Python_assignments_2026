from functools import reduce

students = [
    {"name":"Anna","exam1":85,"exam2":90,"exam3":88,"homework":9},
    {"name":"Peter","exam1":55,"exam2":60,"exam3":58,"homework":6},
    {"name":"Maria","exam1":95,"exam2":92,"exam3":98,"homework":10},
    {"name":"John","exam1":70,"exam2":65,"exam3":72,"homework":8},
    {"name":"Sofia","exam1":40,"exam2":50,"exam3":45,"homework":5},
    {"name":"David","exam1":88,"exam2":91,"exam3":86,"homework":10}
]

def calculate(s):
    avg = (s["exam1"] + s["exam2"] + s["exam3"]) / 3
    hw = s["homework"] / 10 * 100
    final = avg * 0.7 + hw * 0.3
    return {"name":s["name"], "final":final,
            "status":"Pass" if final >= 60 else "Fail",
            "excellent":s["exam1"] >= 90 and s["exam2"] >= 90 and s["exam3"] >= 90,
            "recovery":min(final + 5, 100) if final < 60 else final}

# map creates new result dictionaries; the original list is unchanged.
results = list(map(calculate, students))
passed = list(filter(lambda s: s["status"] == "Pass", results))
excellent = list(filter(lambda s: s["excellent"], results))
total = reduce(lambda a, s: a + s["final"], results, 0)
ranking = sorted(results, key=lambda s: s["final"], reverse=True)

for s in results:
    print(s["name"], round(s["final"],2), s["status"], "Recovery:", round(s["recovery"],2))
print("Passed:", [s["name"] for s in passed])
print("Excellent:", [s["name"] for s in excellent])
print("Class average:", round(total / len(results),2))
print("Ranking:", [s["name"] for s in ranking])
