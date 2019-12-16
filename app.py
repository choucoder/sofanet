from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from database.connection import *
from database.models import *
from model import *
import numpy as np
import datetime

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
	if 'username' in session:
		session['patient'] = 0
		return render_template('index.html', name = session['username'])
	else:
		return render_template('login.html')

@app.route('/get_session_patient', methods=['GET', 'POST'])
def get_session_patient():
	return jsonify({"patient": session['patient']})

@app.route('/login', methods=["POST", "GET"])
def login():

	if request.method == 'GET':
		if 'username' in session:
			return redirect(url_for('index'))
		else:
			return render_template('login.html')

	elif request.method == 'POST':
		error = None
		conex = default_connection()
		cedula = request.form['cedula']
		password = request.form['password']
		medico = Medico.get_medico(cedula=cedula)

		if medico == None:
			error = "Medico no se encuentra registrado en el sistema"
			print(error)
			return render_template('login.html', error=error)
		else:
			if medico.validar_password(password):
				session['username'] = medico.primer_nombre + " " + medico.primer_apellido
				session['cedula'] = cedula
				return redirect(url_for('index'))
			else:
				error = "La contraseña ingresada es incorrecta"
				print(error)
				return render_template('login.html', error = error)

		print("Cedula: {}".format(cedula))
		print("Password: {}".format(password))

@app.route('/register', methods=["GET", "POST"])
def register():
	if 'username' in session:
		return redirect(url_for('index'))
	else:

		if request.method == "GET":
			return render_template('register.html')
		
		elif request.method == "POST":
			
			error = None
			conex = default_connection()

			cedula = request.form["cedula"]
			numero_ss = request.form["numero_ss"]
			primer_nombre = request.form["primer_nombre"]
			primer_apellido = request.form["primer_apellido"]
			fecha = request.form["fecha_nacimiento"]
			list_date = fecha.split('/')
			fecha_nacimiento = datetime.datetime(int(list_date[2]), int(list_date[1]), int(list_date[0]))
			sexo = request.form["sexo"]
			direccion = request.form["direccion"]
			password = request.form["password"]
			confirm_password = request.form["confirm_password"]

			if Medico.get_medico(cedula=cedula) == None:

				if cedula and numero_ss and primer_apellido and primer_nombre and fecha_nacimiento and sexo and direccion and password and confirm_password:

					if password == confirm_password:

						medico = Medico(cedula=cedula, numero_ss=numero_ss)
						medico.primer_nombre = primer_nombre
						medico.primer_apellido = primer_apellido
						medico.fecha_nacimiento = fecha_nacimiento
						medico.sexo = sexo
						medico.direccion_residencia = direccion
						medico.password = password
						medico.save()

						return render_template('login.html')
					else:
						
						error = "Las contraseñas no coinciden"
						return render_template('register.html')
				else:
					error = "Falto algun campo por llenar"
					return render_template('register.html')

			else:
				error = "Usuario ya se encuentra registrado inicie session"
				return render_template('login.html')


@app.route('/logout', methods=["GET", "POST"])
def logout():
	# Remover el username de la sesion si existe
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/sesion_paciente', methods=['GET', 'POST'])
def sesion_paciente():
	if 'username' in session:
		if 'patient' in session:
			default_connection();
			ci = session['patient']

			p = Paciente.get_paciente(ci)

			if p:
				nom = p.primer_nombre
				apell = p.primer_apellido
				sexo = p.sexo
				dire = p.direccion_residencia
				return jsonify({"isalive": 1, "ci": ci, "nom": nom, 
				"apell": apell, "sexo": sexo, "dir": dire})
		else:
			return jsonify({"isalive": 0})
	return redirect(url_for('login'))

@app.route('/consultar_paciente', methods=["GET", "POST"])
def consultar_paciente():
	print("Consulta")
	if 'username' in session:

		conex = default_connection()
		cedula = request.args.get('cedula', 0, type=str)

		p = Paciente.get_paciente(cedula)
		if p == None:
			print("No existe")
			return jsonify({"cedula": cedula, "existe": 0})
		else:
			session['patient'] = p.cedula
			data = {"existe": 1, "cedula": p.cedula, "nombre": p.primer_nombre, "apellido": p.primer_apellido, "edad": 20, "sexo": p.sexo, "direccion": p.direccion_residencia}
			return jsonify(data)

	return redirect(url_for('login'))

