import requests



#===================================================================================================
# Session
#===================================================================================================
class Session(requests.Session):

    def __init__(self, uri):
        requests.Session.__init__(self)
        self.uri = uri


    def find_one(self, entity_class, entity_id, **kwargs):
        response = self.get(self.uri + '/%s/%s' % (entity_class.many(), str(entity_id)))

        if response.status_code == 200:
            contents = response.json()
            info = contents.get(entity_class.one(), {})
            entity = entity_class(self)
            for key, value in info.items():
                setattr(entity, key, value)
            return entity


    def find_many(self, entity_class, **kwargs):
        command = entity_class.many()
        response = self.get(self.uri + '/%s' % command, params=kwargs)

        result = []
        if response.status_code == 200:
            contents = response.json()
            info = contents.get(command, [])
            for i in info:
                entity = entity_class(self)
                for key, value in i.items():
                    setattr(entity, key, value)
                result.append(entity)

        return result
