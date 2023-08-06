# -*- coding: utf-8 -*-
import json
import requests
import re
import traceback
from time import time, sleep
import random
import datetime
import numpy as np
from qasmtoqcis.qasm_to_qcis import QasmToQcis
from qcistoqasm.qcis_to_qasm import QcisToQasm
from isqmap import transpile


class QcisCheck():

    def __init__(self, circuit=None):
        self.circuit = circuit

    def circuit_regular(self):
        regular_exp_map = {
            'X': r'^X(?:\s(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'Y': r'^Y(?:\s(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'Z': r'^Z(?:\s(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'X2P': r'^X2P(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'X2M': r'^X2M(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'Y2P': r'^Y2P(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'Y2M': r'^Y2M(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'H': r'^H(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'S': r'^S(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'SD': r'^SD(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'T': r'^T(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'TD': r'^TD(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){1}$',
            'CZ': r'^CZ(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9]))){2}$',
            'RX': r'^RX\s(?:Q(?:[1-5][0-9]|60|[1-9]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'RY': r'^RY\s(?:Q(?:[1-5][0-9]|60|[1-9]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'RZ': r'^RZ\s(?:Q(?:[1-5][0-9]|60|[1-9]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'RXY': r'^RXY\s(?:Q(?:[1-5][0-9]|60|[1-9]))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))\s([+-]?([0-9]*[.])?([0-9]+|[0-9]+[E][+-]?[0-9]+))$',
            'M': r'^M(?:\s+(?:Q(?:[1-5][0-9]|60|[1-9])))+$'
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
                gate_params = cir.split(' ')[2]
                if abs(float(gate_params)) > np.pi:
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

    def __init__(self, login_key=None, machine_name=None):
        self.qcis_check = QcisCheck()
        self.qasmtoqcis = QasmToQcis()
        self.qcistoqasm = QcisToQasm()
        self.login_key = login_key
        self.token = None
        self.machine_name = machine_name
        self.base_url = 'https://quantumctek-cloud.com/agency/'  # 生产环境url
        self.base_login_url = 'https://quantumctek-cloud.com/api-uaa/oauth/token' # 生产环境登录url
        self.login = self.log_in()
        if self.login == 0:
            raise Exception('登录失败')
        else:
            print('登录成功')

    def log_in(self):
        """
        Authenticate username and password and return user credit

        Returns
        -------
        log in state, 0 means pass authentication, 1 means failed

        """
        data = {
            'grant_type': 'openId',
            'openId': self.login_key,
            'account_type': 'member'
        }
        headers = {"Authorization": "Basic d2ViQXBwOndlYkFwcA=="}
        res = requests.post(url=self.base_login_url, headers=headers, data=data)
        status_code = res.status_code
        if status_code != 200:
            print('登录接口请求失败')
            return 0
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('msg', '登录失败')
        if code != 0:
            print(f'登录失败：{msg}')
            return 0
        token = result.get('data').get('access_token')
        self.token = token
        return 1

    def create_experiment(self, exp_name, remark='测试'):
        """create experiment

        Args:
            url (string): request the address

        Returns:
            0--失败, 非0成功
        """
        url = f'{self.base_url}/service/sdk/api/experiment/save'
        data = {"name": exp_name,
                "remark": remark}
        headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            print(f'创建实验接口请求失败, code:{status_code}')
            return 0
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('message', '创建实验失败')
        if code != 0:
            print(f'创建实验失败：{msg}')
            return 0
        lab_id = result.get('data').get('lab_id')
        return lab_id

    def save_experiment(self, lab_id, exp_data, name='detailtest', language='qcis'):
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
        language_list = ['isq', 'quingo', 'qcis']
        if language not in language_list:
            print(f'保存实验失败, 量子语言只能在{language_list}中选择')
        exp_data = self.get_experiment_data(exp_data.upper())
        url = self.base_url + '/service/sdk/api/experiment/detail/save'
        data = {
            "inputCode": exp_data, "lab_id": lab_id,
            "languageCode": language, "name": name,
            "source": "SDK", "computerCode": self.machine_name
        }
        headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            print('保存实验接口请求失败')
            return 0
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('message', '保存实验失败')
        if code != 0:
            print(f'保存实验失败：{msg}')
            return 0
        save_result = result.get('data').get('exp_id')
        return save_result

    def run_experiment(self, exp_id, num_shots=12000):
        """run experiment

        Args:
            url (string): request the address

        Returns:
            0--失败, 非0成功
        """
        data = {"exp_id": exp_id, "shots": num_shots}
        return self.handler_run_experiment_result(data)

    def handler_run_experiment_result(self, data):
        url = self.base_url + '/service/sdk/api/experiment/temporary/save'
        headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
        res = requests.post(url, json=data, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            print('运行实验接口请求失败')
            return 0
        result = json.loads(res.text)
        code = result.get('code', -1)
        msg = result.get('message', '运行实验失败')
        if code != 0:
            print(f'运行实验失败：{msg}')
            return 0
        run_result = result.get('data').get('query_id')
        return run_result

    def submit_job(
            self, circuit=None, exp_name="exp0",
            parameters=None, values=None, num_shots=12000,
            lab_id=None, exp_id=None, version="version01"):
        if circuit:
            circuit = self.assign_parameters(
                circuit.upper(), parameters, values)
            if not circuit:
                print('无法为线路赋值，请检查线路，参数和参数值之后重试')
                return 0
        data = {
            "exp_id": exp_id,
            "lab_id": lab_id,
            "inputCode": circuit,
            "languageCode": "qcis",
            "name": exp_name,
            "shots": num_shots,
            "source": "SDK",
            "computerCode": self.machine_name,
            "experimentDetailName": version
        }
        print(data)
        return self.handler_run_experiment_result(data)

    def query_experiment(self, query_id, max_wait_time=60):
        """query experiment

        Args:
            query_id (int): 查询id
            max_wait_time(int): 最大等待时间

        Returns:
            0--失败, 非0成功
        """
        t0 = time()
        while time()-t0 < max_wait_time:
            try:
                url = f'{self.base_url}/service/sdk/api/experiment/result/find/{query_id}'
                headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
                res = requests.get(url, headers=headers)
                status_code = res.status_code
                if status_code != 200:
                    print('查询接口请求失败')
                    return 0
                result = json.loads(res.text)
                code = result.get('code', -1)
                msg = result.get('message', '查询实验失败')
                if code != 0:
                    print(f'查询实验失败：{msg}')
                query_exp = result.get('data')
                if query_exp:
                    return query_exp
            except:
                continue
            sleep_time = random.randint(
                0, 15)*0.3+round(random.uniform(0, 1.5), 2)
            print(f'查询实验结果请等待: {{:.2f}}秒'.format(sleep_time))
            sleep(sleep_time)
        print(f'查询实验结果失败')
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
        gates_list = circuit.split('\n')
        gates_list_strip = [g.strip() for g in gates_list if g]
        gates_list_strip = [g for g in gates_list_strip if g]

        # transform circuit from QCIS to expData
        expData = '\n'.join(gates_list_strip)
        return expData

    def set_machine(self, machine_name):
        self.machine_name = machine_name

    def download_config(self, down_file=True):
        url = f'{self.base_url}/service/sdk/api/experiment/download/config/{self.machine_name}'
        headers = {"basicToken": self.token, "Authorization": f'Bearer {self.token}'}
        res = requests.get(url, headers=headers)
        status_code = res.status_code
        if status_code != 200:
            return 0
        result = json.loads(res.text)
        code = result.get('code')
        if code != 0:
            msg = result.get('msg', '下载实验参数失败')
            print(f'下载实验参数失败:{msg}')
            return 0
        data = result.get('data')
        cur_time = self.current_time()
        if down_file:
            with open(f'./{self.machine_name}_config_param_{cur_time}.json', 'w') as f:
                f.write(json.dumps(data))
        return data

    def convert_qasm_to_qcis(self, qasm):
        qcis_raw = self.qasmtoqcis.convert_qasm_to_qcis(qasm)
        simplity_qcis = self.qasmtoqcis.simplify(qcis_raw)
        return simplity_qcis

    def convert_qasm_to_qcis_from_file(self, qasm_file):
        qcis_raw = self.qasmtoqcis.convert_qasm_to_qcis_from_file(qasm_file)
        simplity_qcis = self.qasmtoqcis.simplify(qcis_raw)
        return simplity_qcis
    
    def convert_qcis_to_qasm(self, qcis):
        qasm_circuit = self.qcistoqasm.convert_qcis_to_qasm(qcis)
        return qasm_circuit

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
        state01 = result.get('resultStatus')
        basis_list = []
        basis_content = ''.join([''.join([str(s) for s in state]) for state in state01[1:]])
        qubits_num = len(state01[0])  # 测量比特个数
        for idx in range(qubits_num):
            basis_result = basis_content[idx: len(basis_content): qubits_num]
            basis_list.append([True if res == "1" else False for res in basis_result])
        return basis_list

    # 读取数据转换成量子态概率
    def readout_data_to_state_probabilities_whole(self, result):
        '''
            circuit: 线路
            result: 原始数据
        '''
        basis_list = self.readout_data_to_state_probabilities(result)
        probabilities = self.original_onversion_whole(basis_list)
        return probabilities
    
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
        qubit_num = [f'Q{i}' for i in result.get('resultStatus')[0]]
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