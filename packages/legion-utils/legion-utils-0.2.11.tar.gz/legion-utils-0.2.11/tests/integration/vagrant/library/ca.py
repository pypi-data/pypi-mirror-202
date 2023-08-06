#!/usr/bin/env python3

# Copyright: (c) 2020, Eugene Kovalev <eugene@kovalev.io>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4 as uuid
from ansible.module_utils.basic import AnsibleModule
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.serialization import NoEncryption
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PrivateFormat, load_pem_private_key
from cryptography.x509 import CertificateBuilder, Name, NameAttribute, BasicConstraints
from cryptography.x509 import KeyUsage, AuthorityKeyIdentifier, SubjectKeyIdentifier
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

DOCUMENTATION = '''
---
module: ca

short_description: An ansible module for managing a certificate authority. Pairs with the cert module.

version_added: "0.1"

description:
    - "This module can generate a CA key and certificate, as well as generate a new certificate for the same if the existing certificate is close to expiry. The module is designed with idempotency in mind, so it will only re-generate a certificate if one is close to expiry or if one of the properties does not match, implying that it has changed. This module will not create a new CA key if and only if one does not already exist. Even so, to prevent serious issues like loss of a CA certificate due to an accidental change, this module should be used in concert with version control."

options:
    ca_dir:
        description:
            - The directory where the certificate authority files will be kept. The CA cert and key will be at: <ca_dir>/<common_name>.crt and <ca_dir>/<common_name>.key respectively, while all generated keys and issued certificates will be at <ca_dir>/issued/<host_name>/ (assuming that complimenting private_key and certificate modules are used. If the directory does not exist, it will be created with the following permissions: u=rwx,g=o=
        required: True
    common_name:
        description:
            - This is the common name of the CA. It will be used as part of the file save-path: <common_name>.key and <common_name>.crt
        required: true
    country:
        description:
            - Country, part of the subject name
        required: true
    locality:
        description:
            - Locality, part of the subject name
        required: true
    state_or_province:
        description:
            - State/province, part of the subject name
        required: true
    org:
        description:
            - Organization name, part of the subject name
        required: true
    org_unit:
        description:
            - Organizational unit part of the subject name
        required: true
    email:
        description:
            - The email address associated with the CA
        required: true
    expire_days:
        description:
            - In the event that the module has to create a new certificate, this value will be used to determine when the cert should expire (measured in days).
        required: true
    renew_if_expiring_before:
        description:
            - If an existing certificate is expiring before today + the number of days provided in this value, the module will regenerate the certificate. Note that the expire_days value is less than renew_if_expiring_before, the certificate will be re-generated every time the module is used.
        required: true

author:
    - Eugene Kovalev (@cyclicircuit)
'''

