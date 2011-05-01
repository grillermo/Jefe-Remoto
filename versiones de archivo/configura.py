from configobj import ConfigObj

config = ConfigObj('miconfig.cfg')
config['nombre'] = 'juan'
config['edad'] = 22
config['hermanos'] = ('pedro','paco')
config.write()

dicto = {}
for key,value in config.items():
    print 'loopeando '+str(key)+str(value)

