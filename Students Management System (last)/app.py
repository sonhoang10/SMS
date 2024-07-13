from tinydb import TinyDB, Query
from flask import Flask, render_template, request, jsonify #jsonify là hàm để chuyển đổi dữ liệu sang JSON (Java Script Object Notation là 1 loại dữ liệu để truyền hay xử lí dữ liệu trong sever)

db = TinyDB("student_db.json") #Dùng Tiny Database để lưu trữ trong file sudent_db.json
app = Flask(__name__) #Dùng Flask để mở sever

@app.route("/",methods=["GET"])
def home():
    students = db.all() #Lấy tất cả dữ liệu từ file student_db.json 
    return render_template('Home.html',students=students,) #và đưa vào file home.html (sử dụng Jinja2 để lấy)

@app.route("/add.html", methods=["GET","POST"]) #Get: dùng request.get_json để lấy dữ liệu từ file add.html (JS object)
                                                #Post: để xử lí dữ liệu và insert vào file student_db.json
def add():
    current_stt = len(db.all())
    current_stt+=1
    if request.method == "POST":
        data = request.get_json() #Khi này, data sẽ get dữ liệu đã thêm vào(Tên, Lớp, Mã số)
        name = data.get("Name")
        grade = data.get("Grade")
        student_id = data.get("Id")
        db.insert({"STT":current_stt,"Tên": name, "Lớp": grade, "Id": student_id}) #Thêm thông tin học sinh lưu vào DB
        return jsonify({'result': 'success'})
    return render_template('add.html') #Trả về trang add.html


@app.route("/students/update", methods=["PUT"]) #Lấy dữ liệu từ home.html ra để cập nhật
def update_student():
    data = request.get_json()
    stt = data.get("STT")  # Giữ nguyên giá trị STT
    student_id = data.get("Id")
    new_name = data.get("Tên")
    new_grade = data.get("Lớp")

    Student = Query()
    db.update({"Tên": new_name, "Lớp": new_grade, "Id": student_id}, Student.STT == stt) #update thông tin học viên
    #update(Thông tin muốn cập nhật, đối tượng được chọn để cập nhật)
    return jsonify({'result': 'success'})

@app.route("/students/delete", methods=["DELETE"])  #Lấy dữ liệu từ home.html ra để cập nhật STT và xóa đi học viên
def delete_student():
    data = request.get_json()
    student_stt = data.get("STT")
    
    Student = Query()
    db.remove(Student.STT == student_stt) #xóa đi học sinh
    
    # Cập nhật lại STT cho các học viên còn lại
    students = db.all()
    for student in students: #cho student lặp qua từng đối tượng cho tiny DB để set lại stt
        if student['STT'] > student_stt:
            db.update({'STT': student['STT'] - 1}, Student.STT == student['STT']) 
    return jsonify({'result': 'success'}) # Trả về dữ liệu thành công về file home.html

if __name__ == "__main__": 
    app.run(debug=True)