@app.route('/registrar_paciente', methods=["GET", "POST"])
def registrar_paciente():

	if 'username' in session:

		conex = default_connection()

		cedula = request.args.get('cedula', 0, type=str)
		primer_nombre = request.args.get('primer_nombre', 0, type=str)
		segundo_nombre = request.args.get('segundo_nombre', 0, type=str)
		primer_apellido = request.args.get('primer_apellido', 0, type=str)
		segundo_apellido = request.args.get('segundo_apellido', 0, type=str)
		fecha = request.args.get('fecha_nacimiento', 0, type=str)
		fecha = fecha.split('/')
		fecha_nacimiento = datetime.datetime(int(fecha[2]), int(fecha[1]), int(fecha[0]))
		direccion = request.args.get('direccion', 0, type=str)
		sexo = request.args.get('sexo', 0, type=str)
		telefono = request.args.get('telefono', 0, type=str)

		if cedula and primer_nombre and primer_apellido and fecha and direccion and sexo and telefono:

			p = Paciente.get_paciente(cedula)

			if p == None:
				paciente = Paciente(cedula=cedula, primer_nombre=primer_nombre)
				paciente.segundo_nombre = segundo_nombre
				paciente.primer_apellido = primer_apellido
				paciente.segundo_apellido = segundo_apellido
				paciente.fecha_nacimiento = fecha_nacimiento
				paciente.direccion_residencia = direccion
				paciente.sexo = sexo
				paciente.telefono = telefono
				paciente.edad = edad(fecha_nacimiento)
				paciente.save()
				print("Cedula {} Guardada".format(cedula))

				return jsonify({"existe": 0, "campos_vacios": 0})

			else:
				return jsonify({"existe": 1, "campos_vacios": 0})

		else:
			return jsonify({"existe": 2, "campos_vacios": 1})

	return redirect(url_for('login'))

# Ruta que contiene el formulario de la
# anamnesis que se le realiza al paciente
# para ver si esta en riesgo de padecer 
# diabete mellitus
@app.route('/pre-diagnosis', methods=['GET', 'POST'])
def preDiagnosis():
	if 'username' not in session:
		return redirect(url_for('login'))

	return render_template('pre-diagnosis.html')

