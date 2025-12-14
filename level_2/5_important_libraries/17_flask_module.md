# Deep Dive: Flask

Flask is a micro-framework based on Werkzeug (WSGI) and Jinja2 (Templates). It is "micro" because it does not require particular tools or libraries (no native ORM, no form validation).

---

## 1. The Application Context & Request Context

Flask uses **Context Locals** (proxies) for `request`, `g`, `current_app`, and `session`. This is why you can import `request` globally but it remains thread-safe.

*   **Request Context**: Active only during a request. Keeps track of URL arguments, form data.
*   **App Context**: Keeps track of application-level data (db connections, config).

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    # 'request' points to the SPECIFIC request implementation for this thread/coroutine
    return request.args.get('q')
```

---

## 2. Blueprints (Modularity)

For large apps, you cannot put everything in `app.py`. **Blueprints** allow you to organize routes into components/modules.

```python
# auth.py
from flask import Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login(): ...

# main.py
app.register_blueprint(auth_bp, url_prefix='/auth')
```

---

## 3. Signals

Flask supports event hooking via Blinker.
*   `request_started`, `request_finished`, `template_rendered`.
*   Useful for logging, audit trails, or metrics without cluttering view logic.

---

## 4. Extensions Pattern

Since Flask is minimal, you add features via extensions (`Flask-SQLAlchemy`, `Flask-Login`).
Standard Pattern:
1.  Initialize extension (`db = SQLAlchemy()`).
2.  Bind to app (`db.init_app(app)`).
This "Factory Pattern" allows one extension instance to support multiple apps (testing).

---

## 5. WSGI (Web Server Gateway Interface)

Flask is a WSGI app.
`app = Flask(__name__)` is a callable object `app(environ, start_response)`.
In production, you need a WSGI server (Gunicorn, uWSGI) to serve it. **Never** use `app.run()` in production.
