from src.service.common_service import CommonService


class ServiceFactory:

    @staticmethod
    def get_common_service():
        return CommonService()
