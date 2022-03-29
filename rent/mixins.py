from django.contrib.auth.mixins import PermissionRequiredMixin


class RoomCreatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.add_room",]

class RoomUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.change_room",]


class RoomDeletePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.delete_room",]
    
class RoomViewPermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.view_room",]

    def get_permission_denied_message(self) -> str:
        message = "You are not allowed to view this page."

        return message



class RenterCreatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.add_renter",]

class RenterUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.change_renter",]


class RenterDeletePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.delete_renter",]
    
class RenterViewPermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.view_renter",]



class RenterCreatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.add_renter",]

class RenterUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.change_renter",]


class RenterDeletePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.delete_renter",]
    
class RenterViewPermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.view_renter",]



class PaymentCreatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.add_payment",]

class PaymentUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.change_payment",]


class PaymentDeletePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.delete_payment",]
    
class PaymentViewPermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.view_payment",]



class ReportCreatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.add_report",]

class ReportUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.change_report",]


class ReportDeletePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.delete_report",]
    
class ReportViewPermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.view_report",]


class RoomTypeViewPermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.view_roomtype",]

class RoomTypeCreatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.create_roomtype",]

class RoomTypeUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.update_roomtype",]

class RoomTypeDeletePermissionMixin(PermissionRequiredMixin):
    permission_required=["rent.Delete_roomtype",]


class UserCreatePermissionMixin(PermissionRequiredMixin):
    permission_required=["auth.add_user",]

class UserUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required=["auth.change_user",]


class UserDeletePermissionMixin(PermissionRequiredMixin):
    permission_required=["auth.delete_user",]
    
class UserViewPermissionMixin(PermissionRequiredMixin):
    permission_required=["auth.view_user",]
    
    
    
class BuildingCreatePermissionMixin(PermissionRequiredMixin):
    permission_required=["auth.add_building",]

class BuildingUpdatePermissionMixin(PermissionRequiredMixin):
    permission_required=["auth.change_building",]


class BuildingDeletePermissionMixin(PermissionRequiredMixin):
    permission_required=["auth.delete_building",]
    
class BuildingViewPermissionMixin(PermissionRequiredMixin):
    permission_required=["auth.view_building",]
