import os
import uuid
from dotenv import load_dotenv
import math
import crud
from flask import Flask, flash, redirect, render_template, request, url_for, send_from_directory,abort


load_dotenv()
UPLOAD_DIR = os.path.abspath(
    os.getenv("UPLOAD_DIR", "uploads")
)
ALLOWED_EXTENSIONS = {"pdf", "txt", "md", "docx","jpg", "jpeg", "png", "gif"}
app = Flask(__name__)

os.makedirs(UPLOAD_DIR, exist_ok=True)


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")




@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file or file.filename == "":
        flash("Файл не выбран")
        return redirect(url_for("index"))

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        flash(f"Недопустимый формат: {ext or 'без расширения'}")
        return redirect(url_for("index"))

    stored_name = f"{uuid.uuid4().hex}.{ext}"
    original_name = file.filename

    file_path = os.path.join(UPLOAD_DIR, stored_name)

    # Сохраняем файл
    file.save(file_path)

    # Получаем настоящий размер файла
    size_bytes = os.path.getsize(file_path)

    # Записываем информацию в PostgreSQL
    new_file_id = crud.add_file(
        stored_name,
        original_name,
        size_bytes,
        ext
    )

    return redirect(url_for("index"))

#
from flask import request, render_template
import math


@app.route("/documents-list")
def documents_list():
    page = request.args.get("page", 1, type=int)
    page = max(page, 1)

    per_page = 5

    total = crud.count_documents()
    total_pages = max(1, math.ceil(total / per_page))

    page = min(page, total_pages)
    offset = (page - 1) * per_page

    documents = crud.get_documents_page(per_page, offset)

    return render_template(
        "documents_list.html",
        documents=documents,
        page=page,
        total_pages=total_pages,
        total=total
    )

@app.route("/")
def index():
    print(crud.get_files_count())
    return render_template("index.html")




from flask import abort, send_from_directory

@app.route("/documents/<path:name>")
def serve_document(name):
    result = crud.get_file_by_stored_name(name)

    if result is None:
        abort(404)

    return send_from_directory(
        UPLOAD_DIR,
        name,
        as_attachment=True,
        download_name=result[0]
    )


@app.route("/documents/<int:file_id>/delete", methods=["POST"])
def delete_document(file_id):
    result = crud.get_file_by_id(file_id)

    if result is None:
        abort(404)

    stored_name = result["stored_name"]
    file_path = os.path.join(UPLOAD_DIR, stored_name)

    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
    except OSError:
        app.logger.exception("Ошибка удаления файла %s", stored_name)
        abort(500)

    crud.remove_file(file_id)

    flash("Документ удалён")
    return redirect(url_for("documents_list"))

@app.route("/documents/filter", methods=["POST"])
def documents_filter():
    query = request.form.get("query", "").strip()

    documents = crud.get_by_query(query)

    return render_template(
        "documents_list.html",
        documents=documents,
        query=query
    )

@app.route("/documents/<int:file_id>/view")
def view_document(file_id):
    document = crud.get_file_by_id(file_id)

    if document is None:
        abort(404)

    return send_from_directory(
        UPLOAD_DIR,
        document["stored_name"],
        as_attachment=False
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
