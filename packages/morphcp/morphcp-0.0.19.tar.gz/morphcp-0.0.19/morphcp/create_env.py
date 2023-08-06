#import morph_util.tenants.manage_tenant as manage_tenant
import morphcp.tenants.manage_tenant as manage_tenant
#import morph_util.inject.components as injector
import morphcp.inject.components as injector
#import morph_util.logging.loghandler as loghandler
import morphcp.logging.loghandler as loghandler
#import morph_util.utils.helpers as morph_util
import morphcp.utils.helpers as morph_util

#from morph_util.vars import * 
from morphcp.vars import *
#from morph_util.morphclass import RequestsApi
from morphcp.morphclass import RequestsApi
import os
import json
import urllib
import sys


def content_pack_processing():
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    injector.inject_groups()
    injector.inject_roles()
    injector.inject_optionlist()
    injector.inject_inputs()
    injector.inject_integrations()
    injector.inject_tasks()
    # BUG Troubleshoot workflows they are not finding the correct task id. 
    #injector.inject_workflow()
    injector.inject_whitelabel()
    

def process_content_pack_higher_ed(config: dict):
    """
    The process_content_pack function is the main function that will be called by the content pack.
    It will call all of the other functions in this file to inject all of your content into a tenant.
    

    :doc-author: Trelent
    """
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    # Added overrides for the json configs. 
    if "overrides" in config:
        logger.info(f"Overrides Found!!")
        if "groups" in config['overrides']:
            logger.info(f"Group Overrides Found!!")
            for item in config['overrides']['groups']:
                logger.info(f"Attempting to Create the group {item['name']}")
                payload = {'group': {'name': item['name'], "code": item['code'], "location": item['location']}}
                resp = cl.post(f'/api/groups', data = json.dumps(payload)).json()
                if resp['success'] is True:
                    logger.info(f"Successfully created group {item['name']}")
                else:
                    logger.error(f"Failed to create group {item['name']}")
                    logger.error(f"Error: {resp}")
    
    injector.inject_groups()
    injector.inject_roles()
    if "overrides" in config:
        logger.info(f"Overrides Found!!")
        if "roleGroupAccessOverride" in config['overrides']:
            logger.info(f"Role Group Access Override Found!!")
            for item in config['overrides']['roleGroupAccessOverride']:
                logger.info(f"Attempting to Update the role {item['rolename']}")
                groupId = cl.get(f"/api/groups?name={item['groupname']}").json()['groups'][0]['id']
                roleId = cl.get(f"/api/roles?name={item['rolename']}").json()['roles'][0]['id']
                payload = {"groupId": groupId, "access": item['access']}
                resp = cl.put(f'/api/roles/{roleId}/update-group', data = json.dumps(payload)).json()
                if resp['success'] is True:
                    logger.info(f"Successfully created role {item['rolename']}")
                else:
                    logger.error(f"Failed to create role {item['rolename']}")
                    logger.error(f"Error: {resp}")
    injector.inject_optionlist()
    injector.inject_inputs()
    injector.inject_tasks()
    # FIXME Troubleshoot workflows they are not finding the correct task id. 
    #injector.inject_workflow()
    injector.inject_whitelabel()
    
    def rolename_lookup(rolename):
        multi_tenant_role_id = cl.get(f'/api/roles?name={rolename}')
        multi_tenant_role_id = multi_tenant_role_id.json()
        return multi_tenant_role_id['roles'][0]['id']
    
    # for x in data['schools'].values():
    #for item in config['users'].values():
    for item in config['users']:
        firstName, lastName = item['name'].split(' ', 1)
        uname = firstName[0] + lastName[:7]
        rolename = item['rolename']
        role_id = rolename_lookup(urllib.parse.quote(rolename))
        user = json.dumps({
                "user":{
                "firstName": firstName,
                "lastName": lastName,
                "username": uname,
                "email": item['email'],
                "password": item['password'],
                "roles": [{"id": role_id}],
                "receiveNotifications": False
            }
        })
        create_user = cl.post(f'/api/users', data = user).json()
        logger.debug(create_user)
    #injector.inject_clouds()

def create_lab(config: dict):
    """
    The create_lab function is used to create a new lab.
        It does this by creating a tenant, and then creating the admin user for that tenant.
        The function also creates the content pack for the lab, which includes all of its components.

    :doc-author: Trelent
    """
    logger = loghandler.get_logger(__name__)
    logger.info("Creating Labs")
    
    # Create the tenant
    tenant_id = manage_tenant.create_tenant()
    
    # Create the tenant admin user
    manage_tenant.create_tenant_admin(tenant_id)

    morph_util.clear_session()
    bearer = morph_util.get_bearer(tenant_admin_user_name,tenant_admin_password)
    os.environ["bearertoken"] = bearer
    process_content_pack_higher_ed(config)
    

