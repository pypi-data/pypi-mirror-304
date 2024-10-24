from Abstracts.base_composit import BaseComposit
from Abstracts.base_message import BaseMessage
from Abstracts.base_random_uuid import BaseRandomGUID
from enum_type_message import EnumTypeMessage


class GenerateUuidAndPrint(BaseComposit):
    def __init__(self, rnd: BaseRandomGUID, msg: BaseMessage) -> None:
        super().__init__()
        self.__rnd:BaseRandomGUID = rnd
        self.__msg:BaseMessage = msg

    def run_once(self)->BaseMessage:
        rnd_uuid = self.__rnd.get_id()
        self.__msg.set_msg(msg=f"Try generate random UUID: {rnd_uuid.__str__()}", msg_type=EnumTypeMessage.Normal)
        self.__msg.show_message()

        return self.__msg