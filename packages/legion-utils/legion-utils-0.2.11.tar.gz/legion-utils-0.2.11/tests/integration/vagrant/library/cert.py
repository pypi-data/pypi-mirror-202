#!/usr/bin/env python3

# Copyright: (c) 2020, Eugene Kovalev <eugene@kovalev.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from datetime import datetime, timedelta
from uuid import uuid4 as uuid
from pathlib import Path
from ipaddress import IPv4Address
from ansible.module_utils.basic import AnsibleModule
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.serialization import NoEncryption
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PrivateFormat, load_pem_private_key
from cryptography.x509 import CertificateBuilder, Name, NameAttribute, BasicConstraints
from cryptography.x509 import KeyUsage, AuthorityKeyIdentifier, SubjectKeyIdentifier
from cryptography.x509 import load_pem_x509_certificate, ExtendedKeyUsage
from cryptography.x509 import SubjectAlternativeName, DNSName, IPAddress
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID, ExtensionOID

EXTENDED_KEY_USAGE_SERVER = [ExtendedKeyUsageOID.SERVER_AUTH,
                             ExtendedKeyUsageOID.CLIENT_AUTH,
                             ExtendedKeyUsageOID.CODE_SIGNING]

EXAMPLES = '''
# Create a certificate and private key with given DNS and IP SANs and sign it with a CA
- name: Create a certificate for a server called grab-e for 60 days with a renewal 30 days before expiry.
  cert:
    ca_dir: "{{ inventory_dir }}/host_files/pki/skynet/"
    ca: skynet-ca
    dns_sans: ['localhost', '']
    ip_sans: ['192.168.86.54', '127.0.0.1']
    common_name: grab-e
    country: US
    state_or_province: MA
    locality: Boston
    org: Kovalev
    org_unit: Skynet Network
    email: eugene@kovalev.io
    expire_days: 60
    renew_if_expiring_before: 30
  delegate_to: 127.0.0.1
'''

RETURN = '''
message:
    description: A message regarding why the module generated a new certificate if the previous certificate did not meet a constraint.
    type: str
    returned: always
ca_dir_created:
    description: Indicates whether the CA directory was created or not
    type: bool
    returned: always
key_created:
    description: Indicates whether the CA private key was created or not
    type: bool
    returned: always
'''

def new_private_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend())

def key_to_file(key, file_path):
    file_path.open('wb+').write(key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=NoEncryption()))

def cert_to_file(cert, file_path):
    file_path.open('wb+').write(cert.public_bytes(
        encoding=Encoding.PEM))

def key_from_file(file_path):
    return load_pem_private_key(file_path.open('rb').read(), None, default_backend())

def cert_from_file(file_path):
    return load_pem_x509_certificate(file_path.open('rb').read(), default_backend())

def sans(cert):
    for ext in cert.extensions:
        if ext.oid == ExtensionOID.SUBJECT_ALTERNATIVE_NAME:
            return {str(n.value) for n in ext.value}

def name(common_name, country_name, locality_name, province_name,
         org_name, org_unit_name, email):
    return Name([
        NameAttribute(NameOID.COUNTRY_NAME, country_name),
        NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, province_name),
        NameAttribute(NameOID.LOCALITY_NAME, locality_name),
        NameAttribute(NameOID.ORGANIZATION_NAME, org_name),
        NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, org_unit_name),
        NameAttribute(NameOID.COMMON_NAME, common_name),
        NameAttribute(NameOID.EMAIL_ADDRESS, email)])

def new_cert(subject_name,
             expire_days,
             serial_number,
             ca_key,
             ca_cert,
             priv_key,
             dns_sans,
             ip_sans):
    return CertificateBuilder().subject_name(
        subject_name
    ).issuer_name(
        ca_cert.subject
    ).add_extension(
        SubjectKeyIdentifier.from_public_key(
            priv_key.public_key()
        ),
        critical=False
    ).add_extension(
        AuthorityKeyIdentifier.from_issuer_subject_key_identifier(
            SubjectKeyIdentifier.from_public_key(
                ca_key.public_key()
            )
        ),
        critical=False
    ).not_valid_before(
        datetime.today() - timedelta(days=1)
    ).not_valid_after(
        datetime.today() + timedelta(days=expire_days)
    ).serial_number(
        serial_number
    ).public_key(
        priv_key.public_key()
    ).add_extension(
        BasicConstraints(ca=False, path_length=None),
        critical=False
    ).add_extension(
        ExtendedKeyUsage(EXTENDED_KEY_USAGE_SERVER),
        critical=False
    ).add_extension(
        KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=True,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=False,
            crl_sign=False,
            encipher_only=False,
            decipher_only=False
        ),
        critical=False
    ).add_extension(
        SubjectAlternativeName(
            [DNSName(h) for h in dns_sans] + [IPAddress(IPv4Address(ip)) for ip in ip_sans]
        ),
        critical=False
    ).sign(
        private_key=ca_key,
        algorithm=SHA512(),
        backend=default_backend()
    )

def satisfies_constraints(cert, subject_name, issuer_name,
                          expiring_after_days, ip_sans, dns_sans):
    expiring_soon = datetime.now() + timedelta(days=expiring_after_days) > cert.not_valid_after
    if expiring_soon:
        return False, f"The certificate {cert} is expiring in less than {expiring_after_days} days: {str(cert.not_valid_after)}"
    if cert.issuer != issuer_name:
        return False, f"The certificate issuer name {cert.issuer} does not match {issuer_name}"
    if cert.subject != subject_name:
        return False, f"The certificate subject name {cert.subject} does not match {subject_name}"
    if sans(cert) != set(list(dns_sans) + list(ip_sans)):
        return False, f"The certificates subject-alt names {sans(cert)} do not match {set(list(dns_sans) + list(ip_sans))}"
    return True, 'Certificate properties match constraints, no changes required'

