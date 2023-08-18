from Clients.NSDIClient import NSDIClient

from Clients.VWORLDClient import VWORLDClient

from Clients.BBox import BBox


class SearchClient:

        @classmethod
        def get_data_fromAddress(cls,address:str,__accuracy:float = 10):

                coords = VWORLDClient().get_coords_from_address(address)

                bbox = BBox(coords,__accuracy,__accuracy)

                search_result = NSDIClient().get_geoinfo('12623',bbox).json()['features']

                if len(search_result) >= 2:
                        return cls.get_data_fromAddress(address,__accuracy/2)
                        
                elif len(search_result) == 1:
                        return search_result
                else:
                        return cls.get_data_fromAddress(address,__accuracy*1.5)


# if __name__ == '__main__':
#         searchResult = SearchClient.get_data_fromAddress('관악로 14나길 7-5')
#         print(searchResult)
                