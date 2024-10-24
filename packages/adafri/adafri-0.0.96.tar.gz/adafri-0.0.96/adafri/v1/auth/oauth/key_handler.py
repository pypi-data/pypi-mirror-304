from authlib.jose import JsonWebKey
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Step 1: Generate RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Step 2: Generate a JWK (JSON Web Key) from the RSA key
jwk = JsonWebKey(alg='RS256').generate_key(kty='RSA', crv_or_size=2048)

# Convert the private key to JWK format
private_jwk = jwk.as_dict(is_private=True)
public_jwk = jwk.as_dict(is_private=False)

print("Private JWK:", private_jwk)
print("Public JWK:", public_jwk)
jwk_set = {
    "keys": [public_jwk]
}

# Save the keys as needed