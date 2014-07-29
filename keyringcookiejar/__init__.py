import keyring
from cookielib import (_warn_unhandled_exception, FileCookieJar, LoadError,
                       Cookie, MISSING_FILENAME_TEXT,
                       join_header_words, split_header_words,
                       iso2time, time2isoz)

class KeyringCookieJar(FileCookieJar):

  def save(self, filename=None, ignore_discard=False, ignore_expires=False):
    return 0
    
  def _really_load(self, f, filename, ignore_discard, ignore_expires):
    return 0
