# This an example of how we can expose a particular function in a 3rd party library
# as a function within the albert-ds library. The point of doing this is to create a uniform
# interface through which all of our applications can use this function, and should we decide to
# later change the implementation we can use the same name and not worry about having to
# change/update the dependency in the application layer.

from Levenshtein import distance as levenshtein_distance #noqa
