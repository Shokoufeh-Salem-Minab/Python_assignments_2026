# Task 1: Procedural programming
# here i only use normal functions, loops and if statements.
# every student is just a dictionary and i pass it into the functions.


# the dataset from the homework
students = [
    {"name": "Anna",  "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John",  "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]


def check_students(data):
    # small safety check so the programs stop with a clear message
    # if the data is broken (empty list, missing key, score out of range)
    if len(data) == 0:
        raise ValueError("the student list is empty")

    for s in data:
        for key in ["name", "exam1", "exam2", "exam3", "homework"]:
            if key not in s:
                raise ValueError(f"student {s} is missing the key '{key}'")

        for key in ["exam1", "exam2", "exam3", "homework"]:
            value = s[key]
            # bool is also a number in python so i block it separately
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{s['name']}: {key} must be a number")

        for key in ["exam1", "exam2", "exam3"]:
            if s[key] < 0 or s[key] > 100:
                raise ValueError(f"{s['name']}: {key} must be between 0 and 100")

        # homework is how many of the 10 assignments were submitted
        if s["homework"] < 0 or s["homework"] > 10:
            raise ValueError(f"{s['name']}: homework must be between 0 and 10")


def exam_average(student):
    # average of the 3 exams
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3


def homework_score(student):
    # submitted / 10 * 100
    return student["homework"] / 10 * 100


def final_score(student):
    # 70% exams + 30% homework
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)


def get_status(final):
    # pass mark is 60, exactly 60 is still a pass
    if final >= 60:
        return "Pass"
    return "Fail"


def is_excellent(student):
    # all three exams need to be 90 or more
    if student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90:
        return True
    return False


def recovery_score(final):
    # +5 points but it can never go over 100
    # (this only changes the score, not pass/fail)
    new_score = final + 5
    if new_score > 100:
        new_score = 100
    return new_score


def class_average(finals):
    # add everything up in a loop, then divide
    if len(finals) == 0:
        return 0  # nobody in the class, so no division by zero
    total = 0
    for f in finals:
        total = total + f
    return total / len(finals)


def rank_students(results):
    # sorts from highest to lowest final score using loops (insertion sort)
    # if two students have the same score, the one who was first stays first
    ranked = []
    for r in results:
        position = len(ranked)
        # go back while the student before has a lower score
        while position > 0 and ranked[position - 1]["final"] < r["final"]:
            position = position - 1
        ranked.insert(position, r)
    return ranked


def main():
    check_students(students)

    results = []
    for s in students:
        final = final_score(s)

        result = {
            "name": s["name"],
            "exam_avg": exam_average(s),
            "homework": homework_score(s),
            "final": final,
            "status": get_status(final),
            "excellent": is_excellent(s),
            "recovery": None,
        }

        # recovery only for people under 60, and their status stays Fail
        if final < 60:
            result["recovery"] = recovery_score(final)

        results.append(result)

    print("--- Procedural ---")
    for r in results:
        line = f"{r['name']:6} final={r['final']:.2f} status={r['status']}"
        if r["excellent"]:
            line += " | Excellent Performance"
        if r["recovery"] is not None:
            line += f" | recovery={r['recovery']:.2f}"
        print(line)

    finals = []
    for r in results:
        finals.append(r["final"])
    print(f"\nClass average: {class_average(finals):.2f}")

    print("\nRanking:")
    place = 1
    for r in rank_students(results):
        print(f"{place}. {r['name']} ({r['final']:.2f})")
        place += 1


if __name__ == "__main__":
    main()
