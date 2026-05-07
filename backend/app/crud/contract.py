from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Contract
from typing import Optional, List
from datetime import datetime

def create_contract(
    db: Session,
    name: str,
    amount: float,
    file_path: str,
    file_type: str,
    department: str,
    uploader_id: int,
    uploader_name: str,
    party_a: str,
    party_b: str,
    signing_date: datetime,
    execution_start_date: datetime,
    execution_end_date: datetime
) -> Contract:
    db_contract = Contract(
        name=name,
        amount=amount,
        file_path=file_path,
        file_type=file_type,
        department=department,
        uploader_id=uploader_id,
        uploader_name=uploader_name,
        party_a=party_a,
        party_b=party_b,
        signing_date=signing_date,
        execution_start_date=execution_start_date,
        execution_end_date=execution_end_date,
        download_count=0
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def get_contract_by_id(db: Session, contract_id: int) -> Optional[Contract]:
    return db.query(Contract).filter(Contract.id == contract_id).first()

def get_contracts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    department: Optional[str] = None
) -> List[Contract]:
    query = db.query(Contract)
    if department:
        query = query.filter(Contract.department == department)
    return query.offset(skip).limit(limit).all()

def update_contract(
    db: Session,
    contract_id: int,
    name: Optional[str] = None,
    amount: Optional[float] = None,
    department: Optional[str] = None,
    party_a: Optional[str] = None,
    party_b: Optional[str] = None,
    signing_date: Optional[datetime] = None,
    execution_start_date: Optional[datetime] = None,
    execution_end_date: Optional[datetime] = None
) -> Optional[Contract]:
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        return None

    if name is not None:
        contract.name = name
    if amount is not None:
        contract.amount = amount
    if department is not None:
        contract.department = department
    if party_a is not None:
        contract.party_a = party_a
    if party_b is not None:
        contract.party_b = party_b
    if signing_date is not None:
        contract.signing_date = signing_date
    if execution_start_date is not None:
        contract.execution_start_date = execution_start_date
    if execution_end_date is not None:
        contract.execution_end_date = execution_end_date

    db.commit()
    db.refresh(contract)
    return contract

def delete_contract(db: Session, contract_id: int) -> bool:
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        return False
    db.delete(contract)
    db.commit()
    return True

def get_dashboard_stats(db: Session, department: Optional[str] = None, year: Optional[int] = None):
    """获取仪表板统计数据，如果指定科室则只返回该科室的数据"""
    query = db.query(Contract)

    # 按年份筛选（根据签订日期）
    if year:
        query = query.filter(func.extract('year', Contract.signing_date) == year)

    if department:
        # 只统计指定科室的数据
        dept_query = query.filter(Contract.department == department)
        total_contracts = dept_query.count()
        total_amount = db.query(func.sum(Contract.amount)).filter(
            Contract.department == department
        )
        if year:
            total_amount = total_amount.filter(func.extract('year', Contract.signing_date) == year)
        total_amount = total_amount.scalar() or 0

        department_stats = {
            department: {
                "count": total_contracts,
                "amount": float(total_amount)
            }
        }
    else:
        # 统计所有科室数据（管理员）
        total_contracts = query.count()
        amount_query = db.query(func.sum(Contract.amount))
        if year:
            amount_query = amount_query.filter(func.extract('year', Contract.signing_date) == year)
        total_amount = amount_query.scalar() or 0

        # 获取所有不同的科室
        departments = db.query(Contract.department).distinct().all()
        department_stats = {}
        for (dept,) in departments:
            if dept:
                dept_query = query.filter(Contract.department == dept)
                count = dept_query.count()
                amount_query = db.query(func.sum(Contract.amount)).filter(Contract.department == dept)
                if year:
                    amount_query = amount_query.filter(func.extract('year', Contract.signing_date) == year)
                amount = amount_query.scalar() or 0
                department_stats[dept] = {
                    "count": count,
                    "amount": float(amount)
                }

    return {
        "total_contracts": total_contracts,
        "total_amount": float(total_amount),
        "department_stats": department_stats
    }

def increment_download_count(db: Session, contract_id: int) -> Optional[Contract]:
    """增加合同下载次数"""
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        return None

    contract.download_count += 1
    db.commit()
    db.refresh(contract)
    return contract
