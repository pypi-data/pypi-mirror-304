from typing import List, Union, Dict, Any

from ....models.messages.meta_message_model.meta_base_notification_json import BaseMetaNotificationJson, NotificationType
from ....models.messages.meta_message_model.meta_message_json import MetaMessageJson
from ....models.messages.meta_message_model.meta_status_json import MetaStatusJson
from ....models.messages.meta_message_model.meta_error_json import MetaErrorJson
from ....models.messages.meta_message_model.meta_unknown_json import MetaUnknownJson

class MetaNotificationFactory:
    @staticmethod
    def create(data: Dict[str, Any]) -> Union[MetaMessageJson, MetaStatusJson, MetaErrorJson]:
        base_notification = BaseMetaNotificationJson(**data) 
        notification_type: NotificationType = base_notification.get_notification_type()
        
        match notification_type:
            case NotificationType.MESSAGES:
                return MetaMessageJson(**data)
            case NotificationType.STATUSES:
                return MetaStatusJson(**data)
            case NotificationType.ERRORS: 
                return MetaErrorJson(**data)
            case NotificationType.UNKNOWN: # Tiene entry, object, changes y values. Pero no es Messages ni Statuses
                return MetaUnknownJson(**data)
            case NotificationType.INEXISTENT: # tiene entry, object. Puede no tener changes o values
                return base_notification
            case _: # Es imposible que llegue a este caso
                raise ValueError(f"Unknown notification type: {notification_type}")

