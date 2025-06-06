alt-store-backend/
├── app.py
├── config.py
├── requirements.txt
├── .env
├── instance/
│   └── config.py  (for instance-specific, sensitive configs)
├── models/
│   ├── __init__.py
│   └── user.py
│   └── product.py
│   └── ... (other models)
├── resources/
│   ├── __init__.py
│   ├── auth.py
│   ├── users.py
│   ├── products.py
│   └── ... (other API resources)
├── services/
│   ├── __init__.py
│   └── user_service.py
│   └── product_service.py
│   └── ... (other service logic)
├── auth/
│   ├── __init__.py
│   └── decorators.py (for @login_required, etc.)
│   └── auth_manager.py (logic for JWT, sessions, etc.)
├── utils/
│   ├── __init__.py
│   └── helpers.py
│   └── constants.py
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── ... (migration scripts)
└── tests/
    ├── __init__.py
    ├── test_auth.py
    ├── test_users.py
    └── ...

Phase 1: Project Setup & Core Application

    [ ] Create Project Directory:
        mkdir your_project_name
        cd your_project_name
    [ ] Set up Virtual Environment:
        python -m venv venv
        Activate it: (source venv/bin/activate or venv\Scripts\activate)
    [ ] Create Core Files and Directories:
        app.py, config.py, requirements.txt, .env
        models/, resources/, services/, auth/, utils/, instance/
        Add __init__.py to each new directory.
    [ ] Install Core Libraries:
        pip install Flask Flask-SQLAlchemy Flask-JWT-Extended python-dotenv Werkzeug
        pip freeze > requirements.txt
    [ ] Configure .gitignore:
        Create a .gitignore file and add: venv/, .env, __pycache__/, *.pyc, instance/
    [ ] Basic Configuration (config.py):
        Define Config, DevelopmentConfig, TestingConfig, ProductionConfig classes.
        Include placeholder SECRET_KEY, JWT_SECRET_KEY, SQLALCHEMY_DATABASE_URI.
    [ ] Initialize Flask App (app.py):
        Set up create_app() function.
        Initialize db = SQLAlchemy() and jwt = JWTManager().
        Configure the app using app.config.from_object() and app.config.from_pyfile().
        Add if __name__ == '__main__': app = create_app(); app.run(debug=True).
    [ ] Setup .env:
        Add SECRET_KEY, JWT_SECRET_KEY, DEV_DATABASE_URL (e.g., sqlite:///dev.db).


Phase 2: Database Model & User Authentication

    [ ] User Model (models/user.py):
        Define User model with id, username, email, password_hash.
        Implement set_password() and check_password_hash().
        Add a to_dict() method.
    [ ] Auth Manager (auth/auth_manager.py):
        Create this file (can be empty initially, or add basic JWT handling).
    [ ] Auth Decorators (auth/decorators.py):
        Create this file. For now, you can just import jwt_required from flask_jwt_extended directly in resources, or define custom ones here later.
    [ ] User Service (services/user_service.py):
        Implement create_user() logic (hashing password, adding to DB).
        Implement get_user_by_username() and get_user_by_id().
        Add basic validation (e.g., check for duplicate usernames/emails).
    [ ] Auth Resources (resources/auth.py):
        Create auth_bp Blueprint.
        Define Register and Login Resource classes (using flask_restful.Api is recommended).
        Implement post() methods to call UserService for user creation and authentication.
        Add a Refresh endpoint if using refresh tokens.
    [ ] Register Auth Blueprint (app.py):
        Import auth_bp and app.register_blueprint(auth_bp, url_prefix='/api/auth').

Phase 3: Initial Database Setup & Testing Authentication

    [ ] Create Database Tables:
        Activate virtual environment.
        export FLASK_APP=app.py (or set FLASK_APP=app.py on Windows)
        flask shell
        Inside shell:
        Python

    from app import create_app, db
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created!")
    exit()

[ ] Test Registration & Login:

    Run your Flask app.
    Use Postman, Insomnia, or curl to:
        POST /api/auth/register (send username, email, password).
        POST /api/auth/login (send username, password) and verify you receive tokens.

Phase 4: Core API Logic (Example: Products)

    [ ] Product Model (models/product.py):
        Define Product model (name, description, price, stock, etc.).
        Add a to_dict() method.
    [ ] Product Service (services/product_service.py):
        Implement methods like create_product(), get_all_products(), get_product_by_id(), update_product(), delete_product().
        Include any relevant business validation.
    [ ] Product Resources (resources/products.py):
        Create products_bp Blueprint.
        Define ProductListResource (for GET/POST /api/products).
        Define ProductResource (for GET/PUT/DELETE /api/products/<int:product_id>).
        Apply @jwt_required() where necessary.
        Call the appropriate ProductService methods.
    [ ] Register Product Blueprint (app.py):
        Import products_bp and app.register_blueprint(products_bp, url_prefix='/api').
    [ ] Test Product Endpoints:
        Restart your Flask app.
        Use your API client to test product creation, retrieval, update, and deletion, ensuring to include the JWT access token in the Authorization: Bearer <token> header for protected routes.

Phase 5: Utilities & Testing

    [ ] Utility Functions (utils/helpers.py, utils/constants.py):
        Add any common helper functions or global constants as needed.
    [ ] Write Tests (tests/ folder):
        pip install pytest
        Create tests/ directory with __init__.py.
        Create test files (e.g., test_auth.py, test_products.py).
        Write unit tests for your services/ logic.
        Write integration tests for your resources/ endpoints.
        Ensure TestingConfig in config.py uses an in-memory database.
        Run tests: pytest