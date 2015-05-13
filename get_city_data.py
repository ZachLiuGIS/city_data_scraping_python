import csv
from CityData import CityData

def main():
    city_data = CityData()
    input_zipcode_file = 'atlanta_zipcode.txt'
    output_csv_file = 'atlanta_zipcode_city_data.csv'
    o_file_csv = open(output_csv_file, 'w', newline='')
    csv_writer = csv.writer(o_file_csv)

    print('reading ', input_zipcode_file)

    try:
        with open(input_zipcode_file, 'r') as zipcode_file:
            #write header
            csv_writer.writerow(city_data.get_header_row())
            for item in zipcode_file:
                zipcode = item.rstrip()
                print('reading data for zipcode: ', zipcode)
                data = city_data.get_data_zip(zipcode)
                print(data)
                csv_writer.writerow(data)

    except FileNotFoundError as e:
        print('File not found.')

    finally:
        o_file_csv.close()
        print('program finished.')


if __name__ == '__main__':
    main()




