import argparse


class Person:
    def __init__(self, firstname='david', lastname='saul', age=250, country='niger', city='Lagos'):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.country = country
        self.city = city
        self.skills = []

    def person_info(self):
        print(f'{self.firstname} {self.lastname} is {self.age} years old. He lives in {self.city}, {self.country}')

    def add_skills(self, skill):
        self.skills.append(skill)

    @classmethod
    def from_input(cls):
        firstname = input("Enter first name: ")
        lastname = input("Enter last name: ")
        age = int(input("Enter age: "))
        country = input("Enter country: ")
        city = input("Enter city: ")
        print("\n")

        return cls(firstname, lastname, age, country, city)


def main():
    parser = argparse.ArgumentParser(description="To operate class")

    subparsers = parser.add_subparsers(dest="command")

    # -------default class-------
    subparsers.add_parser("def", help="default class values")

    # -------user class_inp------
    subparsers.add_parser("inp", help="user definded inputs")

    args = parser.parse_args()

    if args.command == "def":
        p = Person()
        return p.person_info()
    elif args.command == "inp":
        p = Person.from_input()
        return p.person_info()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
