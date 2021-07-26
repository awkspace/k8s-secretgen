#!/usr/bin/env python3

import argparse
import string
import yaml
from secrets import choice
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from base64 import b64encode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', default='.k8s-secrets.yml')
    parser.add_argument('--namespace', '-n', required=True)
    args = parser.parse_args()

    generator = SecretGen(args)
    generator.generate()


class SecretGen():

    def __init__(self, args):
        self.config = args.file
        self.namespace = args.namespace

        config.load_kube_config()
        self.k8s = client.CoreV1Api()

    def generate(self):
        self.create_namespace()

        with open(self.config, 'r') as stream:
            secrets = yaml.safe_load_all(stream)

            for defn in secrets:
                secret = self.get_secret(defn['name'])
                secret_exists = not secret

                if defn['key'] not in secret:
                    value = self.generate_value(defn.get('length', 32))
                    secret[defn['key']] = b64encode(value.encode()).decode()
                else:
                    continue

                if secret_exists:
                    self.create_secret(defn['name'], secret)
                else:
                    self.update_secret(defn['name'], secret)

    def create_namespace(self):
        try:
            self.k8s.create_namespace(
                body={
                    'metadata': {
                        'name': self.namespace
                    }
                }
            )
        except ApiException as e:
            if e.status == 409:
                pass
            else:
                raise

    def get_secret(self, name):
        try:
            resp = self.k8s.read_namespaced_secret(
                name, namespace=self.namespace)
        except ApiException as e:
            if e.status == 404:
                return {}
            else:
                raise
        return resp.data

    def generate_value(self, length):
        charset = string.ascii_lowercase + \
            string.ascii_uppercase + string.digits
        return ''.join([choice(charset) for _ in range(length)])

    def create_secret(self, name, secret):
        self.k8s.create_namespaced_secret(
            namespace=self.namespace,
            body={'metadata': {'name': name}, 'data': secret}
        )

    def update_secret(self, name, secret):
        self.k8s.patch_namespaced_secret(
            namespace=self.namespace,
            name=name,
            body={'data': secret}
        )
