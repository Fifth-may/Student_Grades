import sqlite3

# --- first part：global variable ---
DB_NAME = "student_grades.db"


# --- second part：database logic ---
def init_db():

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Subjects (
                subjects_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                max_score INTEGER DEFAULT 99999
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                subjects_id INTEGER,
                score INTEGER,
                FOREIGN KEY (student_id) REFERENCES Students(student_id),
                FOREIGN KEY (subjects_id) REFERENCES Subjects(subjects_id)
            )
        """)
        conn.commit()
    print("database initialazation sucessful！")

def db_add_student(name):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            #--detect if the student is in the database or not--
            cursor.execute("SELECT name FROM Students WHERE name = (?)",(name,))
            if not cursor.fetchone():
                #--------insert student--------
                cursor.execute("INSERT INTO Students (name) VALUES (?)", (name,))
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return False


def db_add_subject(sub,max):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM Subjects WHERE title = (?)",(sub,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO Subjects (title,max_score) VALUES (?, ?)", (sub,max))
                return True 
            else:
                return False
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return False

def db_add_grade(grade):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Students (score) VALUES (?)", (grade,))
            return True
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return False

def db_add_student_grade(name,title,score):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            #find student
            cursor.execute("SELECT student_id FROM Students WHERE name = ?",(name,))
            student = cursor.fetchone()
            if not student:
                print(f"did not find student：{name}")
                return False
            s_id = student[0]
            #find tests
            cursor.execute("SELECT subjects_id FROM Subjects WHERE title = ?",(title,))
            test = cursor.fetchone()
            if not test:
                print(f"did not find test：{title}")
                return False
            sub_id = test[0]
            #check if the score is valid
            query = """
                SELECT Subjects.max_score
                FROM Subjects
                WHERE title = (?)
            """
            cursor.execute(query,(title,))
            test_score = cursor.fetchone()
            if score <= int(test_score[0]):
                #insert score
                cursor.execute("INSERT INTO Grades (student_id,subjects_id,score) VALUES (?,?,?)", (s_id,sub_id,score,))
                conn.commit()
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return False
def db_get_all_reports():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            query = """
                SELECT Students.name, Subjects.title, Grades.score, Subjects.max_score
                FROM Grades
                JOIN Students ON Grades.student_id = Students.student_id
                JOIN Subjects ON Grades.subjects_id = Subjects.subjects_id
                ORDER BY Students.name ASC
            """
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return []
def db_view_students():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            query = """
                SELECT Students.name
                FROM Students
                ORDER BY Students.name ASC
            """
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return []
    
def db_view_subjects():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            query = """
                SELECT title
                FROM Subjects
                ORDER BY Subjects.title ASC
            """
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return []

def db_delete_student():
    student = input("please insert the student you want to delete: ")
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Students WHERE Students.name = (?)",(student,))
            return True
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return False

def db_delete_subject():
    subjects = input("please insert the test you want to delete: ")
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Subjects WHERE Subjects.title = (?)",(subjects,))
            return True
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return False

def db_view_student_reports():
    student = input("please insert the students name: ")
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            query = """
                SELECT Students.name, Subjects.title, Grades.score, Subjects.max_score
                FROM Grades
                JOIN Students ON Grades.student_id = Students.student_id
                JOIN Subjects ON Grades.subjects_id = Subjects.subjects_id
                WHERE Students.name = (?);

            """
            cursor.execute(query,(student,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"database error: {e}")
        return False

# 3. 验证输入值


def verify_name():
    name = input("please enter the students name press enter to cancel: ").strip()
    try:
        name = int(name)
        print("name cannot be a number")
        return verify_name()
    except ValueError:
        return name

def verify_score():
    score = int(input("please insert the highest score avaliable in this test: ").strip())
    try:
        score = int(score)
        return score
    except ValueError:
        print("score can only be a number")
        return verify_score()

def verify_grade():
    grade = int(input("please insert the test score: ").strip())
    try:
        grade = int(grade)
        return grade
    except ValueError:
        print("score can only be a number")
        return verify_grade()
def verify_score_name(name,title):
    with sqlite3.connect(DB_NAME) as conn:
        #姓名
        cursor = conn.cursor()
        cursor.execute("SELECT Students.name FROM Students WHERE name = ? ",(name,))
        student = cursor.fetchone()
        
        if not student:
            print(f"did not find student：{name}")
            return False
        
        #考试
        # continue on the if statement for the tests title 4/22 1:33a.m.
        cursor.execute("SELECT Subjects.title FROM Subjects WHERE title = ?",(title,))
        score = cursor.fetchone()
        

        #没有录入记录
        if not score:
            print(f"did not find test：{title}")
            return False
        

        return True

        
# --- 第三段：UI logic ---
def ui_add_student():
    print("\n--- add new student ---")
    name = verify_name()
    if name:
        if db_add_student(name):
            print(f"sucess：student '{name}' has been added！")
        else:
            print(f"database already exists student：{name}")
    else:
        print("sucessfully cancelled")

def ui_add_subject():
    print("\n--- add new test ---")
    subjects = input("pleast insert the tests name press enter to cancel: ").strip()
    if subjects:
        score = verify_score()
        if score:
            if db_add_subject(subjects,score):
                print(f"sucess，test{subjects}: full score: {score} has been added")
            else:
                print(f"database already has test：{subjects}")
    else:
        print("cancelled sucessfully")
def ui_add_student_grade():
    print("\n--- add new test score ---")
    name = input("please insert students name press enter to cancel: ").strip()
    if name:
        title = input("please insert tests name press enter to cancel: ").strip()
        title_used = verify_score_name(name,title)#检测考试名字和学生有没有已录入档案
        if title_used:
            score = verify_grade()
            if db_add_student_grade(name,title,score):
                print(f"sucess：database has sucessfulled inserted student {name}'s {title} score as {score}分")
            else:
                print("test score cannot be higher that the tests highest score")

def ui_view_reports():
    print("\n=== full report of all students grades ===")
    results = db_get_all_reports()
    
    if not results:
        print("there are no records yet in the database。")
        return

    # print report headings
    print(f"{'name':<10} | {'tests':<10} | {'score':<6} | {'full score':<6} | {'percentage'}")
    print("-" * 60)

    for name, title, score, max_score in results:
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        print(f"{name+(11-len(name))* ' '} | {title+(11-len(title))*' '} | {score}{(8-len(str(score)))*' '} | {max_score}{(8-len(str(max_score)))*' '} | {percentage:.1f}%")

def ui_view_student_report():
    print("\n=== view single students grade report ===")
    results = db_view_student_reports()

    if not results:
        print("there are no records of this student yet。")
        return
    
    print(f"{'name':<10} | {'tests':<10} | {'score':<6} | {'full score':<6} | {'percentage'}")
    print("-" * 60)

    for name, title, score, max_score in results:
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        print(f"{name+(11-len(name))* ' '} | {title+(11-len(title))*' '} | {score}{(8-len(str(score)))*' '} | {max_score}{(8-len(str(max_score)))*' '} | {percentage:.1f}%")




def ui_view_students():
    print("\n=== student statistics ===")
    results = db_view_students()
    if not results:
        print("there are no statistics yet。")
        return
    print("   == name ==")
    for name in results:
        print(f"      {name[0]}")
    

def ui_view_subjects():
    print("\n=== test statistics ===")
    results = db_view_subjects()
    if not results:
        print("there are no statistics yet。")
        return
    print("   == tests ==")
    for title in results:
        print(f"      {title[0]}")

def ui_delete_student():
    print("\n=== delete student ===")
    if db_delete_student():
        print("deleted sucessfully")

def ui_delete_subject():
    print("\n=== delete tests ===")
    if db_delete_subject():
        print("deleted sucessfully")
# --- 4th part：main programme ---
def main():

    init_db()  
    while True:
        print("\n=== student grade menu ===")
        print("1. add student | 2. insert test scores | 3.add tests | 4. view all student scores | 5.view single student scores | 6. view students in database | 7.view tests in database | 8.delete student | 9.delete tests| 10. exit")
        choice = input("请选择 (1-10): ").strip()
        
        if choice == '1':
            ui_add_student()
        elif choice == '2':
            ui_add_student_grade()
        elif choice == '3':
            ui_add_subject()
        elif choice == '4':
            ui_view_reports()
        elif choice == '5':
            ui_view_student_report()
        elif choice =='6':
            ui_view_students()
        elif choice == "7":
            ui_view_subjects()
        elif choice == '8':
            ui_delete_student()
        elif choice == '9':
            ui_delete_subject()
        elif choice == '10':
            print("再见！")
            break
        else:
            print("选项不存在，请重新选择")

if __name__ == "__main__":
    main()