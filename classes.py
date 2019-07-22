class User():
    def __init__(self, userid, username, first_name, last_name):
        self.userid = userid
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class Event():
    def __init__(self, title, time, place, num):
        self.title = title
        self.time = time
        self.place = place
        self.num = num
        self.members = []
        self.is_announced = 0

    def add_member(self, user):
        self.members.append(user)

    def get_description(self):
        return 'Название: ' + self.title + '\nВремя:' + self.time + '\nМесто: ' + self.place +\
               '\nМаксимальное число участников: ' + str(self.num)

    def get_usernames(self):
        res = []
        for user in self.members:
            res.append(user.username)
        return res

    def contains_user(self, userid):
        for user in self.members:
            if userid == user.userid:
                return True
        return False
