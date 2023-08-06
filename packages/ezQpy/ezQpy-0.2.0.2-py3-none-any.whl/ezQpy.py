# -*- coding: utf-8 -*-
import json
import os
import requests
from bs4 import BeautifulSoup as bs
import re
from time import time, sleep
import random
import numpy as np
import traceback
import datetime
# from quMapper import SabreMapper
from isqmap import transpile
from qcistoqasm.qcis_to_qasm import QcisToQasm
from qasmtoqcis.qasm_to_qcis import QasmToQcis


class QcisCheck():

    def __init__(self, circuit=None):
        self.circuit = circuit

    def circuit_regular(self):
        regular_exp_map = {
            'X': r'^X(?:\s(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'Y': r'^Y(?:\s(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'Z': r'^Z(?:\s(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'X2P': r'^X2P(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'X2M': r'^X2M(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'Y2P': r'^Y2P(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'Y2M': r'^Y2M(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'H': r'^H(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'S': r'^S(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'SD': r'^SD(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'T': r'^T(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'TD': r'^TD(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){1}$',
            'CZ': r'^CZ(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))){2}$',
            'RX': r'^RX\s(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'RY': r'^RY\s(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'RZ': r'^RZ\s(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'RXY': r'^RXY\s(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'M': r'^M(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]|[6][1-6])))+$'
        }
        self.circuit = self.circuit.upper()
        circuit_list = self.circuit.strip().split('\n')
        measure_list = []  # 所有的M门，M门不能为空，并且所有的qubit不能重复
        new_circuit_list = circuit_list.copy()
        for index, circuit in enumerate(circuit_list):
            circuit = circuit.strip()
            cir = re.sub(' + ', ' ', circuit)  # 去掉中间多余的空格
            gate = cir.split(' ')[0]
            if gate in regular_exp_map.keys():
                # 判断是否符合基本的正则
                pattern = re.compile(regular_exp_map[gate], re.I)
                result = pattern.match(cir)
                if result is None:
                    return False
            else:
                return False
            if gate == 'M':
                # M后面不能存在相同的qubit
                qubit_list = cir.split(' ')[1:]
                measure_list.extend(qubit_list)
                after_measure_list = circuit_list[index:]
                for after_cir in after_measure_list:
                    after_cir = after_cir.strip()
                    if after_cir.startswith('M'):
                        continue
                    # 判断M之后的指令是否有M中的qubit
                    is_correct = [False if qubit in after_cir else True
                                  for qubit in qubit_list]
                    if not all(is_correct):
                        return False
            # if gate == 'CZ':
            #     # CZ指令需要两个qubit相减必须等于1，必须相邻qubit
            #     qubit_list = cir.split(' ')[1:]
            #     qubit0 = int(re.findall(r'\d+', qubit_list[0])[0])
            #     qubit1 = int(re.findall(r'\d+', qubit_list[1])[0])
            #     if abs(qubit1 - qubit0) != 1:
            #         return False
            if gate.startswith('R'):  # RX RY RZ RXY
                gate_qubit = cir.split(' ')[:2]
                gate_params = cir.split(' ')[2:]
                for gate_param in gate_params:
                    if abs(float(gate_param)) > np.pi:
                        return False
                # 匹配出指令中的小数，不包含科学计数法
                r_result = re.findall(r'([+-]*?[0-9]\.\d*(?!E|e)[0-9])', cir)
                n_result = []
                for r in r_result:
                    num_list = r.split('.')
                    before = ''.join(num_list[0])
                    after = num_list[1]
                    if float(r) > 0 and len(after) > 2:
                        n_r = before + '.' + ''.join(after[:2])
                        n_result.append(n_r)
                    elif float(r) < 0 and len(after) > 20:
                        n_r = before + '.' + ''.join(after[:20])
                        n_result.append(n_r)
                if n_result:
                    new_cir = [*gate_qubit, *n_result]
                    new_circuit_list[index] = ' '.join(new_cir)
        if len(measure_list) == 0 or \
           len(measure_list) != len(set(measure_list)):
            return False
        new_circuit = '\n'.join(
            [circuit.strip() for circuit in new_circuit_list])
        return new_circuit


class Account():

    def __init__(self, username=None, password=None, login_key=None,
                 machine_name=None, exp=None, full_expr_record=False):
        """
            full_expr_record False--覆盖 True--追加
            cloud_url = 'http://172.16.30.224:9091'
            cloud_url = 'https://quantumcomputer.ac.cn'
            cloud_url = 'http://121.37.152.73:1011'
            cloud_url = 'http://121.37.152.73:7070'
            cloud_url = 'http://172.16.30.94:7070'
        """
        self.qcis_check = QcisCheck()
        self.qasmtoqcis = QasmToQcis()
        self.qcistoqasm = QcisToQasm()
        self.username = username
        self.password = password
        self.login_key = login_key
        self.token = None
        if exp is None:
            self.exp = {}
        else:
            self.exp = exp
        self.machine_name = machine_name
        self.full_expr_record = full_expr_record
        if self.login_key:
            cloud_url = 'https://quantumcomputer.ac.cn/'
            self.base_url = f'{cloud_url}'
            self.login = self.log_in()
            if self.machine_name:
                self.set_machine(self.machine_name)
        else:
            cloud_url = 'https://quantumcomputer.ac.cn'
            self.base_url = f'{cloud_url}/pyRequest?username={username}&password={password}'
            self.login = self.log_in()
        if self.login == 0:
            raise Exception('登录失败')

    def log_in(self):
        """
        Authenticate username and password and return user credit

        Returns
        -------
        log in state, 0 means pass authentication, 1 means failed

        """
        if self.login_key:
            url = f'{self.base_url}/sdk/api/multiple/experiment/login'
            # data = {'account': self.username, 'password': self.password}
            data = {"loginToken": self.login_key}
            res = requests.post(url, json=data)
            status_code = res.status_code
            if status_code != 200:
                return 0
            result = json.loads(res.text)
            code = result.get('code', -1)
            msg = result.get('msg', '登录失败')
            if code != 0:
                print(f'登录失败：{msg}')
                return 0
            token = result.get('data').get('token')
            self.token = token
            return 1
        else:
            h = requests.get(url=self.base_url)
            return self.check_login(h, True, True)

    def check_login(self, h, flag=False, check_point=False):
        """
            check user login information.
        """
        content = bs(h.text, "html.parser")
        token_element = content.find_all('p', id='loginMsg')
        user_point_element = content.find_all('p', id='integral')
        ret = 0
        for e in token_element:
            token = str(e).split(
                '登录返回的结果---&gt;')[1].split('</p>')[0]  # 登录失败，直接返回
            token = eval(token)
            if 'msg' in token:
                ret = token.get('msg')
                print(ret)
                return 0
            else:
                self.token = token.get('token')
                print(self.token)
                if not check_point:
                    return 1

        if check_point:
            for e in user_point_element:
                user_point = str(e).split('用户积分---&gt;')[1].split('</p>')[0]
                if '积分不足' in user_point:  # 积分标签中存在 积分不足 直接返回
                    print('积分不足!')
                    raise Exception('积分不足')
                    # return 0
                else:
                    if flag:
                        print(f'您已成功登入云平台，您账号里现在有{user_point}积分')
                    return 1

    def create_experiment(self, exp_name):
        """create experiment

        Args:
            url (string): request the address

        Returns:
            0--失败, 非0成功
        """
        if self.login_key:
            url = f'{self.base_url}/sdk/api/multiple/experiment/save'
            print('当前创建实验使用的机器名:', self.machine_name)
            data = {"experimentClipId": "", "name": exp_name,
                    "machineName": self.machine_name, "source": 'SDK'}
            headers = {"sdk_token": self.token}
            res = requests.post(url, json=data, headers=headers)
            status_code = res.status_code
            if status_code != 200:
                return 0
            result = json.loads(res.text)
            code = result.get('code', -1)
            msg = result.get('msg', '创建实验失败')
            if code != 0:
                print(f'创建实验失败：{msg}')
                return 0
            lab_id = result.get('data').get('lab_id')
            if not self.full_expr_record:
                self.exp = {}

            self.exp[lab_id] = {}
            self.exp[lab_id]['lab_name'] = exp_name
            return lab_id
        else:
            sleep(random.randint(0, 15)*0.3+round(random.uniform(0, 1.5), 2))
            url = self.base_url + f'&expName={exp_name}'
            h = requests.get(url=url)
            content = bs(h.text, "html.parser")
            ret_check_login = self.check_login(h)
            if not ret_check_login:
                return ret_check_login

            create_experiment_element = content.find_all('p', id='addExp')
            for e in create_experiment_element:
                lab_id = str(e).split('新建实验返回的结果---&gt;')[1].split('</p>')[0]
                if 'msg' in lab_id:
                    exp_result = eval(lab_id)
                    if isinstance(exp_result, dict):
                        msg = exp_result.get('msg')
                        print(f'创建实验失败, {msg}')
                        return 0

                if not self.full_expr_record:
                    self.exp = {}

                self.exp[lab_id] = {}
                self.exp[lab_id]['lab_name'] = exp_name
                return lab_id
            print("创建实验失败, 没有返回结果")
            return 0

    def save_experiment(self, lab_id, exp_data, version):
        """save experiment

        Args:
            url (string): request the addresslab_id

        Returns:
            0--失败, 非0成功

        12比特异常情况：
            1.保存实验返回的结果-->{'code':500, 'msg': XXX}
            2.保存实验返回的结果-->  (多进程同时请求可能出现的情况)
            3.保存实验返回的结果-->exp_id,当前实验已保存
            4.保存实验返回的结果-->量子线路指令输入错误，请检查你的输入
        正常情况：
            1.保存实验返回的结果-->exp_id
        """
        exp_data = exp_data.upper()
        exp_data = self.get_experiment_data(exp_data)
        if self.login_key:
            url = self.base_url + '/sdk/api/multiple/experiment/detail/save'
            data = {
                "circuit": exp_data, "lab_id": lab_id,
                "language": "qcis", "version": version,
                "machineName": self.machine_name
            }
            headers = {"sdk_token": self.token}
            res = requests.post(url, json=data, headers=headers)
            status_code = res.status_code
            if status_code != 200:
                return 0
            result = json.loads(res.text)
            code = result.get('code', -1)
            msg = result.get('msg', '保存实验失败')
            if code != 0:
                print(f'保存实验失败：{msg}')
                return 0
            save_result = result.get('data').get('exp_id')
        else:
            sleep(random.randint(0, 15)*0.3+round(random.uniform(0, 1.5), 2))
            url = self.base_url + f'&expId={lab_id}&expData={exp_data}'
            h = requests.get(url=url)
            content = bs(h.text, "html.parser")
            ret_check_login = self.check_login(h)
            if not ret_check_login:
                return ret_check_login

            save_result_element = content.find_all('p', id='saveExp')
            for e in save_result_element:
                save_result = str(e).split(
                    '保存实验返回的结果---&gt;')[1].split('\n  </p>')[0]
                try:
                    save_exp = eval(save_result)
                    if 'code' in save_exp:
                        print(f"保存实验失败, {save_exp.get('msg')}")
                        return 0
                    else:
                        print('保存实验失败, 返回信息中不存在code')
                        return 0
                except:
                    if len(save_result.split(',')) > 1:
                        print(f"保存实验失败, {save_result.split(',')[1]}")
                        return 0
                    else:
                        if u'\u4e00' <= save_result <= u'\u9fff':
                            print(f'保存实验失败, {save_result}')
                            return 0

        if lab_id in self.exp:
            # 追加并且exp_detail存在于字典中
            if self.full_expr_record and 'exp_detail' in self.exp[lab_id]:
                self.exp[lab_id]['exp_detail'][save_result] = {
                    'version_name': save_result, 'run_detail': []}
            else:  # 覆盖，不管是full_expr_record为True还是exp_detail不存在于字典中，都需要重新定义exp_detail
                exp_detail = {}
                exp_detail[save_result] = {
                    'version_name': save_result, 'run_detail': []}
                self.exp[lab_id]['exp_detail'] = exp_detail
        else:
            print('保存实验版本编号无法保存, 信息中不存在当前实验集id')

        return save_result

    def run_experiment(self, exp_id, num_shots=12000):
        """run experiment

        Args:
            url (string): request the address

        Returns:
            0--失败, 非0成功
        """
        if self.login_key:
            url = self.base_url + '/sdk/api/multiple/experiment/temporary/save'
            data = {"circuit": "", "exp_id": exp_id,
                    "lab_id": "", "query_id": "",
                    "shots": num_shots, "version": "",
                    "machineName": self.machine_name,"source": 'SDK'}
            headers = {"sdk_token": self.token}
            res = requests.post(url, json=data, headers=headers)
            status_code = res.status_code
            if status_code != 200:
                return 0
            result = json.loads(res.text)
            code = result.get('code', -1)
            msg = result.get('msg', '运行实验失败')
            if code != 0:
                print(f'运行实验失败：{msg}')
                return 0
            run_result = result.get('data').get('query_id')
        else:
            sleep(random.randint(0, 15)*0.3+round(random.uniform(0, 1.5), 2))
            url = self.base_url + f'&expDetailId={exp_id}&shots={num_shots}'
            h = requests.get(url=url)
            content = bs(h.text, "html.parser")
            ret_check_login = self.check_login(h, check_point=True)
            if not ret_check_login:
                return ret_check_login

            run_result_element = content.find_all('p', id='runExp')
            for e in run_result_element:
                run_result = str(e).split(
                    '运行实验返回的结果---&gt;')[1].split('</p>')[0]

        try:
            if not self.machine_name:
                run_result = int(run_result)

            # 根据exp_id查询初lab_id
            lab_id = None
            for lab in self.exp:
                exp_detail_dir = self.exp[lab].get('exp_detail', None)
                if exp_detail_dir:
                    if exp_id in exp_detail_dir:
                        lab_id = lab

            if lab_id:
                if self.full_expr_record:  # 追加
                    self.exp[lab_id]['exp_detail'][exp_id]['run_detail'].\
                        append(run_result)
                else:
                    self.exp[lab_id]['exp_detail'][exp_id]['run_detail'] = [
                        run_result]
            else:
                print('提交实验后的查询编号无法保存，信息中不存在当前实验集id活实验版本id')

            return run_result
        except:
            print(f'运行实验失败, {run_result}')
            return 0

    def query_experiment(self, query_id, max_wait_time=60, result_type=2):
        if self.login_key is None:
            sleep(random.randint(0, 15)*0.3+round(random.uniform(0, 1.5), 2))
        """query experiment

        Args:
            query_id (int): 查询id
            max_wait_time(int): 最大等待时间
            type (int): 0:实验结果, 1:概率结果, 2:两者都要(默认0)

        Returns:
            0--失败, 非0成功
        """
        t0 = time()
        while time()-t0 < max_wait_time:
            try:
                if self.login_key:
                    if result_type not in [0, 1, 2]:
                        raise Exception('查询实验结果类型错误')
                    url = self.base_url + '/sdk/api/multiple/experiment/find/results'
                    data = {"circuit": "", "exp_id": "", "lab_id": "",
                            "quantumComputer": "", "query_id": query_id,
                            "shots": 0, "version": "string", "type": result_type}
                    headers = {"sdk_token": self.token}
                    res = requests.post(url, json=data, headers=headers)
                    status_code = res.status_code
                    if status_code != 200:
                        return 0
                    result = json.loads(res.text)
                    code = result.get('code', -1)
                    msg = result.get('msg', '查询实验失败')
                    if code != 0:
                        print(f'查询实验失败：{msg}')
                        return 0
                    query_exp = result.get('data', None)
                    if query_exp:
                        return query_exp
                else:
                    url = self.base_url + f'&download={query_id}'
                    h = requests.get(url=url)
                    content = bs(h.text, "html.parser")
                    ret_check_login = self.check_login(h)
                    if not ret_check_login:
                        return ret_check_login

                    query_result_element = content.find_all(
                        'p', id='downloadExp')
                    for e in query_result_element:
                        query_result = str(e).split(
                            '下载实验返回的结果---&gt;')[1].split('  </p>')[0]
                        query_exp = eval(query_result)
                        if 'code' in query_exp:
                            msg = query_exp.get('msg')
                        else:
                            return query_exp
            except:
                import traceback
                print(traceback.format_exc())
                sleep_time = random.randint(
                    0, 15)*0.3+round(random.uniform(0, 1.5), 2)
                print(f'查询实验结果请等待: {{:.2f}}秒'.format(sleep_time))
                sleep(sleep_time)
                continue
        print(f'查询实验结果失败')
        return 0

    def submit_job(self, circuit=None, exp_name='exp0',
                   parameters=None, values=None, num_shots=12000,
                   lab_id=None, exp_id=None, version='version01'):
        """[summary]

        Args:
            circuit_list ([type]): [description]
            exp_name (str, optional): [description]. Defaults to 'exp0'.
            parameters ([type], optional): [description]. Defaults to None.
            values ([type], optional): [description]. Defaults to None.
            num_shots (int, optional): [description]. Defaults to 12000.

        Returns
        -------
            error message: string Error message
            ("你当前正在执行的任务已超过上限, 请待任务结束后再次提交运行",
             "登录失败请检查账户密码是否正确",
             "量子线路指令输入错误, 请检查您的输入",
             "实验任务排队已达上限",
             "线路含有2个参数, 您提供了1个参数值",
             "线路含有参数[*,*,*], 请提供相应的参数值",
             "线路含有*个参数, 您提供了*个参数",
             "线路中的参数与您输入的参数名称不符")
        0--失败, 非0成功
        {
                'lab_id_1': {
                    'exp_name': exp0',
                    'exp_detail':
                        {
                            'exp_id_1':{'version_name': 'v1', 'run_detail': ['query_id1', 'query_id2']},
                            'exp_id_2':{'version_name': 'v2', 'run_detail': ['query_id1', 'query_id2']}
                        },
                    ...
                },
            ...
        }
        """
        if circuit:
            circuit = self.assign_parameters(
                circuit.upper(), parameters, values)
            if not circuit:
                print('无法为线路赋值，请检查线路，参数和参数值之后重试')
                return 0
        if self.login_key:
            url = self.base_url + '/sdk/api/multiple/experiment/temporary/save'
            data = {"circuit": circuit, "exp_id": exp_id,
                    "lab_id": lab_id, "name": exp_name,
                    "shots": num_shots, "version": version,
                    "machineName": self.machine_name,"source": 'SDK'}
            headers = {"sdk_token": self.token}
            res = requests.post(url, json=data, headers=headers)
            status_code = res.status_code
            if status_code != 200:
                return 0
            result = json.loads(res.text)
            code = result.get('code', -1)
            msg = result.get('msg', '运行实验失败')
            if code != 0:
                print(f'运行实验失败：{msg}')
                return 0
            run_result = result.get('data').get('query_id')
            return run_result
        else:
            try:
                flag = True
                if circuit and exp_id:
                    # circuit 与 exp_id 冲突，不执行
                    print('线路和实验版本冲突，无法执行')
                    return 0
                elif circuit and lab_id:
                    # 查看lab_id在字典中是否存在
                    if lab_id not in self.exp:
                        print(f'{lab_id}不存在当前字典中')
                        return 0
                    # 如存在save--run
                elif circuit:
                    # 按照lab_name，# create--save--run
                    lab_id = self.create_experiment(exp_name)
                    if not lab_id:
                        return 0
                elif exp_id and lab_id:
                    flag = False
                    # 检查字典lab_id和exp_id是否匹配
                    # 匹配成功 run
                    if lab_id not in self.exp or exp_id not in self.exp.get(lab_id, {}).get('exp_detail', {}):
                        print(f'输入的实验版本{exp_id}不属于该实验集{lab_id}下')
                        return 0
                elif exp_id:
                    # 查看字典中，是否存在exp_id
                    # 存在 run
                    for item in self.exp:
                        if exp_id in self.exp.get(item, {}).get('exp_detail', {}):
                            flag = False
                    if flag:
                        print('找不到实验版本对应的实验集')
                        return 0
                else:
                    print('没有待创建或已创建的实验可以执行')
                    return 0

                if flag:
                    exp_id = self.save_experiment(lab_id, circuit, version)
                    if not exp_id:
                        return 0
                # 提交实验
                query_id = self.run_experiment(exp_id, num_shots)
                if query_id:
                    return query_id
                else:
                    return 0

            except:
                print(traceback.format_exc())
                print('提交实验失败, 请检查参数信息')

            return 0

    def assign_parameters(self, circuit, parameters, values):
        """
        Check if the number of parameters, values match the circuit definition

        Parameters
        ----------
        circuit : string, QCIS circuit definition with or without parameter place holder
        parameters : list or ndarray of strings, parameters to be filled
        values : list or ndarray of floats, values to be assigned

        Returns
        -------
        circuit : circuit with parameters replaced by values or empty string
            empty string occurs when errors prevents parameters to be assigned
        """
        circuit = circuit.upper()
        p = re.compile(r'\{(\w+)\}')
        circuit_parameters = p.findall(circuit)
        if circuit_parameters:

            # 如果values为整数或浮点数，改为列表格式##########################################################
            if isinstance(values, (float, int)):
                values = [values]
            # 如果parameters为字符格式，改为列表格式#########################################################
            if isinstance(parameters, str):
                parameters = [parameters]
            # 将所有parameter变为大写， 否则set(parameters) != set(circuit_parameters) 不通过 ###############
            parameters = [p.upper() for p in parameters]

            if not values:
                error_message = f'线路含有参数{circuit_parameters}, 请提供相应的参数值'
                print(error_message)
                return ''

            else:
                if len(circuit_parameters) != len(values):
                    error_message = f'线路含有{len(circuit_parameters)}个参数, 您提供了{len(values)}个参数值'
                    print(error_message)
                    return ''

                elif parameters and len(circuit_parameters) != len(parameters):
                    error_message = f'线路含有{len(circuit_parameters)}个参数, 您提供了{len(parameters)}个参数'
                    print(error_message)
                    return ''

                elif set(parameters) != set(circuit_parameters):
                    error_message = '线路中的参数与您输入的参数名称不符'
                    print(error_message)
                else:
                    param_dic = {}
                    ############################# 这个转化可以删了 #########################################
                    #parameters_upper = [p.upper() for p in parameters]
                    for p, v in zip(parameters, values):
                        param_dic[p] = v
                    expData = circuit.format(**param_dic)
                    return expData

        elif parameters or values:
            error_message = '线路定义中不含有参数，无法接受您输入的参数或参数值'
            print(error_message)
            return ''
        else:
            expData = circuit
            return expData

    def get_experiment_data(self, circuit):
        """
        Parse circuit description and generate 
        experiment script and extract number
        of measured qubits

        Parameters
        ----------
        circuit : string, QCIS circuit

        Returns
        -------
        expData : string, transformed circuit

        """
        # get gates from circuit
        if self.login_key:
            gates_list = circuit.split('\n')
            gates_list_strip = [g.strip() for g in gates_list if g]
            gates_list_strip = [g for g in gates_list_strip if g]

            # transform circuit from QCIS to expData
            expData = '\n'.join(gates_list_strip)
            return expData
        else:
            gates_list = circuit.split('\n')
            gates_list_strip = [g.strip() for g in gates_list if g]
            gates_list_strip = [g for g in gates_list_strip if g]

            # transform circuit from QCIS to expData
            expData = ';'.join(gates_list_strip)
            return expData

    def load_exp_data(self, filepath='lab_info.json'):
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            with open(filepath, 'r') as f:
                exp = json.load(f)
                # exp = pickle.load(f)
            return exp
        print('文件不存在或者文件内容为空')

    def save_exp_data(self, filename='lab_info.json', mode='w'):
        if self.exp:
            with open(filename, mode) as f:
                # pickle.dump(self.exp, f)
                json.dump(self.exp, f)

    def set_machine(self, machine_name):
        url = f'{self.base_url}/sdk/api/multiple/experiment/find/quantum/computer'
        data = {
            "experimentClipId": "",
            "machineName": machine_name,
            "name": "",
            "source": "SDK"
        }
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            raise Exception('设置机器名失败，请求接口失败')
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('msg', '设置机器名失败')
        if code != 0:
            print(f'设置机器名失败：{msg}')
            raise Exception(f'设置机器名失败，{msg}')
        self.machine_name = machine_name

    def download_config(self, down_file=True):
        url = f'{self.base_url}/sdk/api/multiple/experiment/config/download'
        data = {
            "name": self.machine_name
        }
        headers = {"sdk_token": self.token}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            return 0
        result = json.loads(res.text)
        if 'code' in result:
            msg = result.get('msg', '下载实验参数失败')
            print(f'下载实验参数失败:{msg}')
            return 0
        cur_time = self.current_time()
        if down_file:
            with open(f'./{self.machine_name}_config_param_{cur_time}.json', 'w') as f:
                f.write(json.dumps(result))
        return result

    def convert_qasm_to_qcis(self, qasm, qubit_map=None):
        qcis_raw = self.qasmtoqcis.convert_qasm_to_qcis(qasm, qubit_map=qubit_map)
        simplity_qcis = self.qasmtoqcis.simplify(qcis_raw)
        return simplity_qcis

    def convert_qasm_to_qcis_from_file(self, qasm_file, qubit_map=None):
        qcis_raw = self.qasmtoqcis.convert_qasm_to_qcis_from_file(qasm_file, qubit_map=qubit_map)
        simplity_qcis = self.qasmtoqcis.simplify(qcis_raw)
        return simplity_qcis

    def qcis_check_regular(self, qcis_raw):
        self.qcis_check.circuit = qcis_raw
        res = self.qcis_check.circuit_regular()
        if isinstance(res, bool):
            print('量子线路指令输入错误，请检查你的输入')
            return 0
        return res

    def simplify(self, qcis_raw):
        new_qcis_raw = self.qcis_check_regular(qcis_raw)
        simplity_qcis = self.qasmtoqcis.simplify(new_qcis_raw)
        return simplity_qcis

    def current_time(self):
        timestamp = datetime.datetime.fromtimestamp(time())
        str_time = timestamp.strftime('%Y%m%d%H%M%S')
        return str_time
    
    def readout_data_to_state_probabilities(self, result):
        '''
            circuit: 线路
            result: 原始数据
        '''
        state01 = result.get('results')
        basis_list = []
        basis_content = ''.join([''.join([str(s) for s in state]) for state in state01[1:]])
        qubits_num = len(state01[0])  # 测量比特个数
        for idx in range(qubits_num):
            basis_result = basis_content[idx: len(basis_content): qubits_num]
            basis_list.append([True if res == "1" else False for res in basis_result])
        return basis_list

    # 读取数据转换成量子态概率全部返回
    def readout_data_to_state_probabilities_whole(self, result):
        '''
            result: 原始数据
        '''
        basis_list = self.readout_data_to_state_probabilities(result)
        probabilities = self.original_onversion_whole(basis_list)
        return probabilities
    
    # 读取数据转换成量子态概率部分，为0不返回
    def readout_data_to_state_probabilities_part(self, result):
        basis_list = self.readout_data_to_state_probabilities(result)
        probabilities = self.original_onversion_part(basis_list)
        return probabilities
    
    def original_onversion_whole(self, state01):
        #当state01为一维时转换成二维数据
        if isinstance(state01[0], bool):
            state01=[state01]
        n = len(state01)  # 读取比特数
        # 测量比特概率限制
        # if n > MAX_QUBIT_NUM:
        #     print(f'Number of qubits > {MAX_QUBIT_NUM}, cannot calculate probabilities.')
        counts = [0] * (2 ** n)
        state01_T = np.transpose(state01)  # 转置
        numShots = len(state01_T)  # 测量重复次数
        # 统计所有numShots 列
        for num in range(numShots):
            k = 0
            for i in range(n):
                k += state01_T[num][i] * (2 ** i)
            counts[k] += 1
        # 计算概率
        # P=[counts[k]/numShots for k in range(2**n)]
        P = {bin(k)[2:].zfill(n): counts[k]/numShots for k in range(2**n)}
        return P
    
    def original_onversion_part(self, state01):
        #当state01为一维时转换成二维数据
        if isinstance(state01[0], bool):
            state01=[state01]
        n = len(state01)  # 读取比特数
        # 测量比特概率限制
        # if n > MAX_QUBIT_NUM:
        #     raise Exception(f'Number of qubits > {MAX_QUBIT_NUM}, cannot calculate probabilities.')
        counts = {}
        state01_T = np.transpose(state01)  # 转置
        numShots = len(state01_T)  # 测量重复次数
        # 统计所有numShots 列
        for num in range(numShots):
            k = 0
            for i in range(n):
                k += state01_T[num][i] * (2 ** i)
            prob_state = bin(k)[2:].zfill(n)
            if prob_state not in counts:
                counts[prob_state] = 1
            else:
                counts[prob_state] += 1
        # 计算概率
        # P=[counts[k]/numShots for k in range(2**n)]
        P = {k: v/numShots for k, v in counts.items()}
        return P
    
    # 量子态概率矫正
    def probability_calibration(self, result):
        '''
            对测量得到的 01 量子态概率进行校正
            参数
            • iq2probFidelity (list[list]) -- 校正系数矩阵，列表每个元素是一个 list, 存
            储一个比特的概率校正系数，每个比特有两个校正系数，例如
                [
                [0.5, 0.5], # 比 特0
                [0.1, 0.9], # 比 特1
                [0.8, 0.2], # 比 特2
                ]
            • pm (list[float]) -- 待矫正的 01 量子态概率，长度为 2*k, 其中 k 是 iq2probFidelity
            的行数 (即比特个数)
            返回类型 list[float]

        '''
        CM_CACHE = {}
        config_json = self.download_config(down_file=False)
        qubit_num = [f'Q{i}' for i in result.get('results')[0]]
        n = len(qubit_num)  # 测量比特个数
        qubits = config_json['overview']['qubits']
        readout_fidelity0 = config_json['readout']['readoutArray']['|0> readout fidelity']['param_list']
        readout_fidelity1 = config_json['readout']['readoutArray']['|1> readout fidelity']['param_list']
        iq2probFidelity = [[readout_fidelity0[qubits.index(q)], readout_fidelity1[qubits.index(q)]] for q in qubit_num]
        P = self.readout_data_to_state_probabilities_whole(result)
        Pm = list(P.values())
        if not isinstance(iq2probFidelity[0], list):
            iq2probFidelity=[iq2probFidelity]
        f = tuple([float(fi) for fi in sum(iq2probFidelity, [])])
        if f not in CM_CACHE:
            inv_CM = 1
            for k in iq2probFidelity[::-1]:
                F00 = k[0]
                F11 = k[1]
                if F00 + F11 == 1:
                    raise Exception(f'Cannot calibrate probability with fidelity: [{F00}, {F11}]')
                inv_cm = np.array([[F11, F11 - 1], [F00 - 1, F00]]) / (F00 + F11 - 1)
                inv_CM = np.kron(inv_CM, inv_cm)
            CM_CACHE[f] = inv_CM
        else:
            inv_CM = CM_CACHE[f]
        Pi = np.dot(inv_CM, (np.array(Pm, ndmin=2).T))
        Pi = {bin(idx)[2:].zfill(n): k[0] for idx, k in enumerate(Pi)}
        return Pi
    
    def convert_qcis_to_qasm(self, qcis):
        qasm_circuit = self.qcistoqasm.convert_qcis_to_qasm(qcis)
        return qasm_circuit

    def qcis_mapping_isq(
            self, qcis_circuit, initial_layout=None,
            objective='size', seed=None, use_post_opt=False):
        config_json = self.download_config(down_file=False)
        try:
            qasm_circuit = self.convert_qcis_to_qasm(qcis_circuit)
            cur_time = self.current_time()
            qpu_file = f'./{self.machine_name}_config_param_{cur_time}.json'
            with open(qpu_file, 'w') as f:
                f.write(json.dumps(config_json))
            qasm_transpiled, _, _, _ = transpile(qasm_circuit,
                                                qpu_file, 
                                                initial_layout=initial_layout,
                                                objective=objective,
                                                seed=seed,
                                                use_post_opt=use_post_opt)
            simplity_qcis = self.convert_qasm_to_qcis(qasm_transpiled)
            return simplity_qcis
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print('circuit mapping error, will submit using the original route')
            return qcis_circuit
    
    """
        qcis mapping quingo temporary comment blocking
    """
    """
    def qcis_mapping_quingo(self, qcis_circuit):
        '''qcis mapping

        Args:
            qcis_circuit (str): qcis circuit

        Returns:
            str : qcis after mapping
        '''        
        config_json = self.download_config(down_file=False)
        try:
            # qcis转换成qasm并写入qasm_file中
            qasm_circuit = self.qcistoqasm.convert_qcis_to_qasm(qcis_circuit)
            qasm_file = 'temp/qasm.qasm'
            with open(qasm_file, 'w') as f:
                f.write(qasm_circuit)
            sabre = SabreMapper()
            # 组装chip_info_fn映射信息
            chip_info_fn = {}
            couplings = []
            coupler_maps = config_json.get('overview').get('coupler_map')
            coupler_used = config_json.get('two qubit gate').get('czGate').get('gate error').get('qubit_used')
            cz_gate_error = config_json.get('two qubit gate').get('czGate').get('gate error').get('param_list')
            for coupler, error in zip(coupler_used, cz_gate_error):
                fidelity = 1- error
                coupler_qubit_map = coupler_maps.get(coupler)
                couplings.append({"fidelity": fidelity, "qubit pair": coupler_qubit_map})
            chip_info_fn['couplings'] = couplings
            qubit_used = config_json.get('qubit').get('singleQubit').get('gate error').get('qubit_used')
            qubit_gate_error = config_json.get('qubit').get('singleQubit').get('gate error').get('param_list')
            qubit_fidelity = {}
            for qubit, error in zip(qubit_used, qubit_gate_error):
                qubit_fidelity[qubit] = 1 - error
            chip_info_fn['fidelity'] = qubit_fidelity
            chip_info_fn['has multiple chips'] = False
            chip_info_fn['qubits'] = qubit_used

            chip_info_fn_file = "temp/chip_info_fn.json"
            mapped_qasm_fn_file = "temp/mapped_qasm_fn.qasm"
            qubit_mapping_fn_file = "temp/qubit_mapping_fn.json"
            with open(chip_info_fn_file, 'w') as f:
                json.dump(chip_info_fn, f)
            # 调用quMapper做mapping操作
            success = sabre.map_schedule(qasm_file, chip_info_fn_file, mapped_qasm_fn_file, qubit_mapping_fn_file)
            if success:
                with open(qubit_mapping_fn_file, 'r') as f:
                    qubit_mapping_fn = json.load(f)
                qubit_map = qubit_mapping_fn.get('physical qubits idx')
                # mapping成功，将转换后的qasm转为qcis，其中编号根据physical qubits idx做映射
                simplity_qcis = self.convert_qasm_to_qcis_from_file(mapped_qasm_fn_file, qubit_map)
                return simplity_qcis
        except Exception as e:
            print(e)
            print('circuit mapping error, will submit using the original route')
            return qcis_circuit
    """
