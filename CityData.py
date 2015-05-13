__author__ = 'zachliu'

import re
import csv
from urllib.request import Request, urlopen, URLError


class Tools:

    def get_data_item(self, pattern, contents):
        match = re.search(pattern, contents)
        if match:
            item = match.group(1)
            return item
        else:
            return None
   
    def get_clean_number(self, num_str):
        if isinstance(num_str, str):
            #remove , $ % and . that is not followed by digit
            pattern = re.compile('[,$%]|\.(?!\d)') 
            clean_num = re.sub(pattern, '', num_str.strip())
            return clean_num
        else:
            return None


class CityData:

    def __init__(self):
        self.baseUrl = r'http://www.city-data.com/zips/'
        self.user_agent = 'Mozilla/4.0(compatible;MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.tools = Tools()

    def get_header_row(self):
        return [
            'zipcode',
            'pop_1990',
            'pop_2000',
            'pop_2010',
            'pct_renter',
            'land_sm',
            'water_sm',
            'pop_den',
            'highsch',
            'bachelor',
            'm_h_value',
            'm_rent',
            'm_age',
            'avg_h_size',
            'm_h_inc',
            'pct_pty'
        ]

    def get_page_zip(self, zipcode):
        try:
            url = self.baseUrl + str(zipcode) + '.html'
            print(url)
            request = Request(url, headers=self.headers)
            response = urlopen(request)
            return response.read().decode('utf-8')
        except URLError as e:
            if hasattr(e, "reason"):
                print("Fail to connect to page, reason: ", e.reason)
                return None

    def get_data_zip(self, zipcode):
        contents = self.get_page_zip(zipcode)

        pat_pop_1990 = re.compile('<b>Population in 1990:</b>(.*?)<b>')
        pat_pop_2000 = re.compile('<b>Zip code population in 2000:</b>(.*?)<br>')
        pat_pop_2010 = re.compile('<b>Zip code population in 2010:</b>(.*?)<br>')
        pat_pct_renter = re.compile('<b>% of renters here:.*?</p>(.*?)</td>') 
        pat_land_sm = re.compile('<b>Land area:</b>(.*?)<b>') 
        pat_water_sm = re.compile('<b>Water area:</b>(.*?)<b>') 
        pat_pop_den = re.compile('<b>Population density:</b>(.*?)<b>') 
        pat_highsch = re.compile('<b>High school or higher:</b>(.*?)</li>') 
        pat_bachelor = re.compile("<b>Bachelor's degree or higher:</b>(.*?)</li>") 
        pat_m_h_value = re.compile('<b>Estimated median house/condo value in 2011:</b>(.*?)<table>') 
        pat_m_rent = re.compile('<b>Median gross rent in 2011:</b>(.*?)</p>', 
            re.DOTALL) 
        pat_m_age = re.compile('<b>Median resident age:.*?</p>(.*?) years</td>') 
        pat_avg_h_size = re.compile('<b>Average household size:.*?</p>(.*?) people</td>') 
        pat_m_h_inc = re.compile('<b>Estimated median household income in 2011:.*?</p>(.*?)</td>') 
        pat_pct_pty = re.compile('<b>Residents with income below the poverty level in 2011:.*?</p>(.*?)</td>', 
            re.DOTALL) 

        pop_1990 = self.tools.get_clean_number(
            self.tools.get_data_item(pat_pop_1990, contents)
        )
        pop_2000 = self.tools.get_clean_number(
            self.tools.get_data_item(pat_pop_2000, contents)
        )
        pop_2010 = self.tools.get_clean_number(
            self.tools.get_data_item(pat_pop_2010, contents)
        )
        pct_renter = self.tools.get_clean_number(
            self.tools.get_data_item(pat_pct_renter, contents)
        )
        land_sm = self.tools.get_clean_number(
            self.tools.get_data_item(pat_land_sm, contents)
        )
        water_sm = self.tools.get_clean_number(
            self.tools.get_data_item(pat_water_sm, contents)
        )
        pop_den = self.tools.get_clean_number(
            self.tools.get_data_item(pat_pop_den, contents)
        )
        highsch = self.tools.get_clean_number(
            self.tools.get_data_item(pat_highsch, contents)
        )
        bachelor = self.tools.get_clean_number(
            self.tools.get_data_item(pat_bachelor, contents)
        )
        m_h_value = self.tools.get_clean_number(
            self.tools.get_data_item(pat_m_h_value, contents)
        )
        m_rent = self.tools.get_clean_number(
            self.tools.get_data_item(pat_m_rent, contents)
        )
        m_age = self.tools.get_clean_number(
            self.tools.get_data_item(pat_m_age, contents)
        )
        avg_h_size = self.tools.get_clean_number(
            self.tools.get_data_item(pat_avg_h_size, contents)
        )
        m_h_inc = self.tools.get_clean_number(
            self.tools.get_data_item(pat_m_h_inc, contents)
        )
        pct_pty = self.tools.get_clean_number(
            self.tools.get_data_item(pat_pct_pty, contents)
        )

        data_item = [zipcode, pop_1990, pop_2000, pop_2010, pct_renter,
            land_sm, water_sm, pop_den, highsch, bachelor,
            m_h_value, m_rent, m_age, avg_h_size, m_h_inc,
            pct_pty]
#        print(data_item)
        return(data_item)

def main():
    test_zip = '30338'
    print('getting data for zipcode {}.\n'.format(test_zip))
    city_data = CityData()
    city_data.get_data_zip(test_zip)


if __name__ == '__main__':
    main()
