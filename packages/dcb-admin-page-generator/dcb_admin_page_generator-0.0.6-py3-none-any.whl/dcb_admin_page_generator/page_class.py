import time
import requests
import re
import os
import sys
here = os.path.dirname(os.path.abspath(__file__))


def deal_p(data, p_type, need_req=False):
    resp = []
    for ele in data:
        if data[ele]['type'] != 'object' and data[ele]['type'] != 'array' and ele != 'pageIndex' and ele != 'pageSize':
            temp_dict = []
            res_dict = {}
            temp_type = type_format(p_type, data[ele]['type'], data[ele]['description'],ele)
            #  判断特殊类型
            if temp_type == 'dict' or temp_type == 'select':
                print("(data[ele]['description']", (data[ele]['description']))
                temp_label, temp_dict, res_dict = deal_type_str(data[ele]['description'],ele)
            else:
                temp_label = label_format(data[ele]['description'], ele)
            #  生成template
            if p_type == 'edit':
                if need_req:
                    resp.append({'prop': ele, 'type': temp_type, 'label': temp_label, 'value': '',
                                 'data': temp_dict, 'options': {}, 'verification': 'req'})
                else:
                    resp.append({'prop': ele, 'type': temp_type, 'label': temp_label, 'value': '',
                                 'data': temp_dict, 'options': {}})
            else:
                if len(temp_dict):
                    resp.append({'prop': ele, 'type': temp_type, 'label': temp_label, 'value': '',
                                 'data': [], 'options': {'dict': res_dict}})
                else:
                    resp.append({'prop': ele, 'type': temp_type, 'label': temp_label, 'value': '',
                                 'data': [], 'options': {}})
    return resp


def translate(string):
    data = {
        'doctype': 'json',
        'type': 'AUTO',
        'i': string
    }
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url, params=data)
    result = r.json()
    try:
        return result['translateResult'][0][0]['tgt']
    except:
        return False


def type_format(p_type, ele_type, desc, prop):
    # print('desc',desc)
    img_arr = ['图']
    type_arr = ['状态', '类型']
    type_arr_en = ['Status', 'status', 'Type', 'type']
    fitter_type_arr = ['名称']
    if p_type == 'edit':
        type_dict = {'string': 'input', 'number': 'price', 'integer': 'num'}
        if any(x in desc for x in img_arr):
            return 'img'
        elif any(x in desc for x in type_arr) or any(x in prop for x in type_arr_en) and not any(x in desc for x in fitter_type_arr):
            return 'select'
        else:
            return type_dict[ele_type] if ele_type in type_dict else ele_type
    elif p_type == 'show':
        type_dict = {'string': 'str', 'number': 'str', 'integer': 'str'}
        if any(x in desc for x in img_arr):
            return 'img_s'
        elif any(x in desc for x in type_arr) or any(x in prop for x in type_arr_en) and not any(x in desc for x in fitter_type_arr):
            return 'dict'
        else:
            return type_dict[ele_type] if ele_type in type_dict else ele_type


def label_format(label, prop):
    label_arr = label.split(' ')
    label_arr = label_arr[0]
    label_arr = label_arr.split('：')
    # print(label_arr)
    # print(label_arr)
    return label_arr[0]


def deal_type_str(s, default_label):
    s = s.replace('=', '')
    number = re.findall('(-?\d+)-?', s)
    s = s.split(number[0], 1)
    # print('s',s)

    if s[0] != '':
        # print('step1', s[0])
        label = s[0].replace(':', '').replace('：', '').replace('-', '')
    else:
        # print('step2', s[0])
        label = default_label
    res = []
    res_dict = {}
    # print('number', number)
    for index in range(1, len(number)):
        # print('s1', s[1])
        # print('number[index]', number[index])
        s = s[1].split(number[index])
        res.append({'key': number[index-1], 'value': s[0].replace('，', '').replace('-', '').replace('、', '')})
        res_dict[number[index-1]] = s[0].replace('-', '').replace('、', '')
        if index == len(number) - 1:
            res.append({'key': number[index], 'value': s[1].replace('，', '').replace('-', '').replace('、', '')})
            res_dict[number[index]] = s[1].replace('-', '').replace('、', '')

    return label, res, res_dict


def deal_path(path):
    print(path["path"])
    return convert(f'api{path["path"]}', '/')


def convert(one_string, space_character):
    string_list = str(one_string).split(space_character)  # 将字符串转化为list
    first = string_list[0].lower()
    print('first', first)
    others = string_list[1:]
    others_capital = [f'{word[0].capitalize()}{word[1:]}' for word in others]  # str.capitalize():将字符串的首字母转化为大写
    others_capital[0:0] = [first]
    hump_string = ''.join(others_capital)  # 将list组合成为字符串，中间无连接符。
    return hump_string


