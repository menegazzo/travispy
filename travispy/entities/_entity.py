from warnings import warn

from travispy._helpers import get_response_contents


class Entity(object):
    '''
    Base class for all |travisci| entities.

    :type session: :class:`.Session`
    :param session:
        Internet session in which entity information will be requested.

    :ivar int id:
        The entity ID.
    '''

    __slots__ = [
        'id',
        '_session',
        '__cache',
    ]

    def __init__(self, session):
        self._session = session

        # A dictionary used to cache objects loaded from lazy information.
        self.__cache = {}

    @classmethod
    def one(cls):
        '''
        :rtype: str
        :returns:
            String representation for a single entity.
            Example: for :class:`.Account` will be ``account``.
        '''
        return cls.__name__.lower()

    @classmethod
    def many(cls):
        '''
        :rtype: str
        :returns:
            String representation for multiple entities.
            Example: for :class:`.Account` will be ``accounts``.
        '''
        return cls.one() + 's'

    @classmethod
    def _find_one_command(cls, command, entity_id, **kwargs):
        '''
        :param str command:
            Command name.

        :type entity_id: int | str
        :param entity_id:
            Entity identification.

        :rtype: str
        :returns:
            API command for retrieving one object.
        '''
        return '/%s/%s' % (command, entity_id,)

    @classmethod
    def find_one(cls, session, entity_id, **kwargs):
        '''
        Method responsible for returning exactly one instance of current class.

        :type session: :class:`.Session`
        :param session:
            Session that must be used to search for result.

        :param int entity_id:
            The ID of the entity.

        :rtype: :class:`.Entity`

        :raises TravisError: when response has status code different than 200.
        '''
        from travispy.entities import COMMAND_TO_ENTITY

        command = cls.one()
        response = session.get(
            session.uri +
            cls._find_one_command(cls.many(), str(entity_id), **kwargs)
        )

        contents = get_response_contents(response)
        if command not in contents:
            return

        info = contents.pop(command, {})
        result = cls._load(info, session)[0]

        for name in contents.keys():

            # Unknown entity.
            if name not in COMMAND_TO_ENTITY:
                continue

            entity_class = COMMAND_TO_ENTITY[name]
            dependency = entity_class._load(contents[name], session)
            if name == entity_class.one():
                dependency = dependency[0]

            setattr(result, name, dependency)

        return result

    # Constant that holds parameter names that should be exclusive.
    # That means no more than one of these values may be given.
    _FIND_MANY_EXCLUSIVE_PARAMETERS = []

    @classmethod
    def find_many(cls, session, **kwargs):
        '''
        Method responsible for returning as many as possible matches for current class.

        :type session: :class:`.Session`
        :param session:
            Session that must be used to search for results.

        :rtype: list(:class:`.Entity`)

        :raises TravisError: when response has status code different than 200.
        '''
        from travispy.entities import COMMAND_TO_ENTITY

        count = 0
        for param in cls._FIND_MANY_EXCLUSIVE_PARAMETERS:
            if param in kwargs:
                count += 1

        if count != 1 and len(cls._FIND_MANY_EXCLUSIVE_PARAMETERS) > 0:
            exclusive_parameters = '", "'.join(cls._FIND_MANY_EXCLUSIVE_PARAMETERS)
            raise RuntimeError('You have to supply either "%s".' % exclusive_parameters)

        command = cls.many()
        response = session.get(session.uri + '/%s' % command, params=kwargs)

        dependencies_result = {}
        contents = get_response_contents(response)

        # Retrieving information from Travis and loading into respective classes.
        infos = contents.pop(command, [])
        result = cls._load(infos, session)

        for name in contents.keys():
            entity_class = COMMAND_TO_ENTITY[name]
            dependencies_result[entity_class.one()] = \
                entity_class._load(contents[name], session)

        # Injecting dependencies into main objects.
        for i, entity in enumerate(result):
            for dependency_name, dependencies in dependencies_result.items():
                setattr(entity, dependency_name, dependencies[i])

        return result

    @classmethod
    def _load(cls, infos, session):
        '''
        Method responsible for creating objects of current class using given ``infos``
        to fill them.

        :type infos: dict | list(dict)
        :param infos:
            JSON information returned by Travis API.

        :param :class:`.Session` session:
            Session that must be given to created objects.

        :rtype: list(:class:`.Entity`)
        :returns:
            List of object filled with given ``infos``.
        '''
        if not isinstance(infos, list):
            infos = [infos]

        result = []
        for info in infos:
            entity = cls(session)
            for key, value in info.items():
                # Log.body from Travis is empty, and is fetched on demand.
                if key == 'body' and info['type'] == 'Log':
                    if value == '':
                        continue
                    else:
                        key = '_body'
                try:
                    setattr(entity, key, value)
                except AttributeError:
                    warn('Unknown {0} attribute {1}'
                         .format(entity.__class__.__name__, key))
            result.append(entity)

        return result

    def _load_lazy_information(self, lazy_information, cache_name, load_method, load_kwarg):
        '''
        Some |travisci| entities stores lazy information (or references) to other entities that they
        have a relationship. Consider :class:`.Build`: it has a reference to its :class:`.Repo`
        container through the attribute ``repository_id`` and other reference to the :class:`.Jobs`
        within it (through ``job_ids``).

        This method is responsible for loading a requested ``lazy_information`` and returning it as
        objects. Also it creates an internal cache so if it is requested more than once, the same
        result will be returned.

        Cache will be updated whenever attribute related to the given ``lazy_information`` is
        changed.

        :param str lazy_information:
            Attribute name where lazy information is stored.

        :param str cache_name:
            Name that will be used to store loaded information.

            .. note::
                Cache will not be accessible from outside the object itself.

        :param callable load_method:
            Method or function that will be used to load lazy information. It must support two
            parameters:

                * :class:`.Session` object (which will be the same as its "parent")
                * ``load_kwarg`` which will receive the stored lazy information

        :param str load_kwarg:
            Name of keyword argument that will be used within ``load_method``.

        :returns:
            The information loaded from stored lazy information. The return type will vary depending
            on what ``load_method`` returns.

        .. seealso:: :meth:`.find_one`
        .. seealso:: :meth:`.find_many`
        '''
        cache = self.__cache

        cached_property_name = 'cached_%s' % cache_name
        cached_property_ref_name = 'cached_%s' % lazy_information

        property_ref = getattr(self, lazy_information)
        if cache.get(cached_property_ref_name) == property_ref:
            return cache[cached_property_name]

        result = load_method(self._session, **{load_kwarg: property_ref})

        # If no result was found, current cache will be deleted.
        if not result:

            if cached_property_ref_name in cache:
                del cache[cached_property_ref_name]

            if cached_property_name in cache:
                del cache[cached_property_name]

        # Valid result should be stored in cache.
        else:
            cache[cached_property_ref_name] = property_ref
            cache[cached_property_name] = result

        return result

    def _load_one_lazy_information(self, entity_class, lazy_information=None):
        '''
        Method responsible for searching one ``entity_class`` based on related ``lazy_information``.

        :type lazy_information: str | None
        :param lazy_information:
            When lazy information is not provided it will be built automatically based on given
            `` entity_class``. See more at :meth:`._load_lazy_information`.

        :rtype: ``entity_class`` instance
        :returns:
            The information loaded from stored lazy information.

        .. seealso:: :meth:`._load_lazy_information`
        '''
        if lazy_information is None:
            lazy_information = '%s_id' % entity_class.one()

        return self._load_lazy_information(
            lazy_information,
            entity_class.one(),
            entity_class.find_one,
            'entity_id',
        )

    def _load_many_lazy_information(self, entity_class, lazy_information=None):
        '''
        Method responsible for searching many ``entity_class`` based on related
        ``lazy_information``.

        :type lazy_information: str | None
        :param lazy_information:
            When lazy information is not provided it will be built automatically based on given
            ``entity_class``. See more at :meth:`._load_lazy_information`.

        :rtype: list(``entity_class`` instance)
        :returns:
            The information loaded from stored lazy information.

        .. seealso:: :meth:`._load_lazy_information`
        '''
        if lazy_information is None:
            lazy_information = '%s_ids' % entity_class.one()

        return self._load_lazy_information(
            lazy_information,
            entity_class.many(),
            entity_class.find_many,
            'ids',
        )

    def __getitem__(self, key):
        return getattr(self, key)
