import requests



#===================================================================================================
# Session
#===================================================================================================
class Session(requests.Session):
    '''
    Internet session created to perform requests to |travisci|.

    :param str uri:
        URI where session will start.
    '''

    def __init__(self, uri):
        requests.Session.__init__(self)
        self.uri = uri


    def find_one(self, entity_class, entity_id, **kwargs):
        '''
        Method responsible for returning exactly one instance of the given ``entity_class``.

        :type entity_class: :class:`.Entity`
        :param entity_class:
            Class of entity that information will be retrieved from |travisci|.

        :param int entity_id:
            The ID of the entity.

        :rtype: ``entity_class`` instance
        '''
        response = self.get(self.uri + '/%s/%s' % (entity_class.many(), str(entity_id)))

        if response.status_code == 200:
            contents = response.json()
            info = contents.get(entity_class.one(), {})
            if not info:
                return

            entity = entity_class(self)
            for key, value in info.items():
                setattr(entity, key, value)

            return entity


    def find_many(self, entity_class, **kwargs):
        '''
        Method responsible for returning as many as possible matches for given ``entity_class``.

        :type entity_class: :class:`.Entity`
        :param entity_class:
            Class of entity that information will be retrieved from |travisci|.

        :rtype: list(``entity_class``)
        '''
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
