from sqlalchemy.orm import Session

from db.schemas import Income
from models.income_models import IncomeAdd

class IncomeRepository:
    def __init__(self, session:Session) -> None:
        self.session = session
        
    def add(self, income_add:IncomeAdd)->Income:
        new_income = Income(**income_add.model_dump())
        self.session.add(new_income)
        self.session.commit()
        self.session.refresh(new_income)
        return new_income
        
        
        