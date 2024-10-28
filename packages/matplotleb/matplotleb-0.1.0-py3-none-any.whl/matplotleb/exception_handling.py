def get_marks(course_num):
    while True:
        try:
            internal = float(input(f"Enter internal marks for course {course_num}: "))
            if internal < 0:
                raise ValueError("Internal marks must be positive or zero.")
            external = float(input(f"Enter external marks for course {course_num}: "))
            if external < 0:
                raise ValueError("External marks must be positive or zero.")
            return internal, external
        except ValueError as e:
            print(e)

def check_pass(internal, external, total_course_marks):
    if internal >= 13 and external >= 38 and total_course_marks >= 50:
        return "Passed"
    else:
        return "Failed"

def calculate_grade(average):
    if average >= 90:
        return "O"
    elif 80 <= average < 90:
        return "A+"
    elif 70 <= average < 80:
        return "A"
    elif 60 <= average < 70:
        return "B+"
    elif 50 <= average < 60:
        return "B"
    else:
        return "Fail"

def main():
    total_internal = 0
    total_external = 0
    total_marks = 0
    for i in range(5):
        internal, external = get_marks(i + 1)
        total_course_marks = internal + external
        total_internal += internal
        total_external += external
        total_marks += total_course_marks

        # Check pass or fail for each course
        result = check_pass(internal, external, total_course_marks)
        print(f"Course {i+1}: {result}")
    # Calculate the average
    average = total_marks / 5
    print(f"\nTotal marks: {total_marks}")
    print(f"Average marks: {average}")

    # Determine and print the grade
    grade = calculate_grade(average)
    print(f"Grade: {grade}")

# Call the main function to run the program
main()
