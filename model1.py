"""
Model exported as python.
Name : model1
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fiz_geo', 'fiz_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

        #################
        # Drop field(s) # --> 6° comando
        #################
        
        # Eliminamos las variables que no utilizamos 
        
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': 'Calculated_47b93bb7_f568_4766_8d98_58c35e96073b',
            'OUTPUT': parameters['Wldsout']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        ################## 
        # Feature filter # --> 4° comando
        ##################
        
        # Nos quedamos con las observaciones de menos de 11 caracteres
        # Eliminamos variables del estilo 'español, méxico' o 'español, españa' y nos quedamos con 'español'
        
        alg_params = {
            'INPUT': 'Calculated_970442e9_7158_4226_b44c_129390bc50af',
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        outputs['FeatureFilter'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_menor_a_11'] = outputs['FeatureFilter']['OUTPUT_menor_a_11']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        ########################## 
        # Field calculator clone # --> 5° comando
        ##########################
        
       # Clonamos NAME_PROP y la llamamos lnm 
       
        alg_params = {
            'FIELD_LENGTH': 10, # Longitud de la variable
            'FIELD_NAME': 'lnm', #Nombre de la variable
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # String
            'FORMULA': '"NAME_PROP"', # Utilizamos NAME_PROP para crear lnm
            'INPUT': 'menor_a_11_83574fee_d116_42f0_83a9_6c3da152a2cf',
            'OUTPUT': parameters['Field_calc']
        }
        outputs['FieldCalculatorClone'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['FieldCalculatorClone']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        ####################### 
        # Corregir geometrías # --> 1° comando
        #######################
        
        # Corregimos geometrías automáticamente
        
        alg_params = {
            'INPUT': '/Users/fernandacortes/Desktop/Herramientas/Clase4/langa/langa.shp',
            'OUTPUT': parameters['Fix_geo']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        ##################################### 
        # Agregar campo que auto-incrementa # --> 2° comando
        #####################################
        
        alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['CorregirGeometras']['OUTPUT'], # Utilizamos como input la layer que creamos anteriormente
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1, # Seleccionamos el valor en el que comienza
            'OUTPUT': parameters['Autoinc_id'] # Nombramos la layer que obtenemos como output
        }
        outputs['AgregarCampoQueAutoincrementa'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['AgregarCampoQueAutoincrementa']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        ######################### 
        # Calculadora de campos # --> 3° comando
        #########################
        
        alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length', # Nombre de la variable
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': 'length(NAME_PROP)', # Calcula length de la variable (NAME_PROP)
            'INPUT': outputs['AgregarCampoQueAutoincrementa']['OUTPUT'],
            'OUTPUT': parameters['Length']
        }
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['CalculadoraDeCampos']['OUTPUT']
        return results

    def name(self):
        return 'model1'

    def displayName(self):
        return 'model1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model1()
