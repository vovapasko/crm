class PermissionInUse(Exception):
    """
    Exception for upgrade_groups command when some permission
    was deleted but actually it is used in some group
    """
    pass
