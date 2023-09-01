class DictionaryComparison:
    """
    건물 딕셔너리 끼리 비교하는 클래스
    """
    
    def __init__(self, dict_list:list):
        # type: (list[dict(Building)]) -> None
        self.dict_list = dict_list
        self.average_dicts(dict_list)

    def average_dicts(self, dict_list:list):
        # type: (list[dict(Building)]) -> None
        """
        들어온 리스트의 평균을 구합니다.
        건물 딕셔너리를 구성하는 건물 주제의 갯수를 모두 더하고 리스트 갯수로 나눕니다.
        """
        
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
        # type: (int) -> dict()
        """
        비교군의 n번째가 평균과 얼마나 차이나는지 구합니다.
        """
        
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

class InterestsComparison:
    """
    주제 리스트끼리 비교하는 클래스
    """
    def __init__(self, interest_list:list):
        # type: (list[list[Interest]]) -> None
        self.interest_list = interest_list
        self.average_list(interest_list)

    def average_list(self, interest_list:list):
        # type: (list[list[Interest]]) -> None
        """
        들어온 주제 리스트의 평균을 구합니다.
        """

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
        # type: (int) -> dict()
        """
        비교군의 n번째가 평균과 얼마나 차이나는지 구합니다.
        """

        if (order >= len(self.interest_list)):
            raise ValueError
        target_interest = self.interest_list[order]
        target_dict = {}
        return_interest = {}
        for i in target_interest:
            return_value = (
                (len(i.polygons)-self.count_average[i.name])
                /(self.biggest_count[i.name]-self.smallest_count[i.name] + 1)
            )
            return_interest[i.name] = return_value
        return return_interest