import json
import sys
import traceback
from typing import TYPE_CHECKING

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem
from PySide6 import QtWidgets\

    


if TYPE_CHECKING:
    from main import MainWindow
from utils.utils import api_request


class Policy:
    def __init__(self, access, auth_method, ip, ips, timeout_session, until, usb_filter, otp_secret, password, server_name, kick, kickable):
        self.access = access
        self.auth_method = auth_method
        self.ip = ip
        self.ips = ips
        self.timeout_session = timeout_session
        self.until = until
        self.kick = kick
        self.kickable = kickable
        self.usb_filter = usb_filter
        self.server_name = server_name

        self.dict = {
            "access": access,
            "auth_method": auth_method,
            "ip": ip,
            "ips": ips,
            "timeout_session": timeout_session,
            "otp_secret": otp_secret,
            "password": password,
            "until": until,
            "kick": kick,
            "kickable": kickable,
            "usb_filter": usb_filter,
            "server_name": server_name
        }

class PolicyTableWidgetItem(QTableWidgetItem):
    def __init__(self, main, current_column, value, checkbox=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checkbox = checkbox
        if self.checkbox:
            self.item = CheckBoxWidget()
            self.item.checkbox.setChecked(value)
            main.tbl_user_policies.setCellWidget(0, current_column, self.item)

        else:
            self.setText(value)

    def cb_is_checked(self):
        if self.checkbox:
            return self.item.checkbox.isChecked()
        else:
            return None

class PolicyTableWidget(QtWidgets.QTableWidget):
    def __init__(self, name, checkbox=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        print(self.name)
        if checkbox:
            pass

    def get_name(self):
        return self.name


class CheckBoxWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.checkbox = QtWidgets.QCheckBox()
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.checkbox)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

class User:
    def __init__(self, ui: 'MainWindow'):

        self.user = None
        self.active = None
        self.cn = None
        self.password = None
        self.comment = None
        self.email = None
        self.ip = None
        self.name = None
        self.tg_id = None
        self.dict = {}
        self.group_policies = []
        self.ui = ui

    def init(self, user):
        self.user = user
        user_data_raw = api_request(f"users/{self.user}")
        user_data = json.loads(user_data_raw)
        self.active = user_data.get("active")
        self.cn = user_data.get("cn")
        self.password = user_data.get("password")
        self.comment = user_data.get("comment")
        self.email = user_data.get("email")
        self.ip = user_data.get("ip")
        self.name = user_data.get("name")
        self.tg_id = user_data.get("tg_id")

        self.dict = {
            "cn": self.cn,
            "name": self.name,
            "ip": self.ip,
            "password": self.password,
            "email": self.email,
            "comment": self.comment,
            "tg_id": self.tg_id,
            "active": self.active,
        }
        self.render_info()



    def init_group_policies(self):
        response = api_request(f"users/{self.user}/policies", request="full")
        try:
            if response.status_code == 200:

                policies = json.loads(response.text)
                if policies:
                    print(policies)
                    self.group_policies = []
                    for item in policies:

                        server_id = str(item[ "server_id" ])
                        server_raw = api_request(f"servers/{server_id}")
                        server_name = json.loads(server_raw)["server_info"]["name"]

                        policy = Policy(
                            access=item["access"],
                            auth_method=item["auth_method"],
                            ip=item["ip"],
                            ips=item["ips"],
                            timeout_session=item["timeout_session"],
                            until=item["until"],
                            kick=item["kick"],
                            kickable=item["kickable"],
                            usb_filter=item["usb_filter"],
                            password=item["password"],
                            otp_secret=item["otp_secret"],
                            server_name=server_name

                    )
                        self.group_policies.append(policy)

            self.render_group_policies()

        except Exception:
            print("Exception in user code:")
            print("-" * 60)
            traceback.print_exc(file=sys.stdout)
            print("-" * 60)

    def render_group_policies(self):
        self.ui.tbl_user_policies.setRowCount(0)
        column_list = json.loads(self.ui.EnumPolicies.get_all_names())

        for policy in self.group_policies:
            self.ui.tbl_user_policies.insertRow(0)
            self.ui.tbl_user_policies.setVerticalHeaderItem(0, QTableWidgetItem(policy.server_name))

            try:
                for column in column_list:
                    id_enum, type_enum = self.ui.EnumPolicies.get(column)
                    value = policy.dict[column]
                    if type_enum == "bool":
                        item = PolicyTableWidgetItem(self.ui, current_column=id_enum, checkbox=True, value=value)
                        self.ui.tbl_user_policies.setItem(0, id_enum, item)
                    else:
                        item = PolicyTableWidgetItem(self.ui, current_column=id_enum, value=str(value))
                        self.ui.tbl_user_policies.setItem(0, id_enum, item)

            except Exception:
                print("Exception in user code:")
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)

    def render_usb_policies(self):
        self.ui.tbl_user_policies.clear()
        for policy in self.group_policies:
            response = api_request(f"servers/{policy.server_name}", request="full")
            server = json.loads(response.text)
            print(server['server_info']['name'])
            server_item = QtWidgets.QTreeWidgetItem(self.ui.tbl_user_ports)
            server_item.setText(0, str(server['server_info']['name']))
            for usb in (server[ 'usb_info' ]):
                item = QtWidgets.QTreeWidgetItem(server_item)

                item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)

                item.setText(0, usb[ 'name' ])
                item.setToolTip(0, usb[ 'virtual_port' ])


    def render_info(self):
       self.ui.cb_user_active.setChecked(self.active)
       self.ui.le_user_cn.setText(self.cn)
       self.ui.le_user_comment.setText(self.comment)
       self.ui.le_user_email.setText(self.email)
       self.ui.le_user_default_ip.setText(self.ip)
       self.ui.le_user_name.setText(self.name)
       self.ui.le_user_tg_id.setText(self.tg_id)

    #def render_clear(self, main):

    def sent_params(self, data):
        print("1")
        response = api_request(f"users/{self.name}", {}, json.dumps(data), "PUT", "full")
        return response
