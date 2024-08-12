from app.models import User

def add_user(data):
    """添加用户"""
    new_user = User(
        UserID=data['UserID'],
        level=data['level'],
        exp=data['exp'],
        RodName=data['RodName'],
        BaitNumber=data['BaitNumber'],
        GMCNumber=data['GMCNumber'],
        Fishername=data['Fishername'],
        baitNumber=data['baitNumber']
    )
    new_user.save()
    return new_user

def get_user(user_id):
    """通过 UserID 获取用户"""
    return User.objects(UserID=user_id).first()

def update_user(user_id, data):
    """更新用户信息"""
    user = User.objects(UserID=user_id).first()
    if user:
        user.update(**data)
        return user.reload()
    return None

def delete_user(user_id):
    """删除用户"""
    user = User.objects(UserID=user_id).first()
    if user:
        user.delete()
        return True
    return False