def run_module():
    module_args = dict(
        ca_dir=dict(type='str', required=True),
        ca=dict(type='str', required=True),
        common_name=dict(type='str', required=True),
        country=dict(type='str', required=True),
        locality=dict(type='str', required=True),
        state_or_province=dict(type='str', required=True),
        org=dict(type='str', required=True),
        org_unit=dict(type='str', required=True),
        email=dict(type='str', required=True),
        expire_days=dict(type='int', required=True),
        renew_if_expiring_before=dict(type='int', required=True),
        dns_sans=dict(type='list', elements='str', required=False),
        ip_sans=dict(type='list', elements='str', required=False))
    result = {'changed': False, 'message': '', 'dir_created': False, 'key_created': False}
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    ca = module.params['ca']
    ca_dir = Path(module.params['ca_dir'])
    common_name = module.params['common_name']
    country = module.params['country']
    locality = module.params['locality']
    province = module.params['state_or_province']
    org = module.params['org']
    org_unit = module.params['org_unit']
    email = module.params['email']
    expire_days = module.params['expire_days']
    renew_if_expiring_before = module.params['renew_if_expiring_before']
    dns_sans = set(module.params['dns_sans'])
    ip_sans = set(module.params['ip_sans'])
    ca_key_path = Path(ca_dir) / (ca + '.key')
    ca_crt_path = Path(ca_dir) / (ca + '.crt')

    if not ca_key_path.exists() or not ca_crt_path.exists():
        module.fail_json(msg=f'The CA {ca} does not have a configured key and cert in {ca_dir}', **result)
    
    ca_key = key_from_file(ca_key_path)
    ca_crt = cert_from_file(ca_crt_path)
    server_dir = Path(ca_dir) / 'issued' / common_name
    key_path = server_dir / (common_name + '.key')
    crt_path = server_dir/ (common_name + '.crt')
    serial = int(uuid())
    cert_ok, msg = satisfies_constraints(cert_from_file(crt_path),
                                         name(common_name, country, locality, province, org, org_unit, email),
                                         ca_crt.subject,
                                         renew_if_expiring_before,
                                         dns_sans,
                                         ip_sans) if crt_path.exists() else (False,
                                                                             f'Certificate {common_name} does not exist')
    
    if module.check_mode:
        if not server.exists():
            result['changed'] = True
            result['message'] = 'The server dir and all contents would be created'
            result['dir_created'] = True
            result['key_created'] = True
        elif not key_path.exists():
            result['changed'] = True
            result['message'] = 'The server key and certificate would be created'
            result['dir_created'] = False
            result['key_created'] = True
        elif not crt_path.exists():
            result['changed'] = True
            result['message'] = 'The server certificate would be created'
            result['dir_created'] = False
            result['key_created'] = False
        elif not cert_ok:
            result['changed'] = True
            result['message'] = msg
            result['dir_created'] = False
            result['key_created'] = False
        else:
            result['changed'] = False
            result['message'] = 'No changes required'
            result['dir_created'] = False
            result['key_created'] = False
    else: # not in check-mode, so we do all this for real
        server_name = name(common_name, country, locality, province, org, org_unit, email)
        if not server_dir.exists():
            result['changed'] = True
            server_dir.mkdir(0o700, parents=True, exist_ok=True)
            result['dir_created'] = False
        if not key_path.exists():
            result['changed'] = True
            key = new_private_key()
            key_to_file(key, key_path)
            result['key_created'] = True
            # if we create a new key, we always create a new cert
            cert_to_file(new_cert(server_name, expire_days, serial, ca_key, ca_crt, key, dns_sans, ip_sans),
                         crt_path)
            result['message'] = 'Generated new key and cert'
        elif not cert_ok:
            result['changed'] = True
            key = key_from_file(key_path)
            cert_to_file(new_cert(server_name, expire_days, serial, ca_key, ca_crt, key, dns_sans, ip_sans),
                         crt_path)
            result['message'] = 'A new certificate was generated because: ' + msg
    module.exit_json(**result)

def main():
    key = new_private_key()
    ca_key = key_from_file(Path('test-ca.key'))
    ca_crt = cert_from_file(Path('test-ca.crt'))
    server_name = name('test-server', 'US', 'Boston', 'MA', 'Kovalev', 'Skynet Network', 'eugene@kovalev.io')
    server_cert = new_cert(server_name,
                           60,
                           9918063603715682735,
                           ca_key,
                           ca_crt,
                           key,
                           ['localhost', 'grab-e', 'grab-e.lan'],
                           ['127.0.0.1', '192.168.86.54', '10.0.0.12'])
    key_to_file(key, Path('test-server.key'))
    cert_to_file(server_cert, Path('test-server.crt'))
    print(satisfies_constraints(cert_from_file(Path('test-server.crt')),
                                server_name,
                                ca_crt.subject,
                                30, 9918063603715682735,
                                ['localhost', 'grab-e', 'grab-e.lan'],
                                ['127.0.0.1', '192.168.86.54', '10.0.0.12']))

if __name__ == '__main__':
    run_module()
