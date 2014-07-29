import keyring, json, time, getpass
from cookielib import (Cookie, CookieJar, LoadError, iso2time)

class KeyringCookieJar(CookieJar):

  DEFAULT_SERVICE = "Python Keyring Cookie Jar"

  def __init__(self, svc=DEFAULT_SERVICE, acct=None,
      delayload=False, policy=None):

    CookieJar.__init__(self, policy)
    self.svc = "Cookies for " + svc
    self.acct = getpass.getuser() if acct is None else acct
    self.delayload = bool(delayload)

    if not self.delayload: self.load()


  def clear(self, domain=None, path=None, name=None):
    super(KeyringCookieJar, self).clear(domain, path, name)
    self.nuke()
    self.save()


  def nuke(self):
    self.delete_password(self.svc, self.acct)


  def save(self, ignore_discard=False, ignore_expires=False):
    keyring.set_password(self.svc, self.acct,
        self.to_json(ignore_discard, ignore_expires))


  def load(self, ignore_discard=False, ignore_expires=False):
    dough = keyring.get_password(self.svc, self.acct) or "[]"
    for cookie in json.loads(dough):
      self.load_cookie(cookie, ignore_discard, ignore_expires)


  def load_cookie(self, c, ignore_discard=False, ignore_expires=False):
    expires = c['expires']
    discard = c['discard'] if expires is not None else True
    domain = c['domain']
    domain_specified = domain.startswith(".")
    c = Cookie(c['version'], c['name'], c['value'],
      c['port'], c['port_specified'],
      domain, domain_specified, c['domain_initial_dot'],
      c['path'], c['path_specified'],
      c['secure'],
      expires,
      discard,
      c['comment'],
      c['comment_url'],
      {})

    if not ignore_discard and c.discard: return
    if not ignore_expires and c.is_expired(): return

    self.set_cookie(c)


  def get_value(self, name):
    for cookie in self:
      if cookie.name != name: continue
      return cookie.value
    return None


  def cookie_to_dict(self, c):
    return {
      'version': c.version,
      'name': c.name,
      'value': c.value,
      'port': c.port,
      'port_specified': c.port_specified,
      'domain': c.domain,
      'domain_specified': c.domain_specified,
      'domain_initial_dot': c.domain_initial_dot,
      'path': c.path,
      'path_specified': c.path_specified,
      'secure': c.secure,
      'expires': c.expires,
      'discard': c.discard,
      'comment': c.comment,
      'comment_url': c.comment_url,
      'rfc2109': c.rfc2109,
    }


  def to_json(self, ignore_discard=False, ignore_expires=False):
    r = []
    for cookie in self:
      if not ignore_discard and cookie.discard: continue
      if not ignore_expires and cookie.is_expired(): continue
      r.append(self.cookie_to_dict(cookie))

    return json.dumps(r)
