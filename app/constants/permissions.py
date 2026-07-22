from dataclasses import dataclass


@dataclass(frozen=True)
class Permission:
    code: str
    name: str
    description: str


class PermissionCodes:

    # Usuarios
    USERS_VIEW = "USERS_VIEW"
    USERS_CREATE = "USERS_CREATE"
    USERS_UPDATE = "USERS_UPDATE"
    USERS_DELETE = "USERS_DELETE"

    # Granjas
    FARMS_VIEW = "FARMS_VIEW"
    FARMS_CREATE = "FARMS_CREATE"
    FARMS_UPDATE = "FARMS_UPDATE"
    FARMS_DELETE = "FARMS_DELETE"

    # Áreas
    AREAS_VIEW = "AREAS_VIEW"
    AREAS_CREATE = "AREAS_CREATE"
    AREAS_UPDATE = "AREAS_UPDATE"
    AREAS_DELETE = "AREAS_DELETE"

    # Roles de granja
    ROLES_VIEW = "ROLES_VIEW"
    ROLES_CREATE = "ROLES_CREATE"
    ROLES_UPDATE = "ROLES_UPDATE"
    ROLES_DELETE = "ROLES_DELETE"

    # Permisos
    PERMISSIONS_VIEW = "PERMISSIONS_VIEW"
    PERMISSIONS_CREATE = "PERMISSIONS_CREATE"
    PERMISSIONS_UPDATE = "PERMISSIONS_UPDATE"
    PERMISSIONS_DELETE = "PERMISSIONS_DELETE"

    # Usuarios por granja
    FARM_USERS_VIEW = "FARM_USERS_VIEW"
    FARM_USERS_ASSIGN = "FARM_USERS_ASSIGN"
    FARM_USERS_UPDATE = "FARM_USERS_UPDATE"
    FARM_USERS_REMOVE = "FARM_USERS_REMOVE"

    # Dispositivos
    DEVICES_VIEW = "DEVICES_VIEW"
    DEVICES_CREATE = "DEVICES_CREATE"
    DEVICES_UPDATE = "DEVICES_UPDATE"
    DEVICES_DELETE = "DEVICES_DELETE"
    DEVICES_CONTROL = "DEVICES_CONTROL"

    # Sensores
    SENSORS_VIEW = "SENSORS_VIEW"
    SENSORS_CONFIGURE = "SENSORS_CONFIGURE"

    # Tareas
    TASKS_VIEW = "TASKS_VIEW"
    TASKS_CREATE = "TASKS_CREATE"
    TASKS_UPDATE = "TASKS_UPDATE"
    TASKS_DELETE = "TASKS_DELETE"
    TASKS_EXECUTE = "TASKS_EXECUTE"

    # Horarios
    SCHEDULES_VIEW = "SCHEDULES_VIEW"
    SCHEDULES_CREATE = "SCHEDULES_CREATE"
    SCHEDULES_UPDATE = "SCHEDULES_UPDATE"
    SCHEDULES_DELETE = "SCHEDULES_DELETE"

    # Lecturas
    SENSOR_READINGS_VIEW = "SENSOR_READINGS_VIEW"

    # Reportes
    REPORTS_VIEW = "REPORTS_VIEW"
    REPORTS_EXPORT = "REPORTS_EXPORT"

    # Configuración
    SYSTEM_CONFIGURATION = "SYSTEM_CONFIGURATION"

    # Auditoría
    SYSTEM_LOGS = "SYSTEM_LOGS"

    # Respaldos
    SYSTEM_BACKUP = "SYSTEM_BACKUP"


