#===================================================================================================
# Entity
#===================================================================================================
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


    def _load_from_lazy_information(self, lazy_information, entity_class, cache_name, load_method, load_kwarg):
        '''
        Some |travisci| entities stores lazy information (or references) to other entities that they
        have a relationship. Consider :class:`.Build`: it has a reference to its :class:`.Repo`
        container through the attribute ``repository_id`` and other reference to the :class:`.Jobs`
        within it (through ``job_ids``).

        This method is responsible for loading a requested ``lazy_information`` and returning it as
        objects of the given ``entity_class``. Also it creates an internal cache so if it is
        requested more than once, the same result will be returned.

        Cache will be updated whenever attribute related to the given ``lazy_information`` is
        changed.

        :param str lazy_information:
            Attribute name where lazy information is stored.

        :type entity_class: :class:`.Entity`
        :param entity_class:
            Class of entity which will be loaded from lazy information.

        :param str cache_name:
            Name that will be used to store loaded information.

            .. note::
                Cache will not be accessible from outside the object itself.

        :param callable load_method:
            Method or function that will be used to load lazy information. It must support two
            parameters:

                * given ``entity_class``
                * ``load_kwarg`` which will receive the stored lazy information

        :param str load_kwarg:
            Name of keyword argument that will be used within ``load_method``.

        :rtype: ``entity_class`` instance | list(``entity_class`` instance)
        :returns:
            The information loaded from stored lazy information. The return type will vary depending
            on what ``load_method`` returns.
        '''
        cache = self.__cache

        cached_property_name = 'cached_%s' % cache_name
        cached_property_ref_name = 'cached_%s' % lazy_information

        property_ref = getattr(self, lazy_information)
        if cache.get(cached_property_ref_name) == property_ref:
            return cache[cached_property_name]

        result = load_method(entity_class, **{load_kwarg: property_ref})

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
            `` entity_class``. See more at :meth:`._load_from_lazy_information`.

        :rtype: ``entity_class`` instance
        :returns:
            The information loaded from stored lazy information.

        .. seealso:: :meth:`._load_from_lazy_information`
        '''
        if lazy_information is None:
            lazy_information = '%s_id' % entity_class.one()

        return self._load_from_lazy_information(
            lazy_information,
            entity_class,
            entity_class.one(),
            self._session.find_one,
            'entity_id',
        )


    def _load_many_lazy_information(self, entity_class, lazy_information=None):
        '''
        Method responsible for searching many ``entity_class`` based on related ``lazy_information``.

        :type lazy_information: str | None
        :param lazy_information:
            When lazy information is not provided it will be built automatically based on given
            `` entity_class``. See more at :meth:`._load_from_lazy_information`.

        :rtype: list(``entity_class`` instance)
        :returns:
            The information loaded from stored lazy information.

        .. seealso:: :meth:`._load_from_lazy_information`
        '''
        if lazy_information is None:
            lazy_information = '%s_ids' % entity_class.one()

        return self._load_from_lazy_information(
            lazy_information,
            entity_class,
            entity_class.many(),
            self._session.find_many,
            'ids',
        )


    def __getitem__(self, key):
        return getattr(self, key)
