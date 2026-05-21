from enum import Enum

class Department(str, Enum):
    PRODUCT = "product"
    ENGINEERING ="engineering"
    SALES = "sales"
    HR = "hr"