from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CourseBaseResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str


class CourseListItemResponse(CourseBaseResponse):
    pass


class CourseResponse(CourseBaseResponse):
    pass


class LectureBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    position: int


class LectureResponse(LectureBaseResponse):
    content: str
    section_id: UUID


class LectureStructureResponse(LectureBaseResponse):
    pass


class SectionBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    position: int


class SectionStructureResponse(SectionBaseResponse):
    question_ids: list[UUID]
    task_ids: list[UUID]
    lectures: list[LectureStructureResponse]
    


class ModuleBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    position: int


class ModuleStructureResponse(ModuleBaseResponse):
    sections: list[SectionStructureResponse]


class CourseStructureResponse(CourseBaseResponse):
    modules: list[ModuleStructureResponse]



class SectionStructureResponse(SectionBaseResponse):
    question_ids: list[UUID]
    task_ids: list[UUID]
    code_task_ids: list[UUID]
    tasks: list[TaskStructureResponse]
    code_tasks: list[CodeTaskStructureResponse]
    lectures: list[LectureStructureResponse]

    
    
class TaskStructureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    position: int


class CodeTaskStructureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    position: int
    language: str