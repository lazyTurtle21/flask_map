from flask import Flask, render_template, request
from twitter2 import get_url, read_conn, get_info
from Kholod_film_map import get_locations, icon_layer, map_creator

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map', methods=['POST'])
def map():
    text = request.form['account']
    res = main(text)
    if res:
        return render_template('failure.html', name=text)
    return render_template('map.html')


def main(acc):
    url = get_url(acc)
    if not url:
        return "No such Twitter account. Try again"

    js = read_conn(url)
    icons = get_info(js, 'location')
    locations = get_locations(icons)
    map_creator(icon_layer(locations))


if __name__ == '__main__':
    app.run(debug=True)
