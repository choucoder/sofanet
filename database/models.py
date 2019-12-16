# models.py

# Aqui se declaran los modelos que le daran la estructura a nuestra base de datos
# usando la API de abstracción de mongoengine 

import mongoengine as mge

# Modelos

class Medico(mge.Document):

	cedula = mge.StringField(max_length=32, primary_key=True, required=True)
	numero_ss = mge.StringField(max_length=32, unique=True, required=True)
	primer_nombre = mge.StringField(max_length=20, required=True)
	segundo_nombre = mge.StringField(max_length=20)
	primer_apellido = mge.StringField(max_length=20, required=True)
	segundo_apellido = mge.StringField(max_length=20)
	fecha_nacimiento = mge.DateTimeField(required=True)
	sexo = mge.StringField(max_length=10 ,required=True)
	direccion_residencia = mge.StringField(max_length=100, required=True)
	password = mge.StringField(max_length=255, required=True)

	@staticmethod
	def get_medico(cedula):
		try:
			query = Medico.objects.get(cedula=cedula)
			return query
		except Exception as e:
			return None

	def validar_password(self, password):
		return (self.password == password)

class Paciente(mge.Document):

	cedula = mge.StringField(max_length=32, primary_key=True, required=True)
	primer_nombre = mge.StringField(max_length=20, required=True)
	segundo_nombre = mge.StringField(max_length=20)
	primer_apellido = mge.StringField(max_length=20, required=True)
	segundo_apellido = mge.StringField(max_length=20)
	fecha_nacimiento = mge.DateTimeField(required=True)
	edad = mge.IntField(required=True)
	sexo = mge.StringField(max_length=20, required=True)
	direccion_residencia = mge.StringField(max_length=100, required=True)
	telefono = mge.StringField(max_length=12)

	@staticmethod
	def get_paciente(cedula):
		try:
			query = Paciente.objects.get(cedula=cedula)
			return query
		except Exception as e:
			return None

class PreDiagnosis(mge.Document):

	medico = mge.ReferenceField(Medico, required=True)
	paciente = mge.ReferenceField(Paciente, required=True)
	fecha_registro = mge.DateTimeField()
	padres_diabeticos = mge.IntField(min_value=0, max_value=10)
	abuelos_diabeticos = mge.IntField()
	murio_diabeticos = mge.IntField()
	sedentarismo = mge.IntField()
	alcohol = mge.IntField(max_length=10)
	drogas = mge.IntField(max_length=10)
	cafe = mge.IntField(max_length=10)
	horario_alimentacion = mge.StringField(max_length=10)
	forma_alimentacion = mge.StringField(max_length=10)
	funcion_pedegree = mge.FloatField(min_value=0, max_value=100000)
	resultado = mge.FloatField(min_value=0, max_value=10000)

	@staticmethod
	def patient_havePreDiagnosis(paciente):
		print("Comenzando")
		try:
			list_pre = PreDiagnosis.objects()
			for pred in list_pre:
				print(pred.paciente.cedula)
				if pred.paciente.cedula == paciente.cedula:
					return True
			return False

		except Exception as e:
			return False

	@staticmethod
	def get_preDiagnosis(medico, paciente):
		try:
			query = PreDiagnosis.objects.get(medico=medico, paciente=paciente)
			return query
		except Exception as e:
			return None

	@staticmethod
	def get_preDiagnosisPatient(paciente):
		try:
			query = PreDiagnosis.objects.get(paciente=paciente)
			return query
		except Exception as e:
			return None


class Diagnosis(mge.Document):

	medico = mge.ReferenceField(Medico, required=True)
	paciente = mge.ReferenceField(Paciente, required=True, primary_key=True)
	fecha_diagnosis = mge.DateTimeField(required=True)
	glucosa = mge.FloatField(min_value=0, max_value=1000, required=True)
	presion = mge.FloatField(min_value=0, max_value=1000, required=True)
	insulina = mge.FloatField(min_value=0, max_value=1000, required=True)
	estatura = mge.FloatField(min_value=0, max_value=1000, required=True)
	masa = mge.FloatField(min_value=0, max_value=1000, required=True)
	prediction_net = mge.FloatField(min_value=0, max_value=1000000, required=True)
	es_diabetico = mge.IntField(required=True)

	@staticmethod
	def patient_haveDiagnosis(paciente):
		try:
			list_d = Diagnosis.objects()
			for d in list_d:
				if d.paciente.cedula == paciente.cedula:
					return True
			return False

		except Exception as e:
			return False

	@staticmethod
	def get_Diagnosis(medico, paciente):
		try:
			query = Diagnosis.objects.get(medico=medico, paciente=paciente)
			return query
		except Exception as e:
			return None

	@staticmethod
	def get_DiagnosisPatient(paciente):
		try:
			query = Diagnosis.objects.get(paciente=paciente)
			return query
		except Exception as e:
			return None

class MonitoringDiagnosis(mge.Document):

	medico = mge.ReferenceField(Medico, required=True)
	paciente = mge.ReferenceField(Paciente, required=True)
	fecha = mge.DateTimeField(required=True)
	glucosa = mge.FloatField(min_value=0, max_value=1000, required=True)
	presion = mge.FloatField(min_value=0, max_value=1000, required=True)
	insulina = mge.FloatField(min_value=0, max_value=1000, required=True)
	masa = mge.FloatField(min_value=0, max_value=1000, required=True)
	estatura = mge.FloatField(min_value=0, max_value=1000, required=True)
	prediction_net = mge.FloatField(required=True)
	esta_controlado = mge.FloatField(required=True)
	es_diabetico = mge.IntField()

	@staticmethod
	def get_monitoringDiagnosis(medico, paciente):
		try:
			query = MonitoringDiagnosis.objects.get(medico=medico, paciente=paciente)
			return query
		except Exception as e:
			return None

	@staticmethod
	def get_monitoringDiagnosisPatient(paciente):
		try:
			query = MonitoringDiagnosis.objects(paciente=paciente)
			return query
		except Exception as e:
			return None

class MonitoringPreDiagnosis(mge.Document):

	medico = mge.ReferenceField(Medico, required=True)
	paciente = mge.ReferenceField(Paciente, required=True)
	fecha = mge.DateTimeField(required=True)
	sedentarismo = mge.IntField()
	alcohol = mge.IntField()
	drogas = mge.IntField(required=True)
	cafe = mge.IntField(required=True)
	hora_alimentacion = mge.StringField(max_length=20, required=True)
	forma_alimentacion = mge.StringField(max_length=20, required=True)
	resultado = mge.FloatField(min_value=0, max_value=10, required=True)

	@staticmethod
	def get_monitoringPreDiagnosisPatient(paciente):
		try:
			query = MonitoringPreDiagnosis.objects(paciente=paciente)
			return query
		except Exception as e:
			return None

	@staticmethod
	def get_monitoringPreDiagnosis(medico, paciente):
		try:
			query = MonitoringPreDiagnosis.objects.get(medico=medico, paciente=paciente)
			return query
		except Exception as e:
			return None