@app.route('/save_prediagnosis', methods=['GET', 'POST'])
def save_prediagnosis():
	if 'username' in session:
		if 'patient' in session:
			cedula = session['patient']
			FORMAS = ['buena', 'regular', 'mala']
			HORARIO = ['bueno', 'regular', 'malo']
			padres_diab = request.args.get('padres_dia', 0, type=str)
			abuelos_diab = request.args.get('abuelos_dia', 0, type=str)
			murio_diab = request.args.get('murio_dia', 0, type=str)
			sedentarismo = request.args.get('sedentarism', type=float)
			alcohol = request.args.get('alcoho', 0, type=float)
			cafe = request.args.get('caf', 0, type=float)
			drogas = request.args.get('droga', 0, type=float)
			formas_alim = request.args.get('formas_ali', 0, type=int)
			horario_alim = request.args.get('horario_ali', 0, type=int)

			if str(sedentarismo) == "" or str(alcohol) == "" or str(cafe) == "" or str(drogas) == "" or str(horario_alim) == "" or str(formas_alim) == "":
				return jsonify({"error": "Faltan datos por llenar"})

			default_connection()	

			paciente = Paciente.get_paciente(cedula)
			print("Result: {}".format(PreDiagnosis.patient_havePreDiagnosis(paciente)))

			if PreDiagnosis.patient_havePreDiagnosis(paciente):
				return jsonify({"nerror": 1, "error": "Al paciente con CI "+cedula+" ya se le hizo preDiagnostico"})

			if padres_diab == 'true':
				padres_diab = 1
			elif padres_diab == 'false':
				padres_diab = 0

			if abuelos_diab == 'true':
				abuelos_diab = 1
			elif abuelos_diab == 'false':
				abuelos_diab = 0

			if murio_diab == 'true':
				murio_diab = 1
			else:
				murio_diab = 0

			f_a = 0
			h_a = 0
			if formas_alim == 0 or formas_alim == 1:
				f_a = formas_alim*0.15
			else:
				f_a = 0.15

			if horario_alim == 0 or horario_alim == 1:
				h_a = horario_alim*0.15
			else:
				h_a = 0.15

			medico = Medico.get_medico(session['cedula'])
			preD = PreDiagnosis(paciente=paciente, medico=medico)
			preD.fecha_registro = datetime.datetime.now()
			preD.padres_diabeticos = padres_diab
			preD.abuelos_diabeticos = abuelos_diab
			preD.murio_diabetico = murio_diab
			preD.sedentarismo = sedentarismo
			preD.alcohol = alcohol
			preD.drogas = drogas
			preD.cafe = cafe
			preD.horario_alimentacion = HORARIO[horario_alim]
			preD.forma_alimentacion = FORMAS[formas_alim]
			preD.funcion_pedegree = ((padres_diab*0.2) + (abuelos_diab*0.2) + (murio_diab*0.3))*1000
			preD.resultado = ((sedentarismo*0.3) + (alcohol*0.2) + (cafe*0.1) + (drogas*0.1) + (f_a) + (h_a))

			print("Funcion Pedegree: {}".format(preD.funcion_pedegree))
			print("Resultados: {}".format(preD.resultado))

			resp = "Paciente no tiene indicios de padecer diabetes."

			if preD.resultado > 0.7:
				resp = "Paciente tiene un " + str(preD.resultado) + "%"
				resp += " de padecer diabetes."

			if preD.funcion_pedegree > (0.4*1000):
				if preD.resultado > 0.7:
					resp += "Ademas, posee altos antecedentes familiares"
					resp += "de diabetes"
				else:
					resp = "Paciente posee altos antecedentes familiares"
					resp += "de diabetes. "

			if preD.resultado > 0.7 or preD.funcion_pedegree > (0.4*1000):
				resp += " Debe realizar un diagnostico"

			porc = ((preD.funcion_pedegree / 1000.0) * 0.5) + (preD.resultado * 0.5)

			preD.save()
			print("V1: {}".format(preD.resultado))
			print("V2: {}".format(100 - preD.resultado))
			return jsonify({"fp": preD.funcion_pedegree, "v1":porc, "v2": (1 - porc), "nerror": 0})

		else:
			return jsonify({"error": "Debe Ingresar un paciente"})

	return redirect(url_for('login'))


# Ruta que contiene el formulario de entrada
# de los resultados de examenes que con los
# cuales se puede predecir si el paciente es
# diabetico o no. (AQUI USO LAS REDES NEURONALES)
@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
	if 'username' not in session:
		return redirect(url_for('login'))

	return render_template('diagnosis.html')