PERMISSIONS = [
    # Usuarios
    Permission(
        PermissionCodes.USERS_VIEW, "Ver usuarios", "Permite consultar usuarios."
    ),
    Permission(
        PermissionCodes.USERS_CREATE, "Crear usuarios", "Permite registrar usuarios."
    ),
    Permission(
        PermissionCodes.USERS_UPDATE,
        "Actualizar usuarios",
        "Permite modificar usuarios.",
    ),
    Permission(
        PermissionCodes.USERS_DELETE, "Eliminar usuarios", "Permite eliminar usuarios."
    ),
    # Granjas
    Permission(PermissionCodes.FARMS_VIEW, "Ver granjas", "Permite consultar granjas."),
    Permission(
        PermissionCodes.FARMS_CREATE, "Crear granjas", "Permite registrar granjas."
    ),
    Permission(
        PermissionCodes.FARMS_UPDATE, "Actualizar granjas", "Permite modificar granjas."
    ),
    Permission(
        PermissionCodes.FARMS_DELETE, "Eliminar granjas", "Permite eliminar granjas."
    ),
    # Áreas
    Permission(PermissionCodes.AREAS_VIEW, "Ver áreas", "Permite consultar áreas."),
    Permission(PermissionCodes.AREAS_CREATE, "Crear áreas", "Permite registrar áreas."),
    Permission(
        PermissionCodes.AREAS_UPDATE, "Actualizar áreas", "Permite modificar áreas."
    ),
    Permission(
        PermissionCodes.AREAS_DELETE, "Eliminar áreas", "Permite eliminar áreas."
    ),
    # Roles
    Permission(PermissionCodes.ROLES_VIEW, "Ver roles", "Permite consultar roles."),
    Permission(PermissionCodes.ROLES_CREATE, "Crear roles", "Permite registrar roles."),
    Permission(
        PermissionCodes.ROLES_UPDATE, "Actualizar roles", "Permite modificar roles."
    ),
    Permission(
        PermissionCodes.ROLES_DELETE, "Eliminar roles", "Permite eliminar roles."
    ),
    # Permisos
    Permission(
        PermissionCodes.PERMISSIONS_VIEW, "Ver permisos", "Permite consultar permisos."
    ),
    Permission(
        PermissionCodes.PERMISSIONS_CREATE,
        "Crear permisos",
        "Permite registrar permisos.",
    ),
    Permission(
        PermissionCodes.PERMISSIONS_UPDATE,
        "Actualizar permisos",
        "Permite modificar permisos.",
    ),
    Permission(
        PermissionCodes.PERMISSIONS_DELETE,
        "Eliminar permisos",
        "Permite eliminar permisos.",
    ),
    # Usuarios por granja
    Permission(
        PermissionCodes.FARM_USERS_VIEW,
        "Ver usuarios de granja",
        "Permite consultar usuarios asignados a una granja.",
    ),
    Permission(
        PermissionCodes.FARM_USERS_ASSIGN,
        "Asignar usuarios a granja",
        "Permite asignar usuarios a una granja.",
    ),
    Permission(
        PermissionCodes.FARM_USERS_UPDATE,
        "Modificar asignación de usuarios",
        "Permite cambiar el rol de un usuario dentro de una granja.",
    ),
    Permission(
        PermissionCodes.FARM_USERS_REMOVE,
        "Retirar usuarios de granja",
        "Permite retirar usuarios de una granja.",
    ),
    # Dispositivos
    Permission(
        PermissionCodes.DEVICES_VIEW,
        "Ver dispositivos",
        "Permite consultar dispositivos.",
    ),
    Permission(
        PermissionCodes.DEVICES_CREATE,
        "Crear dispositivos",
        "Permite registrar dispositivos.",
    ),
    Permission(
        PermissionCodes.DEVICES_UPDATE,
        "Actualizar dispositivos",
        "Permite modificar dispositivos.",
    ),
    Permission(
        PermissionCodes.DEVICES_DELETE,
        "Eliminar dispositivos",
        "Permite eliminar dispositivos.",
    ),
    Permission(
        PermissionCodes.DEVICES_CONTROL,
        "Controlar dispositivos",
        "Permite enviar órdenes a los dispositivos.",
    ),
    # Sensores
    Permission(
        PermissionCodes.SENSORS_VIEW, "Ver sensores", "Permite consultar sensores."
    ),
    Permission(
        PermissionCodes.SENSORS_CONFIGURE,
        "Configurar sensores",
        "Permite configurar sensores.",
    ),
    # Tareas
    Permission(PermissionCodes.TASKS_VIEW, "Ver tareas", "Permite consultar tareas."),
    Permission(
        PermissionCodes.TASKS_CREATE, "Crear tareas", "Permite registrar tareas."
    ),
    Permission(
        PermissionCodes.TASKS_UPDATE, "Actualizar tareas", "Permite modificar tareas."
    ),
    Permission(
        PermissionCodes.TASKS_DELETE, "Eliminar tareas", "Permite eliminar tareas."
    ),
    Permission(
        PermissionCodes.TASKS_EXECUTE,
        "Ejecutar tareas",
        "Permite ejecutar tareas manualmente.",
    ),
    # Horarios
    Permission(
        PermissionCodes.SCHEDULES_VIEW, "Ver horarios", "Permite consultar horarios."
    ),
    Permission(
        PermissionCodes.SCHEDULES_CREATE,
        "Crear horarios",
        "Permite registrar horarios.",
    ),
    Permission(
        PermissionCodes.SCHEDULES_UPDATE,
        "Actualizar horarios",
        "Permite modificar horarios.",
    ),
    Permission(
        PermissionCodes.SCHEDULES_DELETE,
        "Eliminar horarios",
        "Permite eliminar horarios.",
    ),
    # Lecturas
    Permission(
        PermissionCodes.SENSOR_READINGS_VIEW,
        "Ver lecturas de sensores",
        "Permite consultar lecturas de sensores.",
    ),
    # Reportes
    Permission(
        PermissionCodes.REPORTS_VIEW, "Ver reportes", "Permite consultar reportes."
    ),
    Permission(
        PermissionCodes.REPORTS_EXPORT,
        "Exportar reportes",
        "Permite exportar reportes.",
    ),
    # Sistema
    Permission(
        PermissionCodes.SYSTEM_CONFIGURATION,
        "Configurar sistema",
        "Permite modificar la configuración general del sistema.",
    ),
    Permission(
        PermissionCodes.SYSTEM_LOGS,
        "Consultar auditoría",
        "Permite consultar los registros del sistema.",
    ),
    Permission(
        PermissionCodes.SYSTEM_BACKUP,
        "Gestionar respaldos",
        "Permite generar y restaurar respaldos.",
    ),
]
