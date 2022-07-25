"""
Model exported as python.
Name : Modelo3
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Modelo3(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_fields_3', 'drop_fields_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo_3', 'fix_geo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop2000', 'pop2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Zonal_statistics', 'zonal_statistics', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(8, model_feedback)
        results = {}
        outputs = {}

        ######################## 
        # Estadísticas de zona # --> 3° comando
        ########################
        
        # Calculamos la media por país
        
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Campos_restantes_9e003774_b08e_4502_851c_441f73c464ad',
            'INPUT_RASTER': 'landquality_d932a8e2_d05e_4702_9c72_9d5dd931e64b',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Landq']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Landq'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        ########################################## 
        # Guardar objetos vectoriales en archivo # --> 8° comando
        ##########################################
        
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Estadistica_zonal_49815408_9934_4670_97ec_d691ac312251',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Users/Pc__/Desktop/Herramientas computacionales/Clase 4/Replicar paper/Output/raster_stats.gpkg',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GuardarObjetosVectorialesEnArchivo'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        ####################### 
        # Corregir geometrías # --> 1° comando
        #######################
        
        # Corregimos geometrías automáticamente
        
        alg_params = {
            'INPUT': 'C:/Users/Pc__/Desktop/Herramientas computacionales/Clase 4/Replicar paper/Input/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fix_geo_3']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo_3'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        ######################## 
        # Estadísticas de zona # --> 4° comando
        ########################
         
        # Calculamos la media a nivel de county para el raster de la población en 1800
        
        alg_params = {
            'COLUMN_PREFIX': 'pop1800',
            'INPUT': 'Estadistica_zonal_c0e0ec63_c6c2_41ac_9286_6ca48f5c74ad',
            'INPUT_RASTER': 'popd_1800AD_d65898e6_814c_4ba3_9cbe_f4ee7c643a84',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Pop1800']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1800'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        ######################## 
        # Estadísticas de zona # --> 6° comando
        ########################
        
        # Calculamos la media a nivel de county para el raster de la población en el 2000
        
        alg_params = {
            'COLUMN_PREFIX': 'pop2000',
            'INPUT': 'Estadistica_zonal_68ed45f8_2f4b_41cd_9242_e49f94d2d3b0',
            'INPUT_RASTER': 'popd_2000AD_ccdd2995_c907_4c13_ab62_0b2966016206',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Pop2000']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop2000'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        ################### 
        # Quitar campo(s) # --> 2° comando
        ###################
        
        # Eliminamos columnas que no utilizamos
        
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': 'Geometr_as_corregidas_d5a06c4d_5b7e_450f_8dc7_5d5a35a76453',
            'OUTPUT': parameters['Drop_fields_3']
        }
        outputs['QuitarCampos'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_fields_3'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        ########################
        # Estadísticas de zona # --> 5° comando
        ########################
        
        # Calculamos la media a nivel de county para el raster de la población en 1900
        
        alg_params = {
            'COLUMN_PREFIX': 'pop1900',
            'INPUT': 'Estadistica_zonal_601740c0_3288_4581_b138_1e9c40750952',
            'INPUT_RASTER': 'popd_1900AD_7ba960e0_8009_44c6_9f5c_efbd2304ef55',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Pop1900']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1900'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        ######################## 
        # Estadísticas de zona # --> 7° comando
        ########################
        
        alg_params = {
            'COLUMN_PREFIX': 'elevation',
            'INPUT': 'Estadistica_zonal_49815408_9934_4670_97ec_d691ac312251',
            'INPUT_RASTER': 'landquality_d932a8e2_d05e_4702_9c72_9d5dd931e64b',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Zonal_statistics']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Zonal_statistics'] = outputs['EstadsticasDeZona']['OUTPUT']
        return results

    def name(self):
        return 'Modelo3'

    def displayName(self):
        return 'Modelo3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Modelo3()