@app.route('/save_diagnosis', methods=['GET', 'POST'])
def save_diagnosis():
	if 'username' in session:
		if 'patient' in session:
			cedula = session['patient']
			glucosa = request.args.get('glucosa', 0, type=float)
			presion = request.args.get('presion', 0, type=float)
			insulin = request.args.get('insulina', 0, type=float)
			masa = request.args.get('masacor', 0, type=float)
			estatura = request.args.get('estatura', 0, type=float)

			html = ""

			if str(glucosa) == "" and str(presion) == "" and str(insulin) == "" and str(masa) == "" and estatura == "":
				return jsonify({"diagnosis": predict, "error": "Faltan datos"})

			default_connection()
			paciente = Paciente.get_paciente(cedula)

			if Diagnosis.patient_haveDiagnosis(paciente):
				return jsonify({"error": "Al paciente con CI " +cedula+" ya se le hizo diagnostico"})

			if not PreDiagnosis.patient_havePreDiagnosis(paciente):
				return jsonify({"error": "El paciente tiene que pasar primer por un pre-diagnostico"})	

			medico = Medico.get_medico(session['cedula'])
			diag = Diagnosis(paciente=paciente, medico=medico)
			
			# Etapa de clasificación con los datos de entrada
			funcion_pedegree = PreDiagnosis.get_preDiagnosisPatient(paciente).funcion_pedegree
			BMI = (masa / (estatura ** 2))

			html += "<ul class='list'>"
			html += "<li>Glucosa: "+str(glucosa)+"</li>"
			html += "<li>Presión: "+str(presion)+"</li>"
			html += "<li>Insulina: "+str(insulin)+"</li>"
			html += "<li>Indice de masa corporal: "+str(BMI)+"</li>"
			html += "<li>Edad: "+str(paciente.edad)+"</li>"
			html += "</ul>"

			vector = []
			vector.append(glucosa)
			vector.append(presion)
			vector.append(insulin)
			vector.append(BMI)
			vector.append(funcion_pedegree)
			vector.append(paciente.edad)

			vector = np.array(vector)
			vector.reshape((1, 6))

			es_diabetico = -1
			prediction, r1, r2, arg_max = predict(vector)

			print("prediction: {}".format(prediction))
			print("r1: {}".format(r1))
			print("r2: {}".format(r2))
			print("arg_max: {}".format(arg_max))

			diag.fecha_diagnosis = datetime.datetime.now()
			diag.glucosa = glucosa
			diag.presion = presion
			diag.insulina = insulin
			diag.masa = masa
			diag.prediction_net = prediction
			diag.estatura = estatura
			diag.es_diabetico = arg_max

			d = MonitoringDiagnosis(paciente=paciente, medico=medico)
			d.fecha = datetime.datetime.now()
			d.glucosa = glucosa
			d.presion = presion
			d.insulina = insulin
			d.masa = masa
			d.estatura = estatura
			d.prediction_net = prediction
			d.esta_controlado = d.prediction_net
			d.es_diabetico = arg_max
			d.save()

			diag.save()

			return jsonify({"prediction": 1, "error": "", 
				"v1": prediction, "r1": r1, "v2": (1 - prediction), "r2": r2, 
				"html": html}) 

		else:
			jsonify({"save": -1, "error": "Miss a Patient"})
	
	return redirect(url_for('login'))

# Actualizar atributo es_diabetico
@app.route('/es_diabetico', methods=['GET', 'POST'])
def es_diabetico():
	if 'username' in session:
		if 'patient' in session:
			cedula = session['patient']
			paciente = Paciente.get_paciente(cedula)

			diag = Diagnosis.get_DiagnosisPatient(paciente)
			mDiag = MonitoringDiagnosis.objects.get(paciente=paciente)

			diag.es_diabetico = int(not diag.es_diabetico)
			mDiag.es_diabetico = int(not mDiag.es_diabetico)

			diag.save()
			mDiag.save()

			return jsonify({"error": "success"})

		return redirect(url_for('login'))	

	return redirect(url_for('login'))
# Ruta que contiene el formulario de seguimiento
# que se le hace tanto a los pacientes que pa-
# decen diabetes como de los que solo se les 
# hizo el pre-diagnostico de la diabetes
@app.route('/monitoring', methods=['GET', 'POST'])
def monitoring():
	if 'username' not in session:
		return redirect(url_for('login'))

	return render_template('monitoring.html')


@app.route('/monitoring_d', methods=['GET', 'POST'])
def monitoring_d():
	if 'username' not in session:
		return redirect(url_for('login'))

	return render_template('monitoring_d.html')

@app.route('/view_monitoring', methods=['GET', 'POST'])
def view_monitoring():
	if 'username' not in session:
		return redirect(url_for('login'))

	return render_template('view_monitoring.html')

# Vistas de los seguimientos
@app.route('/monitoring_view', methods=['GET', 'POST'])
def monitoring_view():
	if 'username' not in session:
		return redirect(url_for('login'))

	return render_template('monitoring_view.html')

@app.route('/monitoring_view_d', methods=['GET', 'POST'])
def monitoring_view_d():
	if 'username' not in session:
		return redirect(url_for('login'))

	return render_template('monitoring_view_d.html')

@app.route('/monitoring_view_pre', methods=['GET', 'POST'])
def monitoring_view_pre():
	if'username' not in session:
		return redirect(url_for('login'))

	return render_template('monitoring_view_pre.html')

