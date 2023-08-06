import json
from page_class import *


def deal_yapi(configuration, file_path):
    print('file_path', file_path)
    yapi_url = input('请输入获取数据链接的YapiURL')
    id_dict = get_id(yapi_url, configuration)
    resp = requests.get(f'{configuration["serverUrl"]}{configuration["getInfoPath"]}', params=id_dict)
    resp_text = json.loads(resp.text)
    resp_query_path = resp_text["data"]["query_path"]
    resp_body = json.loads(resp_text["data"]["res_body"])
    resp_body_other = json.loads(resp_text["data"]["req_body_other"])

    return resp_query_path, resp_body['properties'], resp_body_other['properties']


def generate_page_list(configuration, generator_title, file_path, need_dialog=False):
    resp_query_path, resp_body, resp_body_other = deal_yapi(configuration, file_path)
    resp_body = resp_body['data']['properties']['list']['items']['properties']
    return GenerateList(generator_title, resp_query_path, resp_body_other, resp_body, f'{"dialog_" if need_dialog else ""}list')


def generate_page_add(configuration, generator_title, file_path, need_dialog=False):
    resp_query_path, resp_body, resp_body_other = deal_yapi(configuration, file_path)
    return GenerateAdd(generator_title, resp_query_path, resp_body_other, resp_body, f'{"dialog_" if need_dialog else ""}add')


def generator(config, generator_title, generator_type, file_path):
    # page_type = input('请输入想要生成的Page Type(list,add,form,dialog_list,dialog_add,dialog_form)')
    page_dict = {'1': 'list', 'list': 'list',
                 '2': 'add', 'add': 'add',
                 '3': 'dialog_list', 'dialog_list': 'dialog_list',
                 '4': 'dialog_add', 'dialog_add': 'dialog_add'}
    generator_type = page_dict[generator_type]

    if generator_type == 'list':
        return generate_page_list(config, generator_title, file_path)
    elif generator_type == 'add':
        return generate_page_add(config, generator_title, file_path)
    elif generator_type == 'dialog_list':
        return generate_page_list(config, generator_title, file_path, need_dialog=True)
    elif generator_type == 'dialog_add':
        return generate_page_add(config, generator_title, file_path, need_dialog=True)


# if __name__ == '__main__':
    # from config import defineConfig as temp_cfg
    # target_file_path = input('输入生成目标路径')
    # page_title = input('请输入生成页面标题')
    # page_type = input('请输入想要生成的Page Type(1、list 2、add 3、dialog_list 4、dialog_add)')
    # my_generator = generator(temp_cfg, page_title, page_type, '')
    # with open('res_text.vue', 'w', encoding='utf8') as f:
    #     f.write(my_generator.generate())

    # read_template(1)
