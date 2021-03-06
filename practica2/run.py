from flask import Flask, render_template, request
from PIL import Image
app = Flask(__name__)


def renderizaMandelbrot(x1, y1, x2, y2, ancho, iteraciones, nombreFicheroPNG):
	# drawing area
	xa = x1
	xb = x2
	ya = y1 + 0.000001
	yb = y2
	maxIt = iteraciones
	# image size
	imgx = ancho
	imgy = int(abs (y2 - y1) * ancho / abs(x2 - x1));
	
	image = Image.new("RGB", (imgx, imgy))

	for y in range(imgy):
		zy = y * (yb - ya) / (imgy - 1)  + ya
		for x in range(imgx):
			zx = x * (xb - xa) / (imgx - 1)  + xa
			z = zx + zy * 1j
			c = z
			for i in range(maxIt):
				if abs(z) > 2.0: break 
				z = z * z + c

			if (i >= maxIt):
				image.putpixel((x, y), (0, 0, 0))
			else:
				image.putpixel((x, y), (i % 4 * 64, i % 8 * 32, i % 16 * 16))

	image.save(nombreFicheroPNG, "PNG")
	
# paleta es una lista de 3-tuplas con los valores RGB de cada color de la paleta
def getColorPaleta(paleta, nColoresPaleta, color):
	nuevoColor = color % (nColoresPaleta)
        
	nPuntosControlPaleta = len(paleta)
        
	icolor1 = float(nuevoColor) * float(nPuntosControlPaleta - 1) / float(nColoresPaleta - 1)
        
	# print len(paleta)
	# print int(icolor1)
        
	if (int(icolor1) == len(paleta) - 1):  # Devolvemos el último color
		return paleta[len(paleta) - 1]
        
		porcentajeC2 = icolor1 - int(icolor1)
		porcentajeC1 = 1.0 - porcentajeC2
		icolor1 = int(icolor1)
		icolor2 = icolor1 + 1
        
		nr = int(paleta[icolor1][0] * porcentajeC1 + paleta[icolor2][0] * porcentajeC2)
		ng = int(paleta[icolor1][1] * porcentajeC1 + paleta[icolor2][1] * porcentajeC2)
		nb = int(paleta[icolor1][2] * porcentajeC1 + paleta[icolor2][2] * porcentajeC2)
        
	return (nr, ng, nb)
        
	
# Renderiza un fractal de Mandelbrot de (x1, y1) a (x2, y2) de ancho pixeles, iteraciones máximas y lo guarda en el fichero especificado en nombreFicheroPNG (debe tener extesión .png) y permitiendo especificar una paleta de colores: paleta es una lista de 3-tuplas con los valores RGB de cada color de la paleta

def renderizaMandelbrotBonito(x1, y1, x2, y2, ancho, iteraciones, nombreFicheroPNG, paleta, nColoresPaleta):
	# drawing area
	xa = x1
	xb = x2
	ya = y1 + 0.000001
	yb = y2
	maxIt = iteraciones
	# image size
	imgx = ancho
	imgy = int(abs (y2 - y1) * ancho / abs(x2 - x1));
        
	image = Image.new("RGB", (imgx, imgy))

	for y in range(imgy):
		zy = y * (yb - ya) / (imgy - 1)  + ya
		for x in range(imgx):
			zx = x * (xb - xa) / (imgx - 1)  + xa
			z = zx + zy * 1j
			c = z
			for i in range(maxIt):
				if abs(z) > 2.0: break 
				
				z = z * z + c

			if (i == maxIt - 1):
				image.putpixel((x, y), (0, 0, 0))  # El nucleo del fractal en negro
			else:
				image.putpixel((x, y), getColorPaleta(paleta, nColoresPaleta, i))

	image.save(nombreFicheroPNG, "PNG")

@app.route('/mand', methods=['POST', 'GET'])
def mand():
    x1 = request.args.get('x1', '')
    y1 = request.args.get('y1', '')
    x2 = request.args.get('x2', '')
    y2 = request.args.get('y2', '')
    iter = request.args.get('iter', '')
    renderizaMandelbrot(float(x1), float(y1), float(x2), float(y2), 500,100, 'static/mandeer.png')
    return render_template('mander.html')

@app.route('/')
def hello_world():
    return 'Hello, World! This is the index page'

@app.route('/user/<username>')
def show_user_profile(username):
    return "<head><link rel='stylesheet' type='text/css' href='/static/style.css'></head><body><h1>Hola %s</h1><img src='/static/jeje.jpg'/></body>" % username

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)