import json

DATA_FILE = "gradebook.json"


class InvalidGradeError(ValueError):
	pass


class UnknownStudentError(LookupError):
	pass


class Student:
	def __init__(self, student_id, name, grades=None):
		self.student_id = student_id
		self.name = name
		self.grades = grades or {}

	@property
	def passing_grade(self):
		return 10

	def average(self):
		return sum(self.grades.values()) / len(self.grades) if self.grades else 0

	def best_course(self):
		return max(self.grades.items(), key=lambda item: item[1]) if self.grades else None

	def __str__(self):
		return f"{self.student_id}: {self.name} (average: {self.average():.2f})"


class GraduateStudent(Student):
	def __init__(self, student_id, name, thesis_title, grades=None):
		super().__init__(student_id, name, grades)
		self.thesis_title = thesis_title

	@property
	def passing_grade(self):
		return 14

	def __str__(self):
		return f"{super().__str__()} [Graduate; thesis: {self.thesis_title}]"


class Gradebook:
	def __init__(self):
		self.students = {}

	def __len__(self):
		return len(self.students)

	def add_student(self, student):
		if student.student_id in self.students:
			raise ValueError("Student IDs must be unique.")
		self.students[student.student_id] = student

	def get_student(self, student_id):
		try:
			return self.students[student_id]
		except KeyError as error:
			raise UnknownStudentError(f"Unknown student ID: {student_id}") from error

	def add_grade(self, student_id, course, grade):
		student = self.get_student(student_id)
		if not 0 <= grade <= 20:
			raise InvalidGradeError("Grades must be between 0 and 20.")
		student.grades[course] = grade

	def offered_courses(self):
		return {course for student in self.students.values() for course in student.grades}

	def ranking(self):
		return sorted(self.students.values(), key=lambda student: student.average(), reverse=True)

	def failing_students(self):
		return [student for student in self.students.values()
				if any(grade < student.passing_grade for grade in student.grades.values())]

	def save(self):
		records = []
		for student in self.students.values():
			records.append({
				"id": student.student_id,
				"name": student.name,
				"grades": student.grades,
				"graduate": isinstance(student, GraduateStudent),
				"thesis_title": getattr(student, "thesis_title", ""),
			})
		with open(DATA_FILE, "w", encoding="utf-8") as file:
			json.dump(records, file, indent=2)

	@classmethod
	def load(cls):
		book = cls()
		try:
			with open(DATA_FILE, "r", encoding="utf-8") as file:
				records = json.load(file)
			for record in records:
				grades = record.get("grades", {})
				if record.get("graduate"):
					student = GraduateStudent(record["id"], record["name"],
											   record.get("thesis_title", ""), grades)
				else:
					student = Student(record["id"], record["name"], grades)
				book.add_student(student)
		except FileNotFoundError:
			pass
		except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
			print(f"Could not load gradebook: {error}")
		return book


def add_student(book):
	student_id = input("Student ID: ").strip()
	name = input("Name: ").strip()
	kind = input("Type (regular/graduate): ").strip().lower()
	if kind in ("graduate", "g"):
		student = GraduateStudent(student_id, name, input("Thesis title: ").strip())
	elif kind in ("regular", "r"):
		student = Student(student_id, name)
	else:
		print("Choose regular or graduate.")
		return
	try:
		book.add_student(student)
		print("Student added.")
	except ValueError as error:
		print(error)


def add_grade(book):
	student_id = input("Student ID: ").strip()
	try:
		book.get_student(student_id)
		course = input("Course: ").strip()
		grade = float(input("Grade (0-20): "))
		book.add_grade(student_id, course, grade)
		print("Grade saved.")
	except UnknownStudentError as error:
		print(error)
	except ValueError as error:
		print(f"Invalid grade: {error}")


def show_students(book):
	if not len(book):
		print("No students.")
		return
	for student in book.students.values():
		print(student)
		best = student.best_course()
		if best:
			course, grade = best
			print(f"  Best course: {course} ({grade:g})")
		else:
			print("  No grades yet.")


def show_common_courses(book):
	try:
		first = book.get_student(input("First student ID: ").strip())
		second = book.get_student(input("Second student ID: ").strip())
		common = set(first.grades) & set(second.grades)
		print("Common courses: " + (", ".join(sorted(common)) if common else "none"))
	except UnknownStudentError as error:
		print(error)


def main():
	book = Gradebook.load()
	while True:
		print("\n1. Add student (regular or graduate)")
		print("2. Add or update a grade")
		print("3. Show all students")
		print("4. Show ranking")
		print("5. Show failing students")
		print("6. Show common courses of two students")
		print("7. Save and exit")
		choice = input("Choose an option: ").strip()
		try:
			if choice == "1":
				add_student(book)
			elif choice == "2":
				add_grade(book)
			elif choice == "3":
				show_students(book)
			elif choice == "4":
				for rank, student in enumerate(book.ranking(), 1):
					print(f"{rank}. {student.name} — {student.average():.2f}")
			elif choice == "5":
				failing = book.failing_students()
				if not failing:
					print("No failing students.")
				for student in failing:
					print(f"{student} (passing grade: {student.passing_grade})")
			elif choice == "6":
				show_common_courses(book)
			elif choice == "7":
				book.save()
				print("Saved. Goodbye.")
				break
			else:
				print("Enter a number from 1 to 7.")
		except (OSError, ValueError) as error:
			print(f"Invalid input or operation: {error}")


if __name__ == "__main__":
	main()
