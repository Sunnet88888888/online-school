from dataclasses import dataclass, field

from uuid import UUID

from app.domain.entities.question_attempt import QuestionAttempt

from app.domain.entities.section import Section
from app.domain.exceptions import InvalidProgressError

@dataclass(slots=True)
class Progress:
    id: UUID
    student_id: UUID
    course_id: UUID
    completed_question_ids: list[UUID] = field(default_factory=list)
    completed_section_ids: list[UUID] = field(default_factory=list)
    
    
    def __post_init__(self) -> None:
        self._validate()
        
    def _validate(self) -> None:
        if len(self.completed_question_ids) != len(set(self.completed_question_ids)):
            raise InvalidProgressError("Progress cannot contain duplicate completed questions.")
        if len(self.completed_section_ids) != len(set(self.completed_section_ids)):
            raise InvalidProgressError("Progress cannot contain duplicate completed sections.")
        
    def has_completed_question(self, question_id: UUID) -> bool:
        return question_id in self.completed_question_ids
    
    def has_completed_section(self, section_id: UUID) -> bool:
        return section_id in self.completed_section_ids
    
    def mark_question_completed(self, question_id: UUID) -> None:
        if question_id not in self.completed_question_ids:
            self.completed_question_ids.append(question_id)
            
    def mark_section_completed(self, section_id: UUID) -> None:
        if section_id not in self.completed_section_ids:
            self.completed_section_ids.append(section_id)
            
            
            
    def apply_correct_attempt(self, attempt: QuestionAttempt) -> bool:
        
        if attempt.student_id != self.student_id:
            raise InvalidProgressError('Question attempt does not belong to this student.')
        
        if not attempt.is_correct():
            return False
        
        
        already_completed = self.has_completed_question(attempt.question_id)
        self.mark_question_completed(attempt.question_id)
        
        return not already_completed
    
    
    
    def sync_section_completion(self, section: Section) -> bool:
        if not section.is_completed_by(self.completed_question_ids):
            return False
        
        already_completed = self.has_completed_section(section.id)
        self.mark_section_completed(section.id)
        return not already_completed
    
    
    def completed_sections_count(self) -> int:
        return len(self.completed_section_ids)
    
    def course_completion_ration(self, total_sections_count: int) -> float:
        if total_sections_count < 1:
            return 0.0
        return min(1.0 , len(self.completed_section_ids) / total_sections_count)
    
    def is_course_completed(self, total_sections_count: int) -> bool:
        return total_sections_count > 0 and len(self.completed_section_ids) >= total_sections_count