def sort_p(s_arr):
    print('intP', [f'{index}、{s_arr[index]["label"]}' for index in range(len(s_arr))])
    is_sort = input('输入调整后的参数顺序以,或、分割（不需要请直接按回车）')
    if is_sort:
        # print(is_sort.split(','))
        return [s_arr[int(index)] for index in is_sort.split(',' if ',' in is_sort else '、')]
    else:
        return s_arr


def get_id(string, config):
    split_arr = string.split('/')

    if len(split_arr) > 4:
        api_id = split_arr[-1]
        project_id = int(split_arr[4])
        # print(config.defineConfig['projects']['token'])
        if project_id in config['projects']['token']:
            return {"id": api_id, "token": config['projects']['token'][project_id]}
        else:
            token = input('请输入token')
            return {"id": api_id, "token": token}
    else:
        return False


def read_template(file_type):
    # print(os.listdir())
    print(sys.path)

    if file_type == 'list':
        with open(f'{here}\\template\\index.vue', encoding='utf8') as f:
            text = f.read()
        return text
    elif file_type == 'add':
        with open(f'{here}\\template\\add_or_edit.vue', encoding='utf8') as f:
            text = f.read()
        return text
    elif file_type == 'dialog_add':
        with open(f'{here}\\template\\dialog_add_or_edit.vue', encoding='utf8') as f:
            text = f.read()
        return text
    elif file_type == 'dialog_list':
        with open(f'{here}\\template\\dialog_list.vue', encoding='utf8') as f:
            text = f.read()
        return text
    else:
        return ''


class GenerateList(object):
    def __init__(self, title, path, body, resp, object_type, dialog=False):
        self.Title = title
        self.Path = deal_path(path)
        self.InP = sort_p(deal_p(body, 'edit'))
        self.OutP = sort_p(deal_p(resp, 'show'))
        self.Operate = input('输入操作函数名以、分割(不需要请直接按回车)')
        self.Type = object_type

    def get_p(self):
        print('入参', self.InP)
        print('出参', self.OutP)
        return self.InP, self.OutP

    def generate(self):
        # translator = Translator(from_lang="Zh", to_lang="En")
        # translation = translator.translate("这是一只笔")
        text = read_template(self.Type)
        text = text.replace('fitter: [],', f'fitter: {self.InP},')
        #  是否需要Operate
        if self.Operate:
            operate_list = self.Operate.split('、')
            table_operation_list = [f"tp['{func}']" for func in operate_list]
            # 查看详情: { text: '查看详情', icon: 'el-icon-edit-outline', func: this.detail, authority: '' },
            op_dict = {}
            op_name_list = []
            for index in range(len(operate_list)):
                # print(op)
                # s1 = translator.translate(operate_list[index])
                s1 = translate(operate_list[index])
                s2 = convert(s1, ' ')
                print('s2', s2)
                op_name_list.append(s2)
                op_dict[operate_list[index]] = {'text': operate_list[index], 'icon': 'el-icon-edit-outline',
                                                'func': f'this.{op_name_list[-1]}', 'authority': ''}
                time.sleep(0.5)
            text = text.replace('tp = {}', f'tp={op_dict};'.replace("'this", 'this').replace("', 'aut", ",'aut"))
            text = text.replace('默认: []', f'默认:{table_operation_list}'.replace("\"", ''))
            for func in op_name_list:
                text = text.replace('// 函数填充', f'{func}(row)'+"{},"+'\n'+'    // 函数填充')
            self.OutP.append({'prop': 'op', 'label': '操作', 'type': 'op', 'data': [], 'options': {'tableOperationList': []}},)
        else:
            pass
        text = text.replace('table_option: [],', f'table_option: {self.OutP},')
        text = text.replace('// Api writePlace', "import { "+self.Path+" } from '@/generated_api';")
        text = text.replace('SOMEFUNCS_LIST', f'{self.Path}')
        text = text.replace('抽奖活动管理', f'{self.Title}')
        return text


class GenerateAdd(object):
    def __init__(self, title, path, body, resp, object_type, dialog=False):
        self.Title = title
        self.Path = deal_path(path)
        self.InP = sort_p(deal_p(body, 'edit', need_req=True))
        self.Type = object_type
        print('self.InP', self.InP)

    def get_p(self):
        print('入参', self.InP)
        return self.InP

    def generate(self):
        text = read_template(self.Type)
        text = text.replace('change_active_info: []', f'change_active_info: {self.InP}')
        text = text.replace('// Api writePlace', "import { "+self.Path+" } from '@/generated_api';")
        text = text.replace('SOMETHING_SUBMIT', f'{self.Path}')
        text = text.replace('抽奖活动管理', f'{self.Title}')
        return text