@app.route('/monitoring_view_d_show', methods=['GET', 'POST'])
def monitoring_view_d_show():
	if 'username' not in session:
		return redirect(url_for('login'))

	default_connection()
	cedula = session['patient']
	paciente = Paciente.get_paciente(cedula)
	obj = MonitoringDiagnosis.get_monitoringDiagnosisPatient(paciente)

	html = ""
	if obj == None:
		return jsonify({"html": html})

	for m in obj:
		html += "<tr>"
		html += "<td>"+m.medico.primer_nombre+"</td>"
		html += "<td>"+str(m.fecha)[:-7]+"</td>"
		html += "<td>"+str(m.glucosa)+"</td>"
		html += "<td>"+str(m.presion)+"</td>"
		html += "<td>"+str(m.insulina)+"</td>"
		html += "<td>"+str(m.masa)+"</td>"
		html += "<td>"+str(m.prediction_net)+"</td>"
		html += "<td>"+str(m.esta_controlado)+"</td>"
		html += "</tr>"

	return jsonify({"html": html})

@app.route('/monitoring_view_pre_show', methods=['GET', 'POST'])
def monitoring_view_pre_show():
	if'username' not in session:
		return redirect(url_for('login'))

	default_connection()
	cedula = session['patient']
	paciente = Paciente.get_paciente(cedula)
	obj = MonitoringPreDiagnosis.get_monitoringPreDiagnosisPatient(paciente)

	html = ""
	if obj == None:
		return jsonify({"html": html})

	for pre in obj:
		html += "<tr>"
		html += "<td>"+pre.medico.primer_nombre+"</td>"
		html += "<td>"+str(pre.fecha)[:-7]+"</td>"
		html += "<td>"+str(pre.sedentarismo)+"</td>"
		html += "<td>"+str(pre.alcohol)+"</td>"
		html += "<td>"+str(pre.drogas)+"</td>"
		html += "<td>"+str(pre.cafe)+"</td>"
		html += "<td>"+str(pre.hora_alimentacion)+"</td>"
		html += "<td>"+str(pre.forma_alimentacion)+"</td>"
		html += "<td>"+str(pre.resultado)+"</td>"
		html += "</tr>"

	return jsonify({"html": html}) 

@app.route('/monitoring_pre', methods=['GET', 'POST'])
def monitoring_pre():
	if 'username' not in session:
		return redirect(url_for('login'))

	return render_template('monitoring_pre.html')

@app.route('/save_monitoring_d', methods=['GET', 'POST'])
def save_monitoring_d():
	if 'username' in session:
		if 'patient' in session:
			cedula = session['patient']
			glucosa = request.args.get('glucosa', 0, type=float)
			presion = request.args.get('presion', 0, type=float)
			insulin = request.args.get('insulina', 0, type=float)
			masa = request.args.get('masa', 0, type=float)
			estatura = request.args.get('estatura', 0, type=float)
			predict = 0.5
			print("Monitoring diagnosis")

			if str(glucosa) == "" and str(presion) == "" and str(insulin) == "" and str(masa) == "":
				return jsonify({"error": "Error, debes llenar todo el formulario"})

			default_connection()

			paciente = Paciente.get_paciente(cedula)
			medico = Medico.get_medico(session['cedula'])

			if not Diagnosis.patient_haveDiagnosis(paciente):
				return jsonify({"error": "Al Paciente no se le ha realizado un diagnostico para hacerle seguimiento"})

			d = MonitoringDiagnosis(paciente=paciente, medico=medico)
			d.fecha = datetime.datetime.now()
			d.glucosa = glucosa
			d.presion = presion
			d.insulina = insulin
			d.estatura = estatura
			d.masa = masa
			d.prediction_net = 1
			d.esta_controlado = d.prediction_net
			d.save()

			lg, lp, li, lbmi, ld, lm, ly, fecha = getListFromMonitoring(4, paciente)

			return jsonify({"error": "Esta Mejorando? 1", "lg": lg,
				"lp": lp, "li": li, "lbmi": lbmi, "ld": ld, "lm": lm, "ly": ly,
				"fecha": fecha})

		else:
			jsonify({"save": -1, "error": "Miss a Patient"})
	
	return redirect(url_for('login'))

