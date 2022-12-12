from fastapiframework.models.camel_case_model import CamelCaseModel


class DataRequestPayload(CamelCaseModel):
    correlation_id: str
    data: CamelCaseModel
