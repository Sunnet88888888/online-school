from app.presentation.api.schemas.content import (
    CourseListItemResponse,
    CourseResponse,
    CourseStructureResponse,
    LectureResponse,
    LectureStructureResponse,
    ModuleStructureResponse,
    SectionStructureResponse,
    TaskStructureResponse,
    CodeTaskStructureResponse,
    AnswerOptionDetailsResponse,
    QuestionDetailsResponse,
    TaskDetailsResponse,
    CodeTaskDetailsResponse,
)

from app.presentation.api.schemas.courses import CreateCourseRequest, UpdateCourseRequest
from app.presentation.api.schemas.errors import ErrorResponse
from app.presentation.api.schemas.lectures import CreateLectureRequest, UpdateLectureRequest



from app.presentation.api.schemas.modules import (
    CreateModuleRequest,
    ModuleResponse,
    UpdateModuleRequest,
)

from app.presentation.api.schemas.sections import (
    CreateSectionRequest,
    SectionResponse,
    UpdateSectionRequest,
)


from app.presentation.api.schemas.auth import(
    RegisterUserRequest,
    RegisteredUserResponse,
    LoginRequest,
    TokenResponse,
    CurrentUserResponse,
    
    
)



from app.presentation.api.schemas.questions import (
    AnswerOptionResponse,
    CreateAnswerOptionRequest,
    CreateQuestionRequest,
    QuestionResponse,
    UpdateAnswerOptionRequest,
    UpdateQuestionRequest,
)


from app.presentation.api.schemas.question_attempts import (
    QuestionAttemptResultResponse,
    StartQuestionAttemptResponse,
    SubmitQuestionAnswerRequest,
)


from app.presentation.api.schemas.tasks import (
    CreateTaskRequest,
    TaskResponse,
    UpdateTaskRequest,
)
from app.presentation.api.schemas.code_tasks import (
    CodeTaskResponse,
    CreateCodeTaskRequest,
    UpdateCodeTaskRequest,
)
from app.presentation.api.schemas.test_cases import (
    CreateTestCaseRequest,
    TestCaseResponse,
    UpdateTestCaseRequest,
)



from app.presentation.api.schemas.task_attempts import (
    SubmitTaskAnswerRequest,
    TaskAttemptResponse,
)
from app.presentation.api.schemas.code_submissions import (
    CodeSubmissionResponse,
    SubmitCodeSubmissionRequest,
)

from app.presentation.api.schemas.course_publication import (
    CoursePublicationErrorResponse,
    CoursePublicationIssueResponse,
    CoursePublicationReadinessResponse,
)




from app.presentation.api.schemas.catalog import (
    CourseCatalogCardResponse,
    CourseCatalogCountersResponse,
    CourseCatalogItemResponse,
    CourseCatalogModulePreviewResponse,
    CourseCatalogSectionPreviewResponse,
)



from app.presentation.api.schemas.profile import(
    UserProfileResponse,
    UpdateMyProfileRequest,
)



from app.presentation.api.schemas.student_analytics import(
    StudentCourseAnalyticsResponse,
    StudentModuleAnalyticsResponse,
    StudentWeakCodeTaskResponse,
    StudentWeakQuestionResponse,
    StudentWeakTaskResponse,
)





from app.presentation.api.schemas.author_course_analytics import(
    AuthorCourseAnalyticsResponse,
    AuthorModuleAnalyticsResponse,
    DifficultTaskAnalyticsResponse,
    DifficultQuestionAnalyticsResponse,
    ProblematicCodeTaskAnalyticsResponse,
)



from app.presentation.api.schemas.course_reviews import (
    UpsertCourseReviewRequest,
    CourseReviewResponse,
    
)







__all__ = [
    "CourseListItemResponse",
    "CourseResponse",
    "CourseStructureResponse",
    "LectureResponse",
    "LectureStructureResponse",
    "ModuleStructureResponse",
    "SectionStructureResponse",
    "CreateCourseRequest",
    "UpdateCourseRequest",
    "CreateModuleRequest",
    "UpdateModuleRequest",
    "ModuleResponse",
    "CreateSectionRequest",
    "UpdateSectionRequest",
    "SectionResponse",
    "CreateLectureRequest",
    "UpdateLectureRequest",
    "ErrorResponse",
    "RegisterUserRequest",
    "RegisteredUserResponse",
    "LoginRequest",
    "TokenResponse",
    "CurrentUserResponse",
    'CreateQuestionRequest',
    'UpdateQuestionRequest',
    'QuestionResponse',
    'CreateAnswerOptionRequest',
    'UpdateAnswerOptionRequest',
    'AnswerOptionResponse',
    'StartQuestionAttemptResponse',
    'SubmitQuestionAnswerRequest',
    'QuestionAttemptResultResponse',
    'CreateCodeTaskRequest',
    'UpdateCodeTaskRequest',
    'CodeTaskResponse',
    'CreateTestCaseRequest',
    'UpdateTestCaseRequest',
    'TestCaseResponse',
    'CreateTaskRequest',
    'UpdateTaskRequest',
    'TaskResponse',
    'TaskStructureResponse',
    'CodeTaskStructureResponse',
    'SubmitTaskAnswerRequest',
    'TaskAttemptResponse',
    'SubmitCodeSubmissionRequest',
    'CodeSubmissionResponse',
    'AnswerOptionDetailsResponse',
    'QuestionDetailsResponse',  
    'TaskDetailsResponse',
    'CodeTaskDetailsResponse',
    'CoursePublicationIssueResponse',
    'CoursePublicationReadinessResponse',
    'CoursePublicationErrorResponse',
    'CourseCatalogCountersResponse',
    'CourseCatalogItemResponse',
    'CourseCatalogSectionPreviewResponse',
    'CourseCatalogModulePreviewResponse',
    'CourseCatalogCardResponse',
    'UserProfileResponse',
    'UpdateMyProfileRequest',
    'StudentCourseAnalyticsResponse',
    'StudentModuleAnalyticsResponse',
    'StudentWeakCodeTaskResponse',
    'StudentWeakQuestionResponse',
    'StudentWeakTaskResponse',
    'AuthorCourseAnalyticsResponse',
    'AuthorModuleAnalyticsResponse',
    'DifficultTaskAnalyticsResponse',
    'DifficultQuestionAnalyticsResponse',
    'ProblematicCodeTaskAnalyticsResponse',
    
]