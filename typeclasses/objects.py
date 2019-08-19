from evennia import DefaultObject
from evennia.utils import create
from evennia.utils import logger
from world.generic_str import article

class Object(DefaultObject):
    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.
        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""
        desc = self.db.desc
        return desc

    @classmethod
    def create(cls, key, account=None, **kwargs):
        """
        Creates a basic object with default parameters, unless otherwise
        specified or extended.
        Provides a friendlier interface to the utils.create_object() function.
        Args:
            key (str): Name of the new object.
            account (Account): Account to attribute this object to.
        Kwargs:
            description (str): Brief description for this object.
            ip (str): IP address of creator (for object auditing).
        Returns:
            object (Object): A newly created object of the given typeclass.
            errors (list): A list of errors in string form, if any.
        """
        errors = []
        obj = None

        # Get IP address of creator, if available
        ip = kwargs.pop('ip', '')

        # If no typeclass supplied, use this class
        kwargs['typeclass'] = kwargs.pop('typeclass', cls)

        # Set the supplied key as the name of the intended object
        kwargs['key'] = key

        # Get a supplied description, if any
        description = kwargs.pop('description', '')

        # Create a sane lockstring if one wasn't supplied
        lockstring = kwargs.get('locks')
        if account and not lockstring:
            lockstring = cls.lockstring.format(account_id=account.id)
            kwargs['locks'] = lockstring

        # Create object
        try:
            obj = create.create_object(**kwargs)

            # Record creator id and creation IP
            if ip: obj.db.creator_ip = ip
            if account: obj.db.creator_id = account.id

            # Set description if there is none, or update it if provided
            if description or not obj.db.desc:
                desc = description if description else f"You see nothing special about {obj.name}."
                obj.db.desc = desc

        except Exception as e:
            errors.append(f"An error occurred while creating this '{key}' object.")
            logger.log_err(e)

        return obj, errors

class ObjHands(Object):
    def return_appearance(self, looker, **kwargs):
        looker.msg(f"You see nothing spectacular about your {self.key}.")

class Staves(Object):
    def at_object_creation(self):
        self.attributes.add('wieldable', 2)
