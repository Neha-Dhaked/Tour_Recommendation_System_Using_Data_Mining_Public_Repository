from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename
import os
from utils.monument_identifier import identify_monument, get_similar_places, load_monument_data

identify_bp = Blueprint('identify', __name__)
UPLOAD_FOLDER = 'static/uploads'

@identify_bp.route('/identify', methods=['GET', 'POST'])
def identify():
    if request.method == 'POST':
        image = request.files['image']
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        # Step 1: Identify the place from image using CLIP
        place_name = identify_monument(image_path)

        # Step 2: Load full monument metadata (from CSV)
        monument_data = load_monument_data()
        monument_info = monument_data.get(place_name, {})

        # Step 3: Get similar places with full metadata
        similar_places = get_similar_places(place_name)

        # Step 4: Render the result page with all data
        return render_template("identify_result.html",
                               image_url=image_path,
                               place_name=place_name,
                               monument=monument_info,
                               similar_places=similar_places)

    return render_template("identify_monument.html")
