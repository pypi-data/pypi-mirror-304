from pydantic import BaseModel, Field
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class InputPayload(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the requestor")
    input: str = Field(..., min_length=1, description="The input string to be converted to uppercase")


class ValidationHandler:
    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={"detail": "Input cannot be empty. Please provide a valid string."},
        )
    
class LogicProcessor:
    @staticmethod
    def process_uppercase_data(InputPayload):
        ValidationHandler.validation_exception_handler(InputPayload, exc= RequestValidationError)
        upper_input = InputPayload.input.upper()
        response = {
            "requestor_name": InputPayload.name,
            "upper_input": upper_input
        }
        return response
    
obj = InputPayload(name='sonal',input='sonal')
response = LogicProcessor.process_uppercase_data(obj)
print('response',response)