EXAMPLES = '''
# Create a certificate authority on the ansible controller (can be used in concert with copy module to distribute the certificate
- name: Create a certificate authority called "Skynet" for 20 years with a renewal 30 days before expiry.
  ca:
    ca_dir: "{{ inventory_dir }}/host_files/pki/skynet/"
    common_name: skynet-ca
    country: US
    state_or_province: MA
    locality: Boston
    org: Kovalev
    org_unit: Skynet Network
    email: eugene@kovalev.io
    expire_days: 7300 # 20 years
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

def new_ca_cert(common_name,
                country_name,
                locality_name,
                province_name,
                org_name,
                org_unit_name,
                email,
                expire_days,
                serial_number,
                ca_key):
    ca_subj_name = name(common_name, country_name, locality_name, province_name,
                        org_name, org_unit_name, email)
    ski_ext = SubjectKeyIdentifier.from_public_key(ca_key.public_key())
    builder = CertificateBuilder()
    builder = builder.subject_name(ca_subj_name)
    builder = builder.issuer_name(ca_subj_name)
    builder = builder.not_valid_before(datetime.today() - timedelta(days=1))
    builder = builder.not_valid_after(datetime.today() + timedelta(days=expire_days))
    builder = builder.serial_number(serial_number)
    builder = builder.public_key(ca_key.public_key())
    builder = builder.add_extension(BasicConstraints(ca=True, path_length=None), critical=False)
    builder = builder.add_extension(KeyUsage(digital_signature=False,
                                             content_commitment=False,
                                             key_encipherment=False,
                                             data_encipherment=False,
                                             key_agreement=False,
                                             key_cert_sign=True,
                                             crl_sign=True,
                                             encipher_only=False,
                                             decipher_only=False), critical=False)
    builder = builder.add_extension(AuthorityKeyIdentifier.from_issuer_subject_key_identifier(ski_ext), critical=False)
    builder = builder.add_extension(ski_ext, critical=False)
    return builder.sign(private_key=ca_key, algorithm=SHA512(), backend=default_backend())

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

def satisfies_constraints(cert_path, common_name, country_name, locality_name,
                          province_name, org_name, org_unit_name, email,
                          expiring_after_days):
    if not cert_path.exists():
        return False, "Certificate does not exist"
    cert = load_pem_x509_certificate(cert_path.open('rb').read(), default_backend())
    name_should_be = name(common_name, country_name, locality_name, province_name,
                           org_name, org_unit_name, email)
    expiring_soon = datetime.now() + timedelta(days=expiring_after_days) > cert.not_valid_after
    if expiring_soon:
        return False, f"The certificate {cert_path} is expiring in less than {expiring_after_days} days: {str(cert.not_valid_after)}"
    if cert.issuer != name_should_be:
        return False, f"The certificate issuer name {cert.issuer} does not match {name_should_be}"
    if cert.subject != name_should_be:
        return False, f"The certificate subject name {cert.subject} does not match {name_should_be}"
    return True, 'Certificate properties match constraints, no changes required'

def run_module():
    module_args = dict(
        ca_dir=dict(type='str', required=True),
        common_name=dict(type='str', required=True),
        country=dict(type='str', required=True),
        locality=dict(type='str', required=True),
        state_or_province=dict(type='str', required=True),
        org=dict(type='str', required=True),
        org_unit=dict(type='str', required=True),
        email=dict(type='str', required=True),
        expire_days=dict(type='int', required=True),
        renew_if_expiring_before=dict(type='int', required=True))
    result = {'changed': False, 'message': '', 'ca_dir_created': False, 'key_created': False}
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

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
    serial = int(uuid())
    ca_key_path = Path(ca_dir) / (common_name + '.key')
    ca_crt_path = Path(ca_dir) / (common_name + '.crt')
    cert_ok, msg = satisfies_constraints(ca_crt_path, common_name, country, locality,
                                         province, org, org_unit, email,
                                         renew_if_expiring_before)
    
    if module.check_mode:
        if not ca_dir.exists():
            result['changed'] = True
            result['message'] = 'The CA dir and all contents would be created'
            result['ca_dir_created'] = True
            result['key_created'] = True
        elif not ca_key_path.exists():
            result['changed'] = True
            result['message'] = 'The CA key and certificate would be created'
            result['ca_dir_created'] = False
            result['key_created'] = True
        elif not ca_cert_path.exists():
            result['changed'] = True
            result['message'] = 'The CA certificate would be created'
            result['ca_dir_created'] = False
            result['key_created'] = False
        elif not cert_ok:
            result['changed'] = True
            result['message'] = msg
            result['ca_dir_created'] = False
            result['key_created'] = False
        else:
            result['changed'] = False
            result['message'] = 'No changes required'
            result['ca_dir_created'] = False
            result['key_created'] = False
    else: # not in check-mode, so we do all this for real
        if not ca_dir.exists():
            result['changed'] = True
            ca_dir.mkdir(0o700, parents=True, exist_ok=True)
            result['ca_dir_created'] = False
        if not ca_key_path.exists():
            result['changed'] = True
            key = new_private_key()
            key_to_file(key, ca_key_path)
            result['key_created'] = True
            # if we create a new key, we always create a new cert
            cert_to_file(new_ca_cert(common_name, country, locality, province,
                                     org, org_unit, email, expire_days, serial, key),
                         ca_crt_path)
            result['message'] = 'Generated new key and cert'
        elif not cert_ok:
            result['changed'] = True
            key = key_from_file(ca_key_path)
            cert_to_file(new_ca_cert(common_name, country, locality, province,
                                     org, org_unit, email, expire_days, serial, key), ca_crt_path)
            result['message'] = 'A new CA certificate was generated because: ' + msg
    module.exit_json(**result)

def main():
    cert_file = Path('test-ca.crt')
    key_file = Path('test-ca.key')
    key = new_private_key()
    cert = new_ca_cert('test-common-name',
                       'US',
                       'MA',
                       'Boston',
                       'Kovalev',
                       'Skynet Network',
                       'eugene@kovalev.io',
                       90,
                       9918063603715682735,
                       key)
    key_to_file(key, key_file)
    cert_to_file(cert, cert_file)
    assert satisfies_constraints(cert_file,
                          'test-common-name',
                          'US',
                          'MA',
                          'Boston',
                          'Kovalev',
                          'Skynet Network',
                          'eugene@kovalev.io',
                          30,
                          9918063603715682735)

if __name__ == '__main__':
    run_module()
