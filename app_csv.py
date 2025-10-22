from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# اسم ملف الإكسيل
EXCEL_FILE = 'results.xlsx'

def get_student_by_civil_id(civil_id):
    # قراءة الملف
    df = pd.read_excel(EXCEL_FILE, dtype={'الرقم المدني': str})

    # البحث عن الطالب حسب الرقم المدني
    df_student = df[df['الرقم المدني'] == civil_id]
    if df_student.empty:
        return None

    student = df_student.iloc[0]

    # المواد
    subjects = ['اللغة العربية (من 100)', 'الرياضيات (من 100)', 'العلوم (من 100)', 'التربية الإسلامية (من 100)', 'الدراسات (من 100)', 'اللغة الإنجليزية (من 100)']

    # جمع الدرجات
    grades = {subject: student[subject] for subject in subjects}
    total = student['المجموع الكلي (من 600)']

    return {
        "name": student['اسم الطالب'],
        "civil_id": student['الرقم المدني'],
        "grades": grades,
        "total": total
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        civil_id = request.form.get('civil_id', '').strip()
        student = get_student_by_civil_id(civil_id)
        if student:
            return render_template('result.html', student=student)
        else:
            error = "الرقم المدني غير موجود"
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)