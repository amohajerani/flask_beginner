'''
Users collection: 
- _id
- username
- email

s3:
    thegagali
        username1
            resume.csv
            ...

Files collection
- _id
- filepath
- username
- private


'''
email = 'amir'


def create_username(email):
    username = email.split("@")[0]
    username = ''.join(e for e in username if e.isalnum())
    num = 0
    while Users.find_one({'username': username}):
        username = username+str(num)
        num += 1
    return username


def get_username(email):
    user_obj = Users.find_one({'email': email})
    if not user_obj:
        username = create_username(email)
        Users.insert({'email': email, 'username': username})
    else:
        username = user_obj['username']
    return username


def file_exists(username, filename):
    filepath = username+'/'+filename
    res = Files.find_one({'filepath': filepath})
    if res:
        return True
    else:
        return False


def insert_file_doc(username, filename, private):
    filepath = username+'/'+filename
    Files.insert_one(
        {'filepath': filepath, 'private': private, 'username': username})
