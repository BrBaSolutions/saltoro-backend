class Endpoints:
    class Authentication:
        BASE = "/api/v1" + "/user-auth"
        SIGNUP = BASE + "/signup"
        LOGIN = BASE + "/login"
        REFRESH = BASE + "/refresh-token"

    class User:
        BASE = "/api/v1"
        USER = BASE + "/user"
