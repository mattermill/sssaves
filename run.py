from sssaves_app import app
import sass

if __name__ == '__main__':
	sass.compile(dirname=('sssaves_app/static/sass', 'sssaves_app/static/css'), source_comments=True)
	app.run(debug=True)