import argparse
from ldap3 import Server, Connection, ALL, NTLM

parser = argparse.ArgumentParser()
parser.add_argument('--username', required=True)
parser.add_argument('--password', required=True)
args = parser.parse_args()

# Tilpass disse til ditt domene
AD_SERVER = 'dc01.dittdomene.local'
AD_USER = 'DOMENE\\adminbruker'
AD_PASS = 'SterktPassord123'
BASE_DN = 'OU=Brukere,DC=dittdomene,DC=local'

# Koble til AD
server = Server(AD_SERVER, get_info=ALL)
conn = Connection(server, user=AD_USER, password=AD_PASS, authentication=NTLM, auto_bind=True)

# Bruker-DN
dn = f'CN={args.username},{BASE_DN}'

# Brukerattributter
attrs = {
    'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
    'cn': args.username,
    'sAMAccountName': args.username,
    'userPrincipalName': f"{args.username}@dittdomene.local",
    'userAccountControl': 544,  # Aktiv konto, krever passord
    'unicodePwd': f'"{args.password}"'.encode('utf-16-le')
}

conn.add(dn, attributes=attrs)

# Tving passordbytte ved første innlogging
conn.modify(dn, {'pwdLastSet': [(0, 0)]})
print(f"Bruker {args.username} opprettet.")
