from typing import Union, List, Dict, Any
from pydantic import Field, BaseModel, field_validator
from pydantic.json_schema import SkipJsonSchema
from vcdm.models.proof import DataIntegrityProof
from vcdm.validations import valid_datetime_string, valid_uri, valid_url


class NameField(BaseModel, extra="forbid"):
    value: str = Field(None, alias="@value")
    language: str = Field(None, alias="@language")
    direction: str = Field(None, alias="@direction")


class DescriptionField(BaseModel, extra="forbid"):
    value: str = Field(None, alias="@value")
    language: str = Field(None, alias="@language")
    direction: str = Field(None, alias="@direction")


class BaseModel(BaseModel, extra="allow"):
    type: Union[str, List[str]] = Field(None)
    id: SkipJsonSchema[str] = Field(None)
    name: SkipJsonSchema[Union[str, NameField, List[NameField]]] = Field(None)
    description: SkipJsonSchema[
        Union[str, DescriptionField, List[DescriptionField]]
    ] = Field(None)

    @field_validator("id")
    @classmethod
    def validate_credential_id(cls, value):
        assert valid_uri(value)
        return value

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        return super().model_dump(by_alias=True, exclude_none=True, **kwargs)


class Issuer(BaseModel):
    id: SkipJsonSchema[str] = Field()


class RelatedResource(BaseModel):
    id: SkipJsonSchema[str] = Field()
    digestSRI: str = Field(None)
    digestMultibase: str = Field(None)


class CredentialSubject(BaseModel):
    type: SkipJsonSchema[Union[str, List[str]]] = Field(None)


class CredentialSchema(BaseModel):
    id: Union[str, List[str]] = Field()
    type: Union[str, List[str]] = Field()


class CredentialStatus(BaseModel):
    id: str = Field(None)
    type: Union[str, List[str]] = Field()
    statusPurpose: str = Field(None)
    statusListIndex: str = Field(None)
    statusListCredential: str = Field(None)


class TermsOfUse(BaseModel):
    type: Union[str, List[str]] = Field()


class RefreshService(BaseModel):
    type: Union[str, List[str]] = Field()


class Evidence(BaseModel):
    type: Union[str, List[str]] = Field()


class RenderMethod(BaseModel):
    type: Union[str, List[str]] = Field()


class Credential(BaseModel):
    context: List[Union[str, dict]] = Field(alias="@context")
    type: Union[str, List[str]] = Field()
    issuer: Union[Issuer, str] = Field()

    validFrom: SkipJsonSchema[str] = Field(None)
    validUntil: SkipJsonSchema[str] = Field(None)
    issuanceDate: SkipJsonSchema[str] = Field(None)
    expirationDate: SkipJsonSchema[str] = Field(None)

    credentialSubject: Union[List[CredentialSubject], CredentialSubject] = Field()
    credentialStatus: SkipJsonSchema[
        Union[List[CredentialStatus], CredentialStatus]
    ] = Field(None)
    credentialSchema: SkipJsonSchema[
        Union[List[CredentialSchema], CredentialSchema]
    ] = Field(None)

    termsOfUse: SkipJsonSchema[Union[List[TermsOfUse], TermsOfUse]] = Field(None)
    refreshService: SkipJsonSchema[Union[List[RefreshService], RefreshService]] = Field(
        None
    )
    evidence: SkipJsonSchema[Union[List[Evidence], Evidence]] = Field(None)
    renderMethod: SkipJsonSchema[Union[List[RenderMethod], RenderMethod]] = Field(None)
    relatedResource: SkipJsonSchema[Union[List[RelatedResource], RelatedResource]] = (
        Field(None)
    )
    proof: Union[List[DataIntegrityProof], DataIntegrityProof] = Field(None)

    @field_validator("context")
    @classmethod
    def validate_context(cls, value):
        assert value[0] in [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/ns/credentials/v2",
        ]
        for item in value[1:]:
            if isinstance(item, str):
                assert valid_url(item)
        return value

    @field_validator("type")
    @classmethod
    def validate_credential_type(cls, value):
        asserted_value = value if isinstance(value, list) else [value]
        assert "VerifiableCredential" in asserted_value
        return value

    @field_validator("issuer")
    @classmethod
    def validate_issuer(cls, value):
        if isinstance(value, str):
            value = value if isinstance(value, str) else value["id"]
            assert valid_uri(value)
            return value

    @field_validator("issuanceDate")
    @classmethod
    def validate_issuance_date(cls, value):
        assert valid_datetime_string(value)
        return value

    @field_validator("expirationDate")
    @classmethod
    def validate_expiration_date(cls, value):
        assert valid_datetime_string(value)
        return value

    @field_validator("validFrom")
    @classmethod
    def validate_valid_from_date(cls, value):
        assert valid_datetime_string(value)
        return value

    @field_validator("validUntil")
    @classmethod
    def validate_valid_until_date(cls, value):
        assert valid_datetime_string(value)
        return value

    @field_validator("credentialSubject")
    @classmethod
    def validate_credential_subject(cls, value):
        asserted_value = value if isinstance(value, list) else [value]
        for subject in asserted_value:
            assert bool(subject.model_dump())
        return value

    @field_validator("relatedResource")
    @classmethod
    def validate_related_ressource(cls, value):
        asserted_value = value if isinstance(value, list) else [value]
        for ressource in asserted_value:
            assert valid_uri(ressource.id)
            assert ressource.digestSRI or ressource.digestMultibase
        return value

    # def add_validity_period():
    #     validFrom = str(datetime.now().isoformat("T", "seconds"))
    #     validUntil = str(datetime.now().isoformat("T", "seconds"))
