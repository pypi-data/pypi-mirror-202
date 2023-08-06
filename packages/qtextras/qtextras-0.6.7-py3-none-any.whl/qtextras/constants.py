import logging


class LibraryNamespace:
    ADD_TYPE_MERGE = "merge"
    ADD_TYPE_NEW = "new"

    # Logging level for 'attention': Like logging.INFO, but requests more of the
    # user's attention
    LOG_LEVEL_ATTENTION = logging.INFO + 1


class PrjEnums(LibraryNamespace):
    # Deprecated, use LibraryNamespace instead
    LOG_LVL_ATTN = LibraryNamespace.LOG_LEVEL_ATTENTION
