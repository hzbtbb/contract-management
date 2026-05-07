from app.core.database import SessionLocal, Base, engine
from app.crud.user import create_user, get_user_by_username

def init_db():
    """初始化数据库，创建默认管理员账号和科室账号"""
    # 先创建所有表
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建成功")

    db = SessionLocal()

    try:
        # 创建管理员账号
        if not get_user_by_username(db, "admin"):
            create_user(db, username="admin", password="admin123", role="admin")
            print("✓ 管理员账号创建成功: admin / admin123")

        # 创建五个科室账号
        departments = [
            ("ground", "地面科"),
            ("command", "指挥科"),
            ("operation", "作业科"),
            ("office", "办公室"),
            ("support", "保障科")
        ]

        for username, dept_name in departments:
            if not get_user_by_username(db, username):
                create_user(db, username=username, password="123456", department=dept_name, role="user")
                print(f"✓ {dept_name}账号创建成功: {username} / 123456")

        print("\n数据库初始化完成！")
        print("\n默认账号信息：")
        print("管理员: admin / admin123")
        print("地面科: ground / 123456")
        print("指挥科: command / 123456")
        print("作业科: operation / 123456")
        print("办公室: office / 123456")
        print("保障科: support / 123456")

    finally:
        db.close()

if __name__ == "__main__":
    init_db()
