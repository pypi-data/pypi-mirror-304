import os, re
from traceback import format_exc as traceback_format_exc

#-----------------------------------------------------------
#-- Class containing data for filling Ecuapass document
#-----------------------------------------------------------
class EcuData:
	temporalDir = None

	empresas = { 
		"BYZA": {
			'id'       : "BYZA",
			"nombre"   : "Grupo BYZA S.A.S.",
			"direccion": "Av. Coral y los Alamos",
			"idTipo"   : "RUC", 
			"idNumero" : "0400201414001",
			"modelCartaportes": "Model_02_Cartaportes_NTA_BYZA",
			"modelManifiestos": "Manifiestos_NTA_BYZA_Template",
			#"modelManifiestos": "Model_Manifiestos_NTA_BYZA_4",
			"modelDeclaraciones": None,
			"MRN": None,
			"MSN": None,
			"permisos" : {"originario":"PO-CO-0033-22", "servicios1": "PO-CO-0033-22"}
		},
		"NTA" : { 
			'id'         : "NTA",
			#"nombre"     : "NUEVO TRANSPORTE DE AMERICA COMPAÑIA LIMITADA", 
			"nombre"     : "TRANSPORTE DE CARGA NACIONAL E INTERNACIONAL ALCOMEXCARGO S.A.",
			#"direccion"  : "ARGENTINA Y JUAN LEON MERA - TULCAN",
			"direccion"  : "CALLE AV. SAN FRANCISCO INT.: REMIGIO CRESPO TORAL REF.",
			"direccion02": "Cll Amazonas Mz C Lote 25B Zona Comercial Aguas Verdes - Aguas Verdes (Perú)",
			"idTipo"     : "RUC", 
			#"idNumero"   : "1791834461001",
			"idNumero"   : "0491523638001",
			"modelCartaportes"  : "Model_Cartaportes_NTA_BYZA",
			"modelManifiestos"  : "Manifiestos_NTA_BYZA_Template",
			"modelDeclaraciones": "Model_Declaraciones_NTA_Single",
			"MSN": "0001",
			"permisos" : {"originario":"C.I.-E.C.-0060-04",
				          "servicios1":"P.P.S.CO015905", "servicios2":"P.P.S.PE000210"}
		},
		"LOGITRANS" : { 
			'id'       : "LOGITRANS",
			"nombre"   : "TRANSPORTES LOGITRANS-ACROS S.A.",
			"direccion": "CALDERON NRO. 63-052 Y URUGUAY",
			"idTipo"   : "RUC", 
			"idNumero" : "0491507748001",
			"modelCartaportes": "Model_Cartaportes_NTA_BYZA",
			"modelManifiestos": "Manifiestos_NTA_BYZA_Template",
			"modelDeclaraciones": "Model_Declaraciones_NTA_Single",
			"MSN": "0001",
			"permisos" : {"originario":"PO-EC-0005-20", "servicios1": "PO-EC-0005-20"}
		},
		"SILOGISTICA": {
			'id'     : "SILOGISTICA",
			"nombre": "PROVIZCAINO S.A.",
			"direccion": "ANTIZ Y 9 DE AGOSTO, CALDERÓN - QUITO",
			"idTipo": "RUC",
			"idNumero": "1791882253001",
			"modelCartaportes": "Model_Cartaportes_Silogistica",
			"modelManifiestos": "Model_Manifiestos_Silogistica",
			"modelDeclaraciones": "Model_Declaraciones_NTA_Single",
			"MSN": "||LOW"
		},
		"SYTSA": {
			'id'     : "SYTSA",
			"nombre" : "TRANSPORTES Y SERVICIOS ASOCIADOS SYTSA CIA. LTDA",
			"direccion": "Panamericana norte, sector El Rosal, Tulcán",
			"idTipo" : "RUC", 
			"idNumero" : "1791770358001",
			"modelCartaportes": "Model_Cartaportes_NTA_SILOG",
			"modelManifiestos": "Model_Manifiestos_NTA",
			"modelDeclaraciones": "Model_Declaraciones_NTA_Single",
			"MSN": None
		},
		"BOTERO": {
			'id'     : "BOTERO",
			"nombre" : "EDUARDO BOTERO SOTO S.A.",
			"direccion": "Carrera 42 No 75-63 Aut. Sur, Itagui (Antioquia)",
			"idTipo" : "NIT", 
			"idNumero" : "890.901.321-5",
			"modelCartaportes": "Model_Cartaportes_Botero",
			"modelManifiestos": "Model_Manifiestos_Botero",
			"modelDeclaraciones": None,
			"MSN": None
		}
	}

	configuracion = {
		"dias_cartaportes_recientes" : 4,
		"numero_documento_inicio" : 2000000,
		"num_zeros" : 5
	}


	def getEmpresaInfo (empresaName):
		return EcuData.empresas [empresaName]

	def getEmpresaId (empresa):
		return EcuData.empresas[empresa]["numeroId"]

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	mainInfo ()
