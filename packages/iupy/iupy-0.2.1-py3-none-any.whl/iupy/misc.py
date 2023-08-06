import datetime
import getpass
import platform


def text_header(**kwargs):
    """
    Returns a timestamp / username header.

    Lines are escaped by default.

    :return:
    """

    # Comment Start

    if 'comment' in kwargs:
        comment = kwargs.get("comment")
    else:
        comment = "!"

    header = "{} Generated at...: {}\n".format(comment, str(datetime.datetime.now()))
    header += "{}           by...: {}\n".format(comment, getpass.getuser())
    header += "{}           on...: {}\n".format(comment, platform.node())

    # If a source was specified for the header, include it.
    if 'genfrom' in kwargs:
        header += "{}           from.: {}\n".format(comment, kwargs.get("getfrom"))

    # If code is being generated for another party that is _not_ the user, specify it here.
    if 'genfor' in kwargs:
        header += "{}           for..: {}\n".format(comment, kwargs.get("genfor"))

    header += "{}\n".format(comment)

    if 'footer' in kwargs:
        header += "{} {}\n".format(comment, kwargs.get("footer"))
        header += "{}\n".format(comment)

    return header


def merge_dict(ad, bd):
    """
    Function that merges two dictionaries together, uses recursion to handle the nesting.

    Returns an empty dictionary if any input is not a dictionary.

    Inspired by:
    https://stackoverflow.com/questions/43797333/how-to-merge-two-nested-dict-in-python

    :param ad:
    :param bd:
    :return:
    """
    if not isinstance(ad, dict) or not isinstance(bd, dict):
        return {}

    for key in bd:
        if key in ad:
            ad[key] = merge_dict(ad[key], bd[key])
        else:
            ad[key] = bd[key]

    return ad
