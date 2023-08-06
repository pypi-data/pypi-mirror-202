import os

from ferveo_py import (
    encrypt,
    combine_decryption_shares,
    decrypt_with_shared_secret,
    Keypair,
    ExternalValidator,
    Transcript,
    Dkg,
    AggregatedTranscript,
    Ciphertext,
    DkgPublicKey,
)

tau = 1
security_threshold = 3
shares_num = 4
validator_keypairs = [Keypair.random() for _ in range(0, shares_num)]
validators = [
    ExternalValidator(f"validator-{i}", keypair.public_key)
    for i, keypair in enumerate(validator_keypairs)
]

# Each validator holds their own DKG instance and generates a transcript every
# validator, including themselves
messages = []
for sender in validators:
    dkg = Dkg(
        tau=tau,
        shares_num=shares_num,
        security_threshold=security_threshold,
        validators=validators,
        me=sender,
    )
    messages.append((sender, dkg.generate_transcript()))

# Now that every validator holds a dkg instance and a transcript for every other validator,
# every validator can aggregate the transcripts
me = validators[0]
dkg = Dkg(
    tau=tau,
    shares_num=shares_num,
    security_threshold=security_threshold,
    validators=validators,
    me=me,
)
pvss_aggregated = dkg.aggregate_transcripts(messages)
assert pvss_aggregated.validate(dkg)

# Server can persist transcripts and the aggregated transcript
transcripts_ser = [bytes(transcript) for _, transcript in messages]
_transcripts_deser = [Transcript.from_bytes(t) for t in transcripts_ser]
agg_transcript_ser = bytes(pvss_aggregated)

# In the meantime, the client creates a ciphertext and decryption request
msg = "abc".encode()
aad = "my-aad".encode()
ciphertext = encrypt(msg, aad, dkg.final_key)

# The client can serialize/deserialize ciphertext for transport
ciphertext_ser = bytes(ciphertext)

# Having aggregated the transcripts, the validators can now create decryption shares
decryption_shares = []
for validator, validator_keypair in zip(validators, validator_keypairs):
    dkg = Dkg(
        tau=tau,
        shares_num=shares_num,
        security_threshold=security_threshold,
        validators=validators,
        me=validator,
    )
    # Assume the aggregated transcript is obtained through deserialization from a side-channel
    agg_transcript_deser = AggregatedTranscript.from_bytes(agg_transcript_ser)
    agg_transcript_deser.validate(dkg)

    # The ciphertext is obtained from the client
    ciphertext_deser = Ciphertext.from_bytes(ciphertext_ser)

    # Create a decryption share for the ciphertext
    decryption_share = agg_transcript_deser.create_decryption_share(
        dkg, ciphertext, aad, validator_keypair
    )
    decryption_shares.append(decryption_share)

# Now, the decryption share can be used to decrypt the ciphertext
# This part is in the client API

shared_secret = combine_decryption_shares(decryption_shares)

plaintext = decrypt_with_shared_secret(ciphertext, aad, shared_secret, dkg.public_params)
assert bytes(plaintext) == msg

# Other serializable objects

# Keypair
keypair = Keypair.random()
keypair_ser = bytes(keypair)
keypair_deser = Keypair.from_bytes(keypair_ser)

# DKG public key
dkg_pk = dkg.final_key
dkg_pk_ser = bytes(dkg_pk)
dkg_pk_deser = DkgPublicKey.from_bytes(dkg_pk_ser)

# Other utilities

bytes_len = Keypair.secure_randomness_size()
secure_randomness = os.urandom(bytes_len)
keypair = Keypair.from_secure_randomness(secure_randomness)
