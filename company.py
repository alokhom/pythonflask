from employee import Employee

class Company:
    def __init__(self):
        self.employees = []
    
    def add_employee(self, new_employee):
        self.employees.append(new_employee)

    def display(self):
        print('crrent employees:')
        for i in self.employees:
            print(i.name)

    def pay_employees(self):
        for i in self.employees:
            print(f"{i.name} is paid ${i.calculate_paycheck():,.2f}")

    # def list_employees(self):
    #     for employee in self.employees:
    #         employee.display()

def main():
    my_company = Company()

    emp1 = Employee('alok',20000)
    emp2 = Employee('Sarah',40000)
    my_company.add_employee(emp1)
    my_company.add_employee(emp2)

    # my_company.display()
    my_company.pay_employees()
    

main()