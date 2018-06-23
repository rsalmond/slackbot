from time import time

from kubernetes import config as kubeconfig
from kubernetes.config import ConfigException
from kubernetes.client.apis import apps_v1_api

from will import settings
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

try:
    kubeconfig.load_incluster_config()
except(IOError,ConfigException):
    kubeconfig.load_kube_config()

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

    deploy = get_deployment()

    for container in deploy.spec.template.spec.containers:
        if 'slackbot' in container.image:
            container.image = 'rsalmond/slackbot:{}'.format(tag)
            break

    return set_deployment(deploy)

def roll_pod():
    """ udpate the deployment in a way that causes kubernetes to roll the pod """
    deploy = get_deployment()
    # update an arbitrary label to force roll
    deploy.spec.template.metadata.labels['date'] = str(int(time()))
    return set_deployment(deploy)

class MorningPlugin(WillPlugin):

    @respond_to('^upgrade')
    def do_upgrade(self, message):
        self.reply('kk updating deployment. brb')
        try:
            roll_pod()
        except Exception as e:
            self.reply('Oops, something borked: {}'.format(e))
