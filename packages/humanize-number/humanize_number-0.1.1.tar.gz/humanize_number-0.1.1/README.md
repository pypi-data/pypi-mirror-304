# humanize_number
A package to humanize numbers into readable formats like 1K, 1M

    pip install humanize_number

>

    from humanize_number import humanize_number

>

    humanize_number(579000)
    >>> 579k

### flask-extension

    from flask import Flask
    from humanize_number.humanize_flask import init_app

    app = Flask(__name__)
    init_app(app)

    # index.html
    # {{ number | humanize_number }}

