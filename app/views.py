from flask import Blueprint, render_template, request, redirect, url_for
import services

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/<uuid>", methods=["GET", "POST"])
def student(uuid):
    if request.method == "POST":
        services.delete_student(uuid)
        return redirect(url_for("student.student_all"))
    student = services.serialize_student(uuid)
    pcolumns = services.serialize_student_columns()
    tests = services.serialize_test_all(uuid)
    tcolumns = services.serialize_test_columns()
    return render_template(
        "student/student.html", 
        pcolumns=pcolumns,
        student=student,
        tcolumns=tcolumns,
        tests=tests
    )
    
@student_bp.route("/<uuid>/edit", methods=["GET", "POST"])
def student_edit(uuid):
    if request.method == "POST":
        services.update_student(uuid, request.form)
        return redirect(url_for("student.student", uuid=uuid))
    columns = services.serialize_student_columns()
    student = services.serialize_student(uuid)
    options = services.serialize_student_options()
    return render_template(
        "student/student_edit.html",
        columns=columns,
        student=student,
        options=options,
    )
    
@student_bp.route("/", methods=["GET"])
def student_all():
    students = services.serialize_student_all()
    columns = services.serialize_student_columns()
    return render_template(
        "student/student_all.html", 
        students=students,
        columns=columns
    )

@student_bp.route("/add", methods=["GET", "POST"])
def student_add():
    if request.method == "POST":
        services.create_student(request.form)
        return redirect(url_for("student.student_all"))
    columns = services.serialize_student_columns(exclude=["outid"])
    options = services.serialize_student_options()
    return render_template(
        "student/student_add.html",
        columns=columns,
        options=options,
    )

    
test_bp = Blueprint("test", __name__, url_prefix="/test")
@test_bp.route("/<student_uuid>/<id>", methods=["GET", "POST"])
def test(student_uuid, id):
    if request.method == "POST":
        services.delete_test(id)
        return redirect(url_for("student.student", uuid=student_uuid))
    test = services.serialize_test(id)
    columns = services.serialize_test_columns()
    return render_template(
        "test/test.html", 
        columns=columns,
        test=test
    )

@test_bp.route("/add/<student_uuid>", methods=["GET", "POST"])
def test_add(student_uuid):
    if request.method == "POST":
        services.create_test(student_uuid, request.form)
        return redirect(url_for("student.student", uuid=student_uuid))
    columns = services.serialize_test_columns(exclude=["id"])
    student = services.serialize_student(student_uuid)
    options = services.serialize_test_options()
    return render_template(
        "test/test_add.html",
        columns=columns,
        student=student,
        options=options,
    )

@test_bp.route("/edit/<student_uuid>/<id>", methods=["GET", "POST"])
def test_edit(student_uuid, id):
    if request.method == "POST":
        services.update_test(id, request.form)
        return redirect(url_for("student.student", uuid=student_uuid))
    columns = services.serialize_test_columns()
    test = services.serialize_test(id)
    options = services.serialize_test_options()
    return render_template(
        "test/test_edit.html",
        columns=columns,
        test=test,
        options=options,
    )

query_bp = Blueprint("query", __name__, url_prefix="/query")
@query_bp.route("/", methods=["GET", "POST"])
def query():
    if request.method == "POST":
        query_result = services.query(request.form)
        return  render_template(
            "query/query_result.html",
            query_result=query_result   
        )
    options = services.serialize_test_options()
    return render_template(
        "query/query.html",
        options=options
    )