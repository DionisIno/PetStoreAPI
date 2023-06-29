from generator.generator import generated_user

headers = [("Content-Type", "application/json"),
           ("Transfer-Encoding", "chunked"),
           ("Connection", "keep-alive"),
           ("Access-Control-Allow-Origin", "*")]

user_data = next(generated_user())
user_json = {
    "id": user_data.id,
    "username": user_data.username,
    "firstName": user_data.firstName,
    "lastName": user_data.lastName,
    "email": user_data.email,
    "password": user_data.password,
    "phone": user_data.phone,
    "userStatus": user_data.userStatus,
}
user_json_without_id = {
    "username": user_data.username,
    "firstName": user_data.firstName,
    "lastName": user_data.lastName,
    "email": user_data.email,
    "password": user_data.password,
    "phone": user_data.phone,
    "userStatus": user_data.userStatus,
}
