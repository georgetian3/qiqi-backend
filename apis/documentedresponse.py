from typing import List

from fastapi import status
from fastapi.responses import Response
from pydantic import BaseModel


class DocumentedResponse:
    def __init__(self, status_code, description, model=None):
        self.status_code = status_code
        self.description = description
        self.model = model
    def documentation(self):
        return {
            'description': self.description,
        }
    def response(self):
        return Response(
            status_code=self.status_code,
        )

class JSONDocumentedResponse(DocumentedResponse):
    def response(self, data: BaseModel | dict=None, exclude: List=[]):
        return Response(
            content=data if not self.model else data.json(exclude_none=True, exclude=set(exclude)),
            status_code=self.status_code,
            media_type='application/json',
        )
    

def create_documentation(*args):
    responses = list(args)
    documentation = {}
    documentation['status_code'] = responses[0].status_code
    documentation['response_description'] = responses[0].description
    if responses[0].model:
        documentation['response_model'] = responses[0].model
    documentation['responses'] = {}
    for response in responses[1:]:
        doc = response.documentation()
        if response.model:
            doc['model'] = response.model
        documentation['responses'][response.status_code] = doc
    return documentation

JDR = JSONDocumentedResponse
JDR204 = JDR(status.HTTP_204_NO_CONTENT, 'Success')
JDR400 = JDR(status.HTTP_400_BAD_REQUEST, 'Failed')
JDR403 = JDR(status.HTTP_403_FORBIDDEN, 'You do not have permission to perform this action.')
JDR404 = JDR(status.HTTP_404_NOT_FOUND,'Resource not found.')