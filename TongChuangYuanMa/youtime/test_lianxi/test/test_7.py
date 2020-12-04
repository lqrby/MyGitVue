class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

if __name__ == "__main__":
    s = Student()
    s.score = 600 # OK，实际转化为s.set_score(60)
    s.score # OK，实际转化为s.get_score()
    print(s.score)