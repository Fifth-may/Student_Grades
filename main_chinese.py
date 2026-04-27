import sqlite3

# --- 第一段：全局常量 ---
DB_NAME = "student_grades.db"


# --- 第二段：数据库逻辑 ---
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
    print("数据库初始化成功！")

def db_add_student(name):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            #--检测学生有没有在档案里--
            cursor.execute("SELECT name FROM Students WHERE name = (?)",(name,))
            if not cursor.fetchone():
                #--------输入学生--------
                cursor.execute("INSERT INTO Students (name) VALUES (?)", (name,))
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
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
        print(f"数据库错误: {e}")
        return False

def db_add_grade(grade):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Students (score) VALUES (?)", (grade,))
            return True
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        return False

def db_add_student_grade(name,title,score):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            #查找学生
            cursor.execute("SELECT student_id FROM Students WHERE name = ?",(name,))
            student = cursor.fetchone()
            if not student:
                print(f"没找到学生：{name}")
                return False
            s_id = student[0]
            #查找考试
            cursor.execute("SELECT subjects_id FROM Subjects WHERE title = ?",(title,))
            test = cursor.fetchone()
            if not test:
                print(f"没找到科目：{title}")
                return False
            sub_id = test[0]
            #成绩是否合格
            query = """
                SELECT Subjects.max_score
                FROM Subjects
                WHERE title = (?)
            """
            cursor.execute(query,(title,))
            test_score = cursor.fetchone()
            if score <= int(test_score[0]):
                #输入成绩
                cursor.execute("INSERT INTO Grades (student_id,subjects_id,score) VALUES (?,?,?)", (s_id,sub_id,score,))
                conn.commit()
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
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
        print(f"查询失败: {e}")
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
        print(f"查询失败: {e}")
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
        print(f"查询失败: {e}")
        return []

def db_delete_student():
    student = input("请输入要删除的学生: ")
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Students WHERE Students.name = (?)",(student,))
            return True
    except sqlite3.Error as e:
        print(f"查询失败: {e}")
        return False

def db_delete_subject():
    subjects = input("请输入要删除的考试: ")
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Subjects WHERE Subjects.title = (?)",(subjects,))
            return True
    except sqlite3.Error as e:
        print(f"查询失败: {e}")
        return False

def db_view_student_reports():
    student = input("请输入学生姓名: ")
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
        print(f"查询失败: {e}")
        return False

# 3. 验证输入值


def verify_name():
    name = input("请输入学生姓名 按回车取消: ").strip()
    try:
        name = int(name)
        print("姓名不能为数字")
        return verify_name()
    except ValueError:
        return name

def verify_score():
    score = int(input("请输入考试最高分数: ").strip())
    try:
        score = int(score)
        return score
    except ValueError:
        print("分数只能为数字")
        return verify_score()

def verify_grade():
    grade = int(input("请输入考试分数: ").strip())
    try:
        grade = int(grade)
        return grade
    except ValueError:
        print("分数只能为数字")
        return verify_grade()
def verify_score_name(name,title):
    with sqlite3.connect(DB_NAME) as conn:
        #姓名
        cursor = conn.cursor()
        cursor.execute("SELECT Students.name FROM Students WHERE name = ? ",(name,))
        student = cursor.fetchone()
        
        if not student:
            print(f"没找到学生：{name}")
            return False
        
        #考试
        # continue on the if statement for the tests title 4/22 1:33a.m.
        cursor.execute("SELECT Subjects.title FROM Subjects WHERE title = ?",(title,))
        score = cursor.fetchone()
        

        #没有录入记录
        if not score:
            print(f"没找到科目：{title}")
            return False
        

        return True

        
# --- 第三段：UI 逻辑 ---
def ui_add_student():
    print("\n--- 添加新学生 ---")
    name = verify_name()
    if name:
        if db_add_student(name):
            print(f"成功：学生 '{name}' 已添加！")
        else:
            print(f"数据库里已有学生：{name}")
    else:
        print("取消成功")

def ui_add_subject():
    print("\n--- 添加新考试 ---")
    subjects = input("请输入考试名字 按回车取消: ").strip()
    if subjects:
        score = verify_score()
        if score:
            if db_add_subject(subjects,score):
                print(f"谢谢，考试{subjects}: 满分{score} 已添加")
            else:
                print(f"数据库里已有考试：{subjects}")
    else:
        print("取消成功")
def ui_add_student_grade():
    print("\n--- 添加新考试成绩 ---")
    name = input("请输入学生名字 按回车取消: ").strip()
    if name:
        title = input("请输入考试名字 按回车取消: ").strip()
        title_used = verify_score_name(name,title)#检测考试名字和学生有没有已录入档案
        if title_used:
            score = verify_grade()
            if db_add_student_grade(name,title,score):
                print(f"成功：已录入 {name} 的 {title} 成绩为 {score}分")
            else:
                print("考试分数不能超过考试最高分数")

def ui_view_reports():
    print("\n=== 学生成绩总报表 ===")
    results = db_get_all_reports()
    
    if not results:
        print("目前没有任何成绩记录。")
        return

    # 打印表头
    print(f"{'姓名':<10} | {'考试':<10} | {'分数':<6} | {'满分':<6} | {'百分比'}")
    print("-" * 60)

    for name, title, score, max_score in results:
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        print(f"{name+(11-len(name))* ' '} | {title+(11-len(title))*' '} | {score}{(8-len(str(score)))*' '} | {max_score}{(8-len(str(max_score)))*' '} | {percentage:.1f}%")

def ui_view_student_report():
    print("\n=== 学生成绩报表 ===")
    results = db_view_student_reports()

    if not results:
        print("目前没有任何成绩记录。")
        return
    
    print(f"{'姓名':<10} | {'考试':<10} | {'分数':<6} | {'满分':<6} | {'百分比'}")
    print("-" * 60)

    for name, title, score, max_score in results:
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        print(f"{name+(11-len(name))* ' '} | {title+(11-len(title))*' '} | {score}{(8-len(str(score)))*' '} | {max_score}{(8-len(str(max_score)))*' '} | {percentage:.1f}%")




def ui_view_students():
    print("\n=== 学生统计 ===")
    results = db_view_students()
    if not results:
        print("目前没有任何成绩记录。")
        return
    print("   == 姓名 ==")
    for name in results:
        print(f"      {name[0]}")
    

def ui_view_subjects():
    print("\n=== 考试统计 ===")
    results = db_view_subjects()
    if not results:
        print("目前没有任何成绩记录。")
        return
    print("   == 考试 ==")
    for title in results:
        print(f"      {title[0]}")

def ui_delete_student():
    print("\n=== 删除学生 ===")
    if db_delete_student():
        print("删除成功")

def ui_delete_subject():
    print("\n=== 删除考试 ===")
    if db_delete_subject():
        print("删除成功")
# --- 第四段：主程序入口 ---
def main():

    init_db()  
    while True:
        print("\n=== 学生成绩系统菜单 ===")
        print("1. 添加学生 | 2. 录入考试成绩 | 3.添加考试 | 4. 查看报表 | 5.查看学生成绩 | 6. 查看已有的学生 | 7.查看已有的考试 | 8.删除学生 | 9.删除考试 | 10. 退出")
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