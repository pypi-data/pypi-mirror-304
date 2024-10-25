class Course:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"{self.name} [{self.duration} horas] ({self.link})"


courses = [
    Course("Intro a terminal de linux con parrot", 15, "https://hack4u.io/cursos/intro-a-linux/"),
    Course("Personalizar el entorno Parrot", 3, "https://hack4u.io/cursos/personalizando-parrot/"),
    Course("Intro al hacking etico", 53, "https://hack4u.io/cursos/intro-hacking-etico/")
]

def list_couses():
    #print(courses)
    for couse in courses:
        print(couse)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course

    return None



