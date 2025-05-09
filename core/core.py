from datetime import datetime

class Stage:
    def __init__(self, name, planned_date, actual_date=None):
        self.name = name
        self.planned_date = planned_date
        self.actual_date = actual_date

    def __repr__(self):
        actual = self.actual_date.strftime('%Y-%m-%d') if self.actual_date else "---"
        return f"{self.name} | Planned: {self.planned_date.strftime('%Y-%m-%d')} | Done: {actual}"

class Project:
    def __init__(self, name, description=''):
        self.name = name
        self.description = description
        self.stages = []

    def add_stage(self, stage_name, planned_date):
        stage = Stage(stage_name, planned_date)
        self.stages.append(stage)

    def set_actual_date(self, stage_index, actual_date):
        if 0 <= stage_index < len(self.stages):
            self.stages[stage_index].actual_date = actual_date

class Office:
    def __init__(self, name):
        self.name = name
        self.projects = []

    def add_project(self, project_name, description=''):
        project = Project(project_name, description)
        self.projects.append(project)

offices = []

def input_date(prompt):
    while True:
        try:
            return datetime.strptime(input(prompt), "%Y-%m-%d")
        except ValueError:
            print("Date format must be yyyy-mm-dd.")

def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Create new office")
        print("2. View offices and projects")
        print("3. Exit")
        choice = input("Your choice: ")

        match choice:
            case '1':
                office_name = input("Office name: ")
                office = Office(office_name)
                offices.append(office)
                project_menu(office)
            case '2':
                list_offices()
            case '3':
                print("Exiting...")
                break
            case _:
                print("Invalid option.")

def project_menu(office):
    while True:
        print(f"\n--- Office: {office.name} ---")
        print("1. Add project")
        print("2. Add stage to project")
        print("3. Set actual date for stage")
        print("4. View projects")
        print("5. Back")
        choice = input("Your choice: ")

        match choice:
            case '1':
                name = input("Project name: ")
                desc = input("Project description (optional): ")
                office.add_project(name, desc)

            case '2':
                if not office.projects:
                    print("No projects found.")
                    continue
                list_projects(office)
                idx = int(input("Project number: ")) - 1
                if idx < 0 or idx >= len(office.projects):
                    print("Invalid project number.")
                    continue
                stage_name = input("Stage name: ")
                planned_date = input_date("Planned date (yyyy-mm-dd): ")
                office.projects[idx].add_stage(stage_name, planned_date)

            case '3':
                if not office.projects:
                    print("No projects available.")
                    continue
                list_projects(office)
                idx = int(input("Project number: ")) - 1
                if idx < 0 or idx >= len(office.projects):
                    print("Invalid project number.")
                    continue
                project = office.projects[idx]
                if not project.stages:
                    print("No stages available.")
                    continue
                for i, s in enumerate(project.stages):
                    print(f"{i+1}. {s}")
                sid = int(input("Stage number: ")) - 1
                if sid < 0 or sid >= len(project.stages):
                    print("Invalid stage number.")
                    continue
                actual_date = input_date("Actual date (yyyy-mm-dd): ")
                project.set_actual_date(sid, actual_date)

            case '4':
                list_projects(office, show_stages=True)

            case '5':
                break

            case _:
                print("Invalid option.")

def list_offices():
    if not offices:
        print("No offices found.")
        return
    for i, office in enumerate(offices):
        print(f"{i+1}. Office: {office.name} | Projects: {len(office.projects)}")
        for j, p in enumerate(office.projects):
            print(f"   {j+1}. {p.name} ({len(p.stages)} stages)")

def list_projects(office, show_stages=False):
    for i, p in enumerate(office.projects):
        print(f"{i+1}. {p.name}")
        if show_stages:
            for s in p.stages:
                print(f"     - {s}")

if __name__ == "__main__":
    main_menu()
