import asyncio
from uuid import UUID

from app.application.use_cases.code_submissions.complete_code_submission import CompleteCodeSubmissionUseCase
from app.application.use_cases.code_submissions.process_code_submission import (
    ProcessCodeSubmissionCommand,
    ProcessCodeSubmissionUseCase,
)
from app.domain.entities.code_task import CodeTaskLanguage
from app.infrastructure.database.database import SessionFactory
from app.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from app.infrastructure.execution.docker_code_execution_gateway import DockerCodeExecutionGateway
from app.infrastructure.execution.docker_runner import DockerRunner, DockerRunConfig
from app.infrastructure.execution.execution_profile_registry import (
    ExecutionProfile,
    ExecutionProfileRegistry,
)
from app.infrastructure.execution.python_submission_bundle_builder import PythonSubmissionBundleBuilder


async def main() -> None:
    submission_id = UUID('fee93325-57ca-4d95-aa51-145283b24df5')

    uow = SqlAlchemyUnitOfWork(session_factory=SessionFactory)
    execution_gateway = DockerCodeExecutionGateway(
        runner=DockerRunner(config=DockerRunConfig()),
        profile_registry=ExecutionProfileRegistry(
            profiles={
                CodeTaskLanguage.PYTHON: ExecutionProfile(
                    image='python:3.12-alpine',
                    bundle_builder=PythonSubmissionBundleBuilder(),
                )
            }
        ),
    )
    complete_use_case = CompleteCodeSubmissionUseCase(uow=uow)
    process_use_case = ProcessCodeSubmissionUseCase(
        uow=uow,
        execution_gateway=execution_gateway,
        complete_use_case=complete_use_case,
    )

    await process_use_case.execute(
        ProcessCodeSubmissionCommand(submission_id=submission_id)
    )


asyncio.run(main())