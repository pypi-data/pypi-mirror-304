class Param(object):
    def __init__(self):
        self.application_id: str = ""
        self.tenant_id: str = ""
        self.token: str = ""
        self.retry_times: int = 0
        self.schema: str = "https"
        self.hosts: list = []
        self.headers: dict = {}
        self.ak: str = ""
        self.sk: str = ""
        self.use_air_auth: bool = False


class Context(object):
    def __init__(self, param: Param):
        self._check_required_field(param)
        self.tenant: str = param.application_id
        self.tenant_id: str = param.tenant_id
        self.token: str = param.token
        self.customer_headers: dict = param.headers
        self.schema: str = param.schema
        self.use_air_auth: bool = param.use_air_auth
        self.hosts: list = param.hosts
        self.volc_auth_conf: VolcAuthConf = VolcAuthConf(param)

    @staticmethod
    def _check_required_field(param: Param) -> None:
        if len(param.application_id) == 0:
            raise Exception("Application id is empty")
        if len(param.tenant_id) == 0:
            raise Exception("Tenant id is emtpy")
        if len(param.hosts) == 0:
            raise Exception("Hosts is empty")
        Context._check_auth_required_field(param)

    @staticmethod
    def _check_auth_required_field(param: Param) -> None:
        if param.use_air_auth and param.token == "":
            raise Exception("Token is empty")

        if not param.use_air_auth and (param.sk == "" or param.ak == ""):
            raise Exception("Ak or sk is empty")


class VolcAuthConf(object):
    def __init__(self, param: Param):
        self.ak: str = param.ak
        self.sk: str = param.sk
        self.region: str = "placeholder"
