import json
import shutil
import subprocess

from airtest.core.api import *
from airtest.core.helper import *
from airtest.core.ios.ios import *

auto_setup(__file__)


class apputils(object):
    def __init__(self, udid: str = None, bundle_id: str = None, parent_dir=os.environ["HOME"]):
        """初始化
        
        Keyword arguments:
        udid -- 设备的udid，此处是用的是 airtest 的 udid 格式为 http://ip 或者 http+usbmux://udid，
        如果是前者默认使用usb连接的第一个设备，如果是后者解析 udid
        
        bundle_id -- 应用的唯一标识，如果没有，从环境变量取，再没有默认为 com.sina.weibo.inhouse
        
        parent_dir -- abspath for parent_dir
        """
        # 
        o = urlparse(udid)
        if o.scheme == "http+usbmux":
            parse_udid = o.hostname
        else:
            parse_udid = self.__first_connect_usb_device_udid()
            log("使用第一个usb链接的udid", desc="[ios_utils] udid 解析")

        if not parse_udid:
            raise ValueError("invalid udid value")
        if not bundle_id:
            try:
                bundle_id = os.environ["bundle_id"]
            except KeyError as e:
                bundle_id = "com.sina.weibo.inhouse"
                log(e, desc="[ios_utils] bundle_id 解析")

        self.__client = wda.USBClient(udid=parse_udid)
        self.__logData = {}
        self.__bundle_id = bundle_id
        self.__is_mounted_documents = False
        self.__is_mounted_container = False
        self.__auto_test_mock_dir = "Autotest/Mock/"
        self.__auto_test_log_dir = "Autotest/Logs/"

        # mount point path
        self.__root_dir = os.path.expanduser(parent_dir)

        # /mount_parent_dir/uuid_bundleId_documents
        self.__mount_documents_path = os.path.join(self.__root_dir, udid + bundle_id + "documents")
        self.__mount_container_path = os.path.join(self.__root_dir, udid + bundle_id + "container")

    # def mounted_dir(self, documents=True):
    #     if documents and self.__is_mounted_documents:
    #         return self.__mount_documents_path
    #     elif not documents and self.__is_mounted_container:
    #         return self.__mount_container_path
    #     else:
    #         print("{} doesn't mounted.".format("App documents" if documents else "App container" ))
    #         return None

    # def exist_mount_point(self, mount_point) -> bool:
    #     p1 = subprocess.Popen('mount', stdout=subprocess.PIPE)
    #     p2 = subprocess.Popen(['grep', mount_point], stdin=p1.stdout, stdout=subprocess.PIPE)
    #     p1.stdout.close()
    #     p2.communicate()

    #     return True if p2.returncode == 0 else False

    def mount_documents(self) -> bool:
        return self.__mount()

    def mount_container(self) -> bool:
        return self.__mount(False)

    def __mount(self, documents=True) -> bool:

        mounted = self.__is_mounted_documents if documents else self.__is_mounted_container
        if mounted:
            return

        mount_dir = self.__mount_documents_path if documents else self.__mount_container_path
        mound_arg = '--documents' if documents else '--container'

        result = True
        if not os.path.ismount(mount_dir):
            self.__creat_empty_dir_force(mount_dir)
            code = subprocess.call(['ifuse', mount_dir, '-u', self.__uuid, mound_arg, self.__bundle_id])
            result = code == 0

        if documents:
            self.__is_mounted_documents = result
        else:
            self.__is_mounted_container = result
        return result

    def unmount(self):
        """Umount mount point and remove mount point dirctory
        
        """

        subprocess.call(['umount', self.__mount_documents_path])
        subprocess.call(['umount', self.__mount_container_path])
        if os.path.exists(self.__mount_documents_path):
            shutil.rmtree(self.__mount_documents_path)
        if os.path.exists(self.__mount_container_path):
            shutil.rmtree(self.__mount_container_path)
        self.__is_mounted_documents = False
        self.__is_mounted_container = False

    def __creat_empty_dir_force(self, folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)

        # def __creat_dir_if_not_exist(self, folder_path):

    #     if not os.path.exists(folder_path):
    #         os.makedirs(folder_path)

    def __first_connect_usb_device_udid(self) -> str:
        cmd = "tidevice list"
        lines = os.popen(cmd).readlines()
        for line in lines[1:]:
            sl = line.rstrip("\n")
            o = re.split(r"  +", sl, 5)
            if o[-1] == "usb":
                return o[0]
        return None

    def __push_file_to_device(self, local_file, parent_dir, file_name=None) -> bool:
        """Copy local file to App documents
        
        Keyword arguments:
        local_file -- local file path, abspath
        parent_dir -- the parent directory in documents, not include mount point prefix 
        file_name -- under the parent_dir
        """
        print("__push_file_to_device")
        s = os.path.expanduser(local_file)

        if not os.path.exists(s):
            raise FileNotFoundError(f"{local_file} does not exist")
        if not self.__is_mounted_documents:
            self.__mount()
        if parent_dir.startswith("/"):
            parent_dir = parent_dir[1:]
        dest = os.path.join(self.__mount_documents_path, parent_dir)
        if not os.path.exists(dest):
            os.makedirs(dest)
        if file_name:
            dest = os.path.join(dest, file_name)

        r = subprocess.call('cp' + ' -Rf ' + s + ' ' + dest, shell=True)
        return r == 0

    # def __pull_file_from_device(self, dest: str = "", app_documents_file: str = "") -> bool:
    #     """Copy App file in documents to local

    #     Keyword arguments:
    #     dest -- description
    #     parent_dir -- description
    #     file_name -- description
    #     """
    #     print("__pull_file_from_device")
    #     if not self.__is_mounted_documents:
    #         self.__mount()
    #     if app_documents_file.startswith("/"):
    #         app_documents_file = app_documents_file[1:]
    #     src = os.path.join(self.__mount_documents_path, app_documents_file)        
    #     r = subprocess.call('cp ' + '-Rf ' + src + ' ' + dest, shell=True)
    #     return r == 0

    def __app_send_request(self, path: str = "", method: str = "POST", data: dict = {}):
        """Send data to host App
        
        Keyword arguments:
        path -- description
        method -- description
        data -- description
        """
        arguments = {"bundleId": self.__bundle_id, "value": data}

        if method.upper == "POST":
            return self.__client.http.post(path, arguments)
        elif method.upper == "GET":
            return self.__client.http.get(path, arguments)
        else:
            print("__app_send_request unsurport")
            return None

    def __app_mock_data_json_file(self, data: dict = {}):
        """Mock app request with k/v pairs 
        
        Keyword arguments:
        data -- dict, { "path" : "filename"}

        """
        return self.__app_send_request('/wda/app/mock/data/file', "POST", data)

    # Public
    def push_preset_mock_ab_to_device(self, src: str):
        print("push_preset_mock_file_to_device")
        # /Documents/Autotest/Mock/AB/config.json
        parent_dir = os.path.join(self.__auto_test_mock_dir, "AB")
        self.__push_file_to_device(src, parent_dir, "config.json")

    # Public
    def mock_ab(self, data: dict = {}):
        """Mock app abtest with k/v pairs {feature_name:value}
        
        Keyword arguments:
        data -- dict, {feature_name1:val , feature_name2: value}
        """
        return self.__app_send_request('/wda/app/mock/ab', "POST", data)

    # Public
    def unmock_ab(self, data: dict = {}):
        """Unmock app abtest with features, Remove all if list is empty 
        
        Keyword arguments:
        data -- dict, {key:val , key: value}
        """
        return self.__app_send_request('/wda/app/unmock/ab', "POST", data)

    # Public
    def push_preset_mock_file_to_device(self, src):
        print("push_preset_mock_file_to_device")
        # /Autotest/Mock/Data/config.json
        parent_dir = os.path.join(self.__auto_test_mock_dir, "Data")
        self.__push_file_to_device(src, parent_dir, "config.json")

    # Public 
    def push_mock_file_to_device(self, src):
        print("push file to device")
        # /Autotest/Mock/Data/
        parent_dir = os.path.join(self.__auto_test_mock_dir, "Data")
        self.__push_file_to_device(src, parent_dir)

    # Public
    def push_mock_interface(self, url_path: str = None, file_path: str = None):
        """Mock app request with url path、local file abspath end with .json

        url_path -- request url path

        file_path -- local json file path, must end with .json
        """

        if not url_path or not file_path:
            raise ValueError("push_mock_interface arguments not None")

        print("push_mock_interface")

        # cp local file to /Autotest/Mock/Data/
        self.__push_file_to_device(file_path, "Autotest/Mock/Data/")

        # set mock map
        file_name = os.path.basename(file_path)
        self.__app_mock_data_json_file({url_path: file_name})

    # Public
    def clean_mock_interface(self, data: dict = {}):
        """Unmock app request with k/v pairs 
        
        Keyword arguments:
        data -- dict, {"path1":"file_name.json" , "path2": "file_name.json"} 
        path eg: /2/xxx/aaa

        """
        print("clean_mock_interface")
        self.__app_mock_data_json_file(data)

        # def app_mock_data_json_data(self, data):

    #     """Mock app abtest with json responce

    #     Keyword arguments:
    #     data -- dict, {key:val , key: value}

    #     """
    #     return self.__app_send_request('/wda/app/mock/data/json', "POST", data)

    # def app_ummock_data(self, data):
    #     """Unmock url paths, k/v pairs , Remove all if data is empty

    #     Keyword arguments:
    #     data -- dict, {key:val , key: value}

    #     """
    #     return self.__app_send_request('/wda/app/unmock/data', "POST", data)

    # Public
    # def pull_log_file_from_device(self):
    #     print("pull_log_file_from_device")
    #     #App: /Documents/Autotest/Logs/
    #     # locol dir:

    #     local_dir = os.environ["HOME"] + 
    #     self.__pull_file_from_device("Autotest/Logs/")

    #     r = subprocess.call('cp' + ' -Rf ' + s + ' ' + dest, shell=True)
    #     return r == 0

    # Public
    def get_last_log_file_content(self, act_code: str = ""):
        print("get_last_log_file_content")
        # 
        if len(self.__logData) > 0:
            return {}

        if not self.__is_mounted_documents:
            self.__mount()

        log_dir = os.path.join(self.__mount_documents_path, self.__auto_test_log_dir)
        if not os.path.exists(log_dir):
            return None

        subfiles = os.listdir(log_dir)
        log_file = os.path.join(log_dir, subfiles[-1])

        # Parse log file
        with open(log_file, mode="r", encoding='utf-8') as f:
            # format:    timestamp:xx|action:xx|subtype:xx|content:xxx\n
            for line in f:
                real_line = line[:-1]
                if len(real_line) == 0:
                    continue
                args = real_line.split('|')
                if len(args) != 4:
                    continue
                timestamp = args[0].split(':')[1]
                action = args[1].split(':')[1]
                subtype = args[2].split(':')[1]
                content = args[3][len("content:"):]
                log = {"ts": timestamp, "value": json.loads(content)}
                if action in self.__logData:
                    subtypes = self.__logData[action]
                    if subtype in subtypes:
                        subtypes[subtype].append(log)
                    else:
                        subtypes[subtype] = [log]
                else:
                    subtype_obj = {subtype: [log]}
                    self.__logData[action] = subtype_obj

    # Public
    def clean_log_file(self):
        print("clean log file")

    # Public
    def clean_all(self):
        """ !!!! Will Remove all in directory Autotest, eg: preset data、ab、log、mock ab、mock data
        
        """
        print("clean all")

        if not self.__is_mounted_documents:
            self.__mount()

        autotest_dir = os.path.join(self.__mount_documents_path, "Autotest")
        subprocess.call("rm" + " -rf " + autotest_dir)
        self.unmock_ab()
        self.clean_mock_interface()
        self.unmount()

    def start_app(self):
        self.__client.app_start(self.__bundle_id)
