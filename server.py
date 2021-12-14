import json
from flask_cors import CORS, cross_origin
from store.coordinate_store import retrieve_latest_point
from flask import Flask, request
from overlay_generator.create_overlay import generate as generate_overlay
from conductor.of_movement import move_to_point
from conductor.of_sound import play_pitch
from conductor.of_paint import fire

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

overlay = generate_overlay()

@app.route('/play')
def play():
    pitch = int(request.args.get('pitch'))
    duration = float(request.args.get('duration'))
    # frame = retrieve_latest_frame()
    # current_point = track_image_in(frame)
    current_point = retrieve_latest_point()
    destination_point = overlay.get_random_point_for_pitch(pitch)
    move_to_point(destination_point, current_point, overlay)
    play_pitch(pitch, duration)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/fire_paint')
@cross_origin()
def fire_paint():
  fire()
  return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=3232)
