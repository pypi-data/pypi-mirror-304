from humanize_number import humanize_number

def init_app(app):
    """
    Initialize the application with humanize_number as a Jinja2 filter
    """

    app.jinja_env.filters['humanize_number'] = humanize_number