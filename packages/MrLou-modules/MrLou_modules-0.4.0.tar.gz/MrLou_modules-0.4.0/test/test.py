from MrLou_modules.Certificate_Utils.cert_utils import convert_pkcs12_to_x509_with_chain, convert_pkcs12_to_x509_with_root_chain

p12_path = r"c:\users\ldescamp\downloads\acsba.qbetest.com.pfx"
p12_password = input("type your password: ")
cert_out_path = r"c:\users\ldescamp\downloads\output_certificate.pem"
key_out_path = r"c:\users\ldescamp\downloads\output_private_key.pem"
fullchain_out_path = r"c:\users\ldescamp\downloads\output_full_chain.pem"

convert_pkcs12_to_x509_with_chain(
    p12_path=p12_path,
    p12_password=p12_password,
    cert_out_path=cert_out_path,
    key_out_path=key_out_path,
    fullchain_out_path=fullchain_out_path
)

