from Animal_class import *
from Rabbit_class import *
from Bush_class import *
from Wolf_class import *

class Animal_factory():

    
    @staticmethod
    def get_new_Rabbit():
        return Rabbit()


    @staticmethod
    def get_new_Bush():
        return Bush()


    @staticmethod
    def get_new_Wolf():
        return Wolf()
