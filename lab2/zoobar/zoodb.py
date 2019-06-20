from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import os
from debug import *

CredBase = declarative_base()
BankBase = declarative_base()
PersonBase = declarative_base()
PcodeBase = declarative_base()
TransferBase = declarative_base()

class Person(PersonBase):
    __tablename__ = "person"
    username = Column(String(128), primary_key=True)

class Pcode(PcodeBase):
    __tablename__ = "pcode"
    username = Column(String(128), primary_key=True)
    profile = Column(String(5000), nullable=False, default="")

class Cred(CredBase):
    __tablename__ = "cred"
    username = Column(String(128), primary_key=True)
    password = Column(String(128))
    salt = Column(String(128))
    token = Column(String(128))

class Bank(BankBase):
    __tablename__ = "bank"
    username = Column(String(128), primary_key=True)
    zoobars = Column(Integer, nullable=False, default=10)

class Transfer(TransferBase):
    __tablename__ = "transfer"
    id = Column(Integer, primary_key=True)
    sender = Column(String(128))
    recipient = Column(String(128))
    amount = Column(Integer)
    time = Column(String)
    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

def dbsetup(name, base):
    thisdir = os.path.dirname(os.path.abspath(__file__))
    dbdir   = os.path.join(thisdir, "db", name)
    if not os.path.exists(dbdir):
        os.makedirs(dbdir)

    dbfile  = os.path.join(dbdir, "%s.db" % name)
    engine  = create_engine('sqlite:///%s' % dbfile,
                            isolation_level='SERIALIZABLE')
    base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()

def bank_setup():
    return dbsetup("bank", BankBase)

def cred_setup():
    return dbsetup("cred", CredBase)

def person_setup():
    return dbsetup("person", PersonBase)

def transfer_setup():
    return dbsetup("transfer", TransferBase)

def pcode_setup():
    return dbsetup("pcode", PcodeBase)

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s [init-person|init-transfer|init-cred|init-bank|init-pcode]" % sys.argv[0]
        exit(1)

    cmd = sys.argv[1]
    if cmd == 'init-person':
        person_setup()
    elif cmd == 'init-transfer':
        transfer_setup()
    elif cmd == 'init-cred':
        cred_setup()
    elif cmd == 'init-bank':
        bank_setup()
    elif cmd == 'init-pcode':
        pcode_setup()
    else:
        raise Exception("unknown command %s" % cmd)
