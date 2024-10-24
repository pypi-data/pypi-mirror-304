import yaml
import tools


class GetConf:
    def __init__(self):
        project_path = tools.get_project_path()
        with open(project_path + tools.sep(["config", "environment.yaml"], add_sep_before=True), "r",
                  encoding="UTF-8") as env_file:
            self.env = yaml.load(env_file, Loader=yaml.FullLoader)
            if self.env["environment"] == "dev":
                with open(project_path + tools.sep(["config", "dev.yaml"], add_sep_before=True), "r",
                          encoding="UTF-8") as config_file:
                    self.config = yaml.load(config_file, Loader=yaml.FullLoader)

            else:
                with open(project_path + tools.sep(["config", "prod.yaml"], add_sep_before=True), "r",
                          encoding="UTF-8") as config_file:
                    self.config = yaml.load(config_file, Loader=yaml.FullLoader)

    def get_username_password(self, user):
        return self.config["user"][user]["username"], self.config["user"][user]["password"]

    def get_url(self):
        """
        获取测试地址
        :return:
        """
        return self.config["base_url"]

    def get_mysql_config(self):
        return self.config["mysql"]

    def get_obs_config(self):
        return self.config["obs"]

    def get_redis(self):
        return self.config["redis"]

    def get_dingding_webhook(self):
        return self.config["dingding_group"]["webhook"]

    def get_qywx_webhook(self):
        return self.config["qywx_group"]["webhook"]

    def get_jenkins(self):
        return self.config["jenkins"]

    # 获取项目名称
    def get_project_name(self):
        return self.env["project_name"]

    def get_report_title(self):
        return self.env["report_title"]

    def get_api_base_url(self):
        return self.config["api_base_url"]

    def get_proxy_url(self):
        return f"{self.config['api_base_url']}{self.config['api_proxy_url']}"

    def get_actuator_base_url(self):
        return self.config["actuator_base_url"]

    # 获取当前测试模式
    def get_current_mode(self):
        if self.env["environment"] == "prod":
            return True
        else:
            return False


if __name__ == '__main__':
    print(GetConf().get_proxy_url())
