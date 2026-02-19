# REGLAS DE NEGOCIO #

## APLICACIONES - USUARIOS ##

Un usuario puede: 
    1. pertenecer a varios tenants
    2. pero solo una vez por tenant
    3. un usurio corresponde a un unico rol

Un tenant:
    1. Tiene un unico dueño
    2. solo puede tener una suscripcion activa
    3. puede tener mucho roles

Al crear un tenant:
    1. se crea el rol Admin
    2. el dueño queda asignado a ese rol
    3. se crea una suscripción (PENDING hasta que pague)

Un rol:
    1. Es unico por tenantt
    2. puede tener muchos permisos