@app.route('/save_monitoring_pre', methods=['GET', 'POST'])
def save_monitoring_pre():
	if 'username' in session:
		if 'patient' in session:
			cedula = session['patient']
			sedentarismo = request.args.get('sedentarism', type=int)
			alcohol = request.args.get('alcoho', 0, type=int)
			cafe = request.args.get('caf', 0, type=int)
			drogas = request.args.get('droga', 0, type=int)
			formas_alim = request.args.get('formas_ali', 0, type=int)
			horario_alim = request.args.get('horario_ali', 0, type=int)
			FORMAS = ['buena', 'regular', 'mala']
			HORARIO = ['bueno', 'regular', 'malo']

			if sedentarismo == "" or alcohol == "" or cafe == "" or drogas == "" or formas_alim == "" or horario_alim == "":
				return jsonify({"error": "Debe Llenar todo el formulario"})

			default_connection()

			paciente = Paciente.get_paciente(cedula)
			medico = Medico.get_medico(session['cedula'])
			
			if not PreDiagnosis.patient_havePreDiagnosis(paciente):
				return jsonify({"error": "Debe hacerle un prediagnostico para poder realizar seguimiento"})

			print("Monitoring preDiagnosis")
			f_a = 0
			h_a = 0
			if formas_alim == 0 or formas_alim == 1:
				f_a = formas_alim*0.15
			else:
				f_a = 0.15

			if horario_alim == 0 or horario_alim == 1:
				h_a = horario_alim*0.15
			else:
				h_a = 0.15

			mPre = MonitoringPreDiagnosis(paciente=paciente, medico=medico)
			mPre.fecha = datetime.datetime.now()
			mPre.sedentarismo = sedentarismo
			mPre.alcohol = alcohol
			mPre.drogas = drogas
			mPre.cafe = cafe
			mPre.hora_alimentacion = HORARIO[horario_alim]
			mPre.forma_alimentacion = FORMAS[formas_alim]
			mPre.resultado = ((sedentarismo*0.3) + (alcohol*0.2) + (cafe*0.1) + (drogas*0.1) + (f_a) + (h_a))

			resp = ""
			try:
				ant_mPre = MonitoringPreDiagnosis.objects(paciente=paciente).order_by('-id').limit(1)[0]
				if ant_mPre.resultado > mPre.resultado:
					resp = "Paciente ha estando mejorando!"
				else:
					resp = "Paciente no esta siguiendo las recomendaciones médicas puestas"
			except Exception as e:
				ant_pre = PreDiagnosis.objects.get(paciente=paciente)
				if ant_pre.resultado > mPre.resultado:
					resp = "Paciente ha estado siguiendo las recomendaciones médicas"
				else:
					resp = "Paciente no esta siguiendo las recomendaciones médicas"
			mPre.save()

			return jsonify({"error": resp, "r1": mPre.resultado, 
				"r2": (1 - mPre.resultado)})

		else:	
			return jsonify({"error": "Debe Ingresar un paciente"})

	return redirect(url_for('login'))			


def getListFromMonitoring(num, pac):
	default_connection()

	# Obtener ultimos num seguimientos
	md = MonitoringDiagnosis.objects(paciente=pac).order_by('-id').limit(num)

	# Transformar en lista para luego
	# hacer reverse a esta
	lmd = list(md)
	lmd.reverse()

	# Crear listas a devolver (Glucosa,
	# Presion, Insulina, BMI, fecha)
	lg = []
	lp = []
	li = []
	lbmi = []
	ld = []
	lm = []
	ly = []
	lfecha = []

	for _md in lmd:
		lg.append(_md.glucosa)
		lp.append(_md.presion)
		li.append(_md.insulina)
		lbmi.append(_md.masa / (_md.estatura ** 2))
		ld.append(_md.fecha.day)
		lm.append(_md.fecha.month)
		ly.append(_md.fecha.year)
		fecha = str(_md.fecha.day) + "/" + str(_md.fecha.month) + "/" + str(_md.fecha.year)
		lfecha.append(fecha)

	return lg, lp, li, lbmi, ld, lm, ly, lfecha







