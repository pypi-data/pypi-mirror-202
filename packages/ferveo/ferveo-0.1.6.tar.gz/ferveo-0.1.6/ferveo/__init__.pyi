from typing import Sequence


class Keypair:
    @staticmethod
    def random() -> Keypair:
        ...

    @staticmethod
    def from_secure_randomness(data: bytes) -> Keypair:
        ...

    @staticmethod
    def from_bytes(data: bytes) -> Keypair:
        ...

    def __bytes__(self) -> bytes:
        ...

    public_key: PublicKey


class PublicKey:
    @staticmethod
    def from_bytes(data: bytes) -> PublicKey:
        ...

    def __bytes__(self) -> bytes:
        ...


class ExternalValidator:

    def __init__(self, address: str, public_key: PublicKey):
        ...

    address: str

    public_key: PublicKey


class Transcript:
    @staticmethod
    def from_bytes(data: bytes) -> Transcript:
        ...

    def __bytes__(self) -> bytes:
        ...


class DkgPublicKey:
    @staticmethod
    def from_bytes(data: bytes) -> DkgPublicKey:
        ...

    def __bytes__(self) -> bytes:
        ...


class ExternalValidatorMessage:
    ...


class Dkg:

    def __init__(
            self,
            tau: int,
            shares_num: int,
            security_threshold: int,
            validators: Sequence[ExternalValidator],
            me: ExternalValidator,
    ):
        ...

    final_key: DkgPublicKey

    public_params: DkgPublicParameters

    def generate_transcript(self) -> Transcript:
        ...

    def aggregate_transcripts(self, transcripts: Sequence[(ExternalValidator, Transcript)]) -> Transcript:
        ...


class Ciphertext:
    @staticmethod
    def from_bytes(data: bytes) -> Ciphertext:
        ...

    def __bytes__(self) -> bytes:
        ...


class UnblindingKey:
    ...


class DecryptionShare:
    @staticmethod
    def from_bytes(data: bytes) -> DecryptionShare:
        ...

    def __bytes__(self) -> bytes:
        ...


class DkgPublicParameters:
    @staticmethod
    def from_bytes(data: bytes) -> DkgPublicParameters:
        ...

    def __bytes__(self) -> bytes:
        ...


class AggregatedTranscript:

    def create_decryption_share(
            self,
            dkg: Dkg,
            ciphertext: Ciphertext,
            aad: bytes,
            unblinding_key: UnblindingKey
    ) -> DecryptionShare:
        ...

    def validate(self, dkg: Dkg) -> bool:
        ...

    @staticmethod
    def from_bytes(data: bytes) -> AggregatedTranscript:
        ...

    def __bytes__(self) -> bytes:
        ...
