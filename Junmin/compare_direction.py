
class Comparison_dict:
    def __init__(self, dict_list:list):
        self.dict_list = dict_list
        self.average_dicts(dict_list)

    def average_dicts(self, dict_list:list):

        self.whole_count = {}
        self.smallest_count = {}
        self.biggest_count = {}

        overall = 0

        for dict in dict_list:
            for name, buildings in dict.items():
                if name in self.whole_count:
                    self.whole_count[name] += len(buildings)
                    self.biggest_count[name] = max(len(buildings),self.biggest_count[name])
                    self.smallest_count[name] = min(len(buildings),self.smallest_count[name])
                else:
                    self.whole_count[name] = len(buildings)
                    self.biggest_count[name] = len(buildings)
                    self.smallest_count[name] = len(buildings)


                overall += len(buildings)

        self.count_average = {key: value / len(dict_list) for key, value in self.whole_count.items()}

    def compare_dicts(self, order):
        if (order >= len(self.dict_list)):
            raise ValueError
        target_dict = self.dict_list[order]
        return_dict = {}
        for key in target_dict:
            return_value = (
                (len(target_dict[key])-self.count_average[key])
                /(self.biggest_count[key]-self.smallest_count[key]+1)
            )

            return_dict[key] = return_value
        
        return return_dict
    
        


class Comparison_interest:
    def __init__(self, interest_list:list):
        self.interest_list = interest_list
        self.average_list(interest_list)

    def average_list(self, interest_list:list):

        self.whole_count = {}
        self.smallest_count = {}
        self.biggest_count = {}

        overall = 0

        for interests in interest_list:
            for interest in interests:
                name = interest.name
                buildings = interest.polygons
                if name in self.whole_count:
                    self.whole_count[name] += len(buildings)
                    self.biggest_count[name] = max(len(buildings),self.biggest_count[name])
                    self.smallest_count[name] = min(len(buildings),self.smallest_count[name])
                else:

                    self.whole_count[name] = len(buildings)
                    self.biggest_count[name] = len(buildings)
                    self.smallest_count[name] = len(buildings)


                overall += len(buildings)

        self.count_average = {key: value / len(interest_list) for key, value in self.whole_count.items()}

    def compare_interests(self, order):
        if (order >= len(self.interest_list)):
            raise ValueError
        target_interest = self.interest_list[order]
        target_dict = {}
        return_interest = {}

        for i in target_interest:
            print (i.name)
            return_value = (
                (len(i.polygons)-self.count_average[i.name])
                /(self.biggest_count[i.name]-self.smallest_count[i.name] + 1)
            )

            return_interest[i.name] = return_value
        
        return return_interest
    
        

            



    