from local_spotlights import db, create_app
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
quit()
