from syncqb import qb_client
# from pprint import pprint
# from lxml.etree import _Element

def main():
    # table info:
    # database: bnsucj684
    # values valid for fid 6: 'Misc', '_other'
    # values valid for fid 9: 23
    # fid 3 is the record id, which is auto generated
    # use a value from fid 3 to update or delete a record
    # create a series of tests to test the functionality of each method for both xml and json
    # ONLY MODIFY OR DELETE RECORDS THAT YOU CREATED

    record_data = [
        {
            '6': 'Misc',
            '9': 23.0,
            '3': None
        },
        {
            '6': 'Misc',
            '9': 23.1,
            '3': None
        },
    ]
    record_data_csv = 'Misc,23\nMisc,23\nMisc,23\nMisc,23\nMisc,23\nMisc,23'
    uploads = [
        {
            'field': '19',
            'filename': 'test.txt',
            'value': 'MjM='
        }
    ]

    client = qb_client.get_xml_client()
    client2 = qb_client.get_json_client(default='NOT APPLICABLE')

    # xml_res = client.get_f
    xml_res = 'N/A'
    json_res = client2.do_query(
        qid=13, database="bpxua87ct", sort=[22], ascending=False)
    # json_res = 'N/A'

    print('xml_res:', xml_res)
    print('json_res:', json_res)
    




if __name__ == '__main__':
    main()