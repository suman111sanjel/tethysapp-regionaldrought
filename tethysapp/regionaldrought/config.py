# from t
from tethysapp.regionaldrought.app import Regionaldrought
TethysAppName=Regionaldrought.package
initilizationData={
    'country':'Nepal',
    'navLogoImage':'/static/'+TethysAppName+'/images/logo-icimod.png',
    'defaultView':{
        'center': [9388155.512006583, 3291367.8109067543],
        'zoom': 6
    },
    'TethysAppName':TethysAppName,
    'AdminLevel':'l2Jumla',
}
