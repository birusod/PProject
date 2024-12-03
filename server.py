from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)  # => a flask app


@app.route('/')  # home page
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # check for empty strings or only spaces
    if not bool(city.strip()):
        city = 'Seattle'

    wd = get_current_weather(city)

    # City not found by  API
    if not wd['cod'] == 200:
        # return "City  not found"
        return render_template('city_not_found.html')

    return render_template(
        'weather.html',
        title=wd['name'],
        status=wd['weather'][0]['description'].capitalize(),
        temp=f"{wd['main']['temp']:.1f}",
        feels_like=f"{wd['main']['feels_like']:.1f}"
    )


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)
