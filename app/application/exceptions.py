class ApplicationError(Exception):
    """Base exception for application-layer errors"""


class CourseNotFoundError(ApplicationError):
    pass

class LectureNotFounError(ApplicationError):
    pass

class ModuleNotFoundError(ApplicationError):
    pass
