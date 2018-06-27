import logging

from time import time
from uptime import boottime
from datetime import datetime as dt

from dxf import DXF

from kubernetes import config as kubeconfig
from kubernetes.config import ConfigException
from kubernetes.client.apis import apps_v1_api

from will import settings
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

KUBE_OK = True

try:
    kubeconfig.load_incluster_config()
except(IOError,ConfigException):
    try:
        kubeconfig.load_kube_config()
    except(FileNotFoundError):
        KUBE_OK = False

api = apps_v1_api.AppsV1Api()

def get_namespace():
    """ return  kube namespace we're running in """
    try:
        with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace') as f:
            return f.read()
    except FileNotFoundError as e:
        # yolo
        return 'default'

def get_deployment_name():
    deployment_name = getattr(settings, 'K8S_NAME', None)

    if deployment_name is None:
        raise Exception("Unable to determine kubernetes deployment name.")
    else:
        return deployment_name

def get_deployment():
    """ fetch deployment object from k8s """
    namespace = get_namespace()
    deployment_name = get_deployment_name()
    return api.read_namespaced_deployment(name=deployment_name, namespace=namespace)

def set_deployment(new_deployment):
    """ update deployment object in k8s """
    namespace = get_namespace()
    deployment_name = get_deployment_name()
    return api.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=new_deployment)

def get_current_tag():
    """ return the current tag of the slackbot container """
    deploy = get_deployment()

    for container in deploy.spec.template.spec.containers:
        if 'slackbot' in container.image:
            return container.image.split(':')[-1]

def set_current_tag(tag):
    """ update the deployment to run the container identified by `tag` """

    if tag not in list_dockerhub_tags():
        raise Exception('That tag doesnt exist in dockerhub! You tryna fuckin kill me?')

    deploy = get_deployment()

    for container in deploy.spec.template.spec.containers:
        if 'slackbot' in container.image:
            reponame = getattr(settings, 'DOCKER_REPO', None)
            if reponame is None:
                raise Exception('Unable to determine the current docker repo/image in use.')
            container.image = '{}:{}'.format(reponame, tag)
            break

    return set_deployment(deploy)

def roll_pod():
    """ udpate the deployment in a way that causes kubernetes to roll the pod """
    if not KUBE_OK:
        raise Exception('I cant update the deployment right now, I dont have a valid kubernetes client config to authenticate.')

    deploy = get_deployment()
    # update an arbitrary label to force roll
    deploy.spec.template.metadata.labels['date'] = str(int(time()))
    return set_deployment(deploy)

def auth(dxf, response):
    """ necessary for dxf module to access dockerhub """
    username = getattr(settings, 'DOCKER_USERNAME', None)
    password = getattr(settings, 'DOCKER_PASSWORD', None)

    if None in (username, password):
        raise Exception('Unable to locate dockerhub credentials.')

    dxf.authenticate(username, password, response=response)

def list_dockerhub_tags():

    reponame = getattr(settings, 'DOCKER_REPO', None)
    if reponame is None:
        raise Exception('Unable to determine the current docker repo/image in use.')

    # we'll assume dockerhub for the time being
    dxf = DXF('registry-1.docker.io', reponame, auth)

    return dxf.list_aliases()

class BotopsPlugin(WillPlugin):

    @respond_to('^upgrade to latest')
    def explain_semver(self, message):
        self.reply('Semver motherfucker, do you speak it!?')

    @respond_to('^upgrade to (?P<version>\d+\.\d+\.\d+)')
    def upgrade_to_version(self, message, version):
        """ upgrade to <version number>: fetch and run a specific version of slackbot."""
        try:
            set_current_tag(version)
        except Exception as e:
            logging.error('Error trying to set current deployment tag.')
            logging.error(e)
            self.reply(str(e))
            return

        self.reply('Aight deployment updated to version {}, restarting in a moment.'.format(version))

    @respond_to('^releases')
    def check_releases(self, message):
        """ releases: list available slackbot releases """
        try:
            releases = list_dockerhub_tags()
        except Exception as e:
            logging.error('Error trying to list dockerhub tags.')
            logging.error(e)
            self.reply(str(e))
            return

        release_list = ','.join(releases)
        #TODO: only show releases higher than current
        self.reply('There are {} releases available: {}'.format(len(releases), releases))

    @respond_to('^uptime')
    def check_uptime(self, message):
        """ uptime: report system uptime """
        uptime = dt.now() - boottime()
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds // 60) % 60
        self.reply('Host has been up for {} days {} minutes and {} seconds.'.format(uptime.days, hours, minutes))

    @respond_to('^restart')
    def do_restart(self, message):
        """ restart: bounce the slackbot container """
        self.reply(":okay: I guess I'll just kill myself ...")

        try:
            roll_pod()
        except Exception as e:
            logging.error('Error trying to roll pod.')
            logging.error(e)
            self.reply(str(e))

    @respond_to('^version')
    def say_version(self, message):
        """ version: say what my current version is. """
        self.reply('My slackbot version is {}.'.format(getattr(settings, 'SLACKBOT_VERSION', None)))
