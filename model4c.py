"""
Model exported as python.
Name : model4c
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing


class Model4c(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_drop_fields', 'countries_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Areas_out', 'areas_out', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_fixgeo', 'countries_fixgeo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_reprojected', 'countries_reprojected', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}

        ################################ 
        # Save vector features to file # --> comando 5
        ################################
        
        #Guardamos como csv 
        
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Calculated_93f68059_6234_4997_bba1_880ed2e5fff4', #layer creada anteriormente
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': '/Users/fernandacortes/Desktop/Herramientas/Clase4/output/areas.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        ################# 
        # Drop field(s) # --> comando 1
        #################
        
        # Cargamos la layer y eliminamos las columas que no vamos a uilizar
        
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'], #columas a eliminar
            'INPUT': '/Users/fernandacortes/Desktop/Herramientas/Clase4/Input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', #directorio para cargar la layer
            'OUTPUT': parameters['Countries_drop_fields'] #nombramos la layer que queremos como output
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_drop_fields'] = outputs['DropFields']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        #################### 
        # Field calculator # --> comando 4
        ####################
        
        alg_params = {
            'FIELD_LENGTH': 10, #result field length
            'FIELD_NAME': 'km2area', #cómo lo vamos a nombrar
            'FIELD_PRECISION': 3, #cantidad de decimales del resultado (3)
            'FIELD_TYPE': 0,  #Float
            'FORMULA': 'area($geometry)/1000000', #área delpolígono dividido 1000000
            'INPUT': 'Fixed_geometries_c3703b5c_704c_4fb5_881d_eb9166c26c45', #layer que utilizamos
            'OUTPUT': parameters['Areas_out'] #nombramos la layer que obtenemos como output
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Areas_out'] = outputs['FieldCalculator']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        ################## 
        # Fix geometries # --> comando 3
        ##################
        
        # Corregimos geometrías 
        
        alg_params = {
            'INPUT': 'Reprojected_6519aa57_ade5_44fa_8b85_2369378b9ff2', #utilizamos la layer creada anteriormente
            'OUTPUT': parameters['Countries_fixgeo'] #nombramos la layer que queremos como output
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_fixgeo'] = outputs['FixGeometries']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        ################### 
        # Reproject layer # --> comando 2
        ###################
        
        # Reproyectamos para que los países tengan el tamaño correcto
        
        alg_params = {
            'INPUT': 'Remaining_fields_0084a4b8_2348_4ffc_a689_b56dd41b6bfb', #utilizamos como input la layer anteriormente creada
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('ESRI:54034'), #indica que la reproyección es "cylindrical equal area"
            'OUTPUT': parameters['Countries_reprojected'] #nombramos la layer que queremos como output
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_reprojected'] = outputs['ReprojectLayer']['OUTPUT']
        return results

    def name(self):
        return 'model4c'

    def displayName(self):
        return 'model4c'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4c()
