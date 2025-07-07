from flask import Blueprint, render_template, request, redirect, url_for, current_app, Response, flash, session
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from database.models import db, Image
from app.utils_rules import extract_features, rule_based_prediction
from app.charts import generate_annotation_pie_chart, generate_file_size_boxplot, generate_cumulative_curve
import csv
from flask_babel import _

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'Aucune image envoyée', 400
    file = request.files['image']
    if file.filename == '':
        return 'Nom de fichier vide', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{timestamp}_{filename}"
        saved_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        file.save(saved_path)

        features = extract_features(saved_path)
        predicted_label = rule_based_prediction(features)

        new_image = Image(
            filename=new_filename,
            date_uploaded=datetime.now(),
            annotation=None,
            annotation_auto=predicted_label,
            width=features['width'],
            height=features['height'],
            file_size_kb=features['file_size_kb'],
            avg_red=features['avg_red'],
            avg_green=features['avg_green'],
            avg_blue=features['avg_blue']
        )

        db.session.add(new_image)
        db.session.commit()

        return redirect(url_for('main.annotate', filename=new_filename))
    return 'Format de fichier non autorisé', 400

@main.route('/annotate/<filename>', methods=['GET'])
def annotate(filename):
    image = Image.query.filter_by(filename=filename).first()
    return render_template('annotate.html', image=image)

@main.route('/annotate/<filename>/annotation', methods=['POST'])
def save_annotation(filename):
    image = Image.query.filter_by(filename=filename).first()
    if not image:
        return 'Image non trouvée', 404

    label = request.form.get('label')
    lat = request.form.get('latitude')
    lon = request.form.get('longitude')

    if not label or label not in ['pleine', 'vide']:
        flash("Veuillez sélectionner une annotation (pleine ou vide).", "danger")
        return redirect(url_for('main.annotate', filename=filename))

    try:
        latitude = float(lat)
        longitude = float(lon)
    except (ValueError, TypeError):
        flash("Veuillez entrer des coordonnées valides (latitude/longitude).", "danger")
        return redirect(url_for('main.annotate', filename=filename))

    image.annotation = label
    image.latitude = latitude
    image.longitude = longitude
    db.session.commit()

    flash("Annotation et coordonnées enregistrées avec succès.", "success")
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
def dashboard():
    filter_value = request.args.get('filter')
    min_size = request.args.get('min_size', type=int)
    min_date_str = request.args.get('min_date')
    min_date = None
    if min_date_str:
        try:
            min_date = datetime.strptime(min_date_str, "%Y-%m-%d")
        except ValueError:
            pass
    query = Image.query
    if filter_value in ['pleine', 'vide']:
        query = query.filter_by(annotation=filter_value)
    if min_size is not None:
        query = query.filter(Image.file_size_kb >= min_size)
    if min_date is not None:
        query = query.filter(Image.date_uploaded >= min_date)
    images = query.all()

    total = len(images)
    pleines = Image.query.filter_by(annotation='pleine').count()
    vides = Image.query.filter_by(annotation='vide').count()

    chart_pie = generate_annotation_pie_chart()
    chart_size = generate_file_size_boxplot()
    chart_cumulative = generate_cumulative_curve()

    # Histogram bins computation
    from collections import Counter
    import math

    bins = Counter()
    for img in images:
        if img.file_size_kb is not None:
            bin_index = int(math.floor(img.file_size_kb / 100))
            bins[bin_index * 100] += 1

    size_labels = [f"{k}-{k+100} KB" for k in sorted(bins.keys())]
    size_counts = [bins[k] for k in sorted(bins.keys())]

    # Courbe cumulative
    from collections import defaultdict

    date_counts = defaultdict(int)
    for img in images:
        if img.date_uploaded:
            date_str = img.date_uploaded.strftime("%Y-%m-%d")
            date_counts[date_str] += 1

    sorted_dates = sorted(date_counts.keys())
    cumulative_labels = []
    cumulative_counts = []
    total_so_far = 0
    for date in sorted_dates:
        total_so_far += date_counts[date]
        cumulative_labels.append(date)
        cumulative_counts.append(total_so_far)

    # Ajouter une propriété temporaire mean_color à chaque image
    for img in images:
        if img.avg_red is not None and img.avg_green is not None and img.avg_blue is not None:
            img.mean_color = round((img.avg_red + img.avg_green + img.avg_blue) / 3, 2)
        else:
            img.mean_color = None

    # Histogramme par jour de la semaine
    weekday_names = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    weekday_counts_map = Counter()

    for img in images:
        if img.date_uploaded:
            weekday_index = img.date_uploaded.weekday()  # 0 = lundi, 6 = dimanche
            weekday_counts_map[weekday_index] += 1

    weekday_labels = weekday_names
    weekday_counts = [weekday_counts_map.get(i, 0) for i in range(7)]

    return render_template(
        'dashboard.html',
        images=images,
        total=total,
        pleines=pleines,
        vides=vides,
        selected_filter=filter_value,
        selected_min_size=min_size,
        selected_min_date=min_date_str,
        chart_pie=chart_pie,
        chart_size=chart_size,
        chart_cumulative=chart_cumulative,
        size_labels=size_labels,
        size_counts=size_counts,
        cumulative_labels=cumulative_labels,
        cumulative_counts=cumulative_counts,
        weekday_labels=weekday_labels,
        weekday_counts=weekday_counts
    )

@main.route('/set_language/<lang_code>')
def set_language(lang_code):
    if lang_code in ['en', 'fr']:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('main.index'))


@main.route('/download')
def download_csv():
    images = Image.query.all()

    def generate():
        data = [
            ['filename', 'date_uploaded', 'annotation', 'annotation_auto', 'width', 'height', 'file_size_kb', 'avg_red', 'avg_green', 'avg_blue', 'latitude', 'longitude']
        ]
        for img in images:
            data.append([
                img.filename,
                img.date_uploaded.strftime('%Y-%m-%d %H:%M:%S'),
                img.annotation or '',
                img.annotation_auto or '',
                img.width,
                img.height,
                f"{img.file_size_kb:.2f}",
                f"{img.avg_red:.2f}",
                f"{img.avg_green:.2f}",
                f"{img.avg_blue:.2f}",
                img.latitude if img.latitude is not None else '',
                img.longitude if img.longitude is not None else ''
            ])
        for row in data:
            yield ','.join(map(str, row)) + '\n'

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=images.csv"})

from flask import request, session, redirect, url_for

@main.route('/set_language')
def set_language_query():
    lang = request.args.get('lang')
    if lang:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))