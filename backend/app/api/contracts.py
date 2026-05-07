from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.schemas.contract import ContractResponse, ContractUpdate, DashboardStats
from app.crud import contract as crud_contract
from app.api.auth import get_current_user
from app.models.models import User

router = APIRouter()

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=ContractResponse)
async def upload_contract(
    name: str = Form(...),
    amount: float = Form(...),
    department: str = Form(...),
    party_a: str = Form(...),
    party_b: str = Form(...),
    signing_date: str = Form(...),
    execution_start_date: str = Form(...),
    execution_end_date: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传合同文件"""
    # 验证文件类型
    allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="不支持的文件类型，仅支持PDF和图片")

    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)

    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 解析日期
    try:
        sign_date = datetime.fromisoformat(signing_date.replace('Z', '+00:00'))
        exec_start = datetime.fromisoformat(execution_start_date.replace('Z', '+00:00'))
        exec_end = datetime.fromisoformat(execution_end_date.replace('Z', '+00:00'))
    except:
        raise HTTPException(status_code=400, detail="日期格式错误")

    # 创建数据库记录
    contract = crud_contract.create_contract(
        db=db,
        name=name,
        amount=amount,
        file_path=file_path,
        file_type=file_ext,
        department=department,
        uploader_id=current_user.id,
        uploader_name=current_user.username,
        party_a=party_a,
        party_b=party_b,
        signing_date=sign_date,
        execution_start_date=exec_start,
        execution_end_date=exec_end
    )

    return contract

@router.get("/", response_model=List[ContractResponse])
def get_contracts(
    skip: int = 0,
    limit: int = 100,
    department: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取合同列表"""
    # 如果不是管理员，只能查看自己科室的合同
    if current_user.role != "admin":
        department = current_user.department

    contracts = crud_contract.get_contracts(
        db=db,
        skip=skip,
        limit=limit,
        department=department
    )
    return contracts

@router.get("/{contract_id}", response_model=ContractResponse)
def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个合同详情"""
    contract = crud_contract.get_contract_by_id(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="合同不存在")

    # 权限检查
    if current_user.role != "admin" and contract.department != current_user.department:
        raise HTTPException(status_code=403, detail="无权访问此合同")

    return contract

@router.put("/{contract_id}", response_model=ContractResponse)
def update_contract(
    contract_id: int,
    contract_update: ContractUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新合同信息"""
    contract = crud_contract.get_contract_by_id(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="合同不存在")

    # 权限检查
    if current_user.role != "admin" and contract.uploader_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此合同")

    updated_contract = crud_contract.update_contract(
        db=db,
        contract_id=contract_id,
        name=contract_update.name,
        amount=contract_update.amount,
        department=contract_update.department,
        party_a=contract_update.party_a,
        party_b=contract_update.party_b,
        signing_date=contract_update.signing_date,
        execution_start_date=contract_update.execution_start_date,
        execution_end_date=contract_update.execution_end_date
    )

    return updated_contract

@router.delete("/{contract_id}")
def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除合同"""
    contract = crud_contract.get_contract_by_id(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="合同不存在")

    # 权限检查
    if current_user.role != "admin" and contract.uploader_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此合同")

    # 删除文件
    if os.path.exists(contract.file_path):
        os.remove(contract.file_path)

    # 删除数据库记录
    crud_contract.delete_contract(db, contract_id)

    return {"message": "合同已删除"}

@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取仪表板统计数据"""
    # 如果不是管理员，只返回本科室的统计数据
    department = None if current_user.role == "admin" else current_user.department
    stats = crud_contract.get_dashboard_stats(db, department=department, year=year)
    return stats

@router.get("/{contract_id}/download")
def download_contract_file(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """下载合同文件"""
    contract = crud_contract.get_contract_by_id(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="合同不存在")

    # 权限检查
    if current_user.role != "admin" and contract.department != current_user.department:
        raise HTTPException(status_code=403, detail="无权下载此合同")

    # 检查文件是否存在
    if not os.path.exists(contract.file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    # 增加下载次数
    crud_contract.increment_download_count(db, contract_id)

    # 返回文件
    return FileResponse(
        path=contract.file_path,
        filename=os.path.basename(contract.file_path),
        media_type='application/octet-stream'
    )

@router.post("/{contract_id}/download")
def download_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """记录合同下载并增加下载次数"""
    contract = crud_contract.get_contract_by_id(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="合同不存在")

    # 权限检查
    if current_user.role != "admin" and contract.department != current_user.department:
        raise HTTPException(status_code=403, detail="无权下载此合同")

    # 增加下载次数
    crud_contract.increment_download_count(db, contract_id)

    return {"message": "下载记录成功", "download_count": contract.download_count + 1}
