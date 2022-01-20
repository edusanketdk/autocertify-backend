from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from frontend import create_app as frontend_create_app
from upload import create_app as upload_create_app
from clean import create_app as clean_create_app
from send import create_app as send_create_app



frontend_app = frontend_create_app()
upload_app = upload_create_app()
clean_app = clean_create_app()
send_app = send_create_app()


application = DispatcherMiddleware(
    frontend_app, {
    '/upload': upload_app,
	'/send': send_app,
	'/clean': clean_app,
})



if __name__ == "__main__":
	run_simple(
        hostname='localhost',
        port=5000,
        application=application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True,
		)