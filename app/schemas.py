from pydantic import BaseModel


class TestResponse(BaseModel):
    prediction: float


class HealthResponse(BaseModel):
    status: bool


class TestDataInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float

    def get_array(self):
        return [
            [
                self.feature1,
                self.feature2,
                self.feature3,
                self.feature4,
                self.feature5,
            ]
        ]
