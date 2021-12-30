from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


from api.frontend import create_app as frontend
from api.upload import create_app as upload
from api.send import create_app as send
from api.clean import create_app as clean

frontend = frontend()
upload = upload()
send = send()
clean = clean()


application = DispatcherMiddleware(
    frontend, {
    '/upload': upload,
	'/send': send,
	'/clean': clean,
})

if __name__ == "__main__":
	run_simple(
        hostname='localhost',
        port=5000,
        application=application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True)