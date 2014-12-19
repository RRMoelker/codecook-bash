# -*- coding: utf-8 -*-
import json
import urllib2

from helpers import singleton

cc_api_server = "http://codecook.io"
cc_api_path   = "/api/dev"


@singleton
class CodecookApi:
    """
    Interfaces with CodeCook.io website to get concepts, methods and snippets
    """

    def configure(self, username, key, api_server=cc_api_server, api_path=cc_api_path):
        self.username   = username
        self.key        = key
        self.api_server = api_server
        self.api_path   = api_path
        self.api_url    = api_server + api_path

    def search_concept(self, query):
        url = '/concept/search/?q=%s' % query
        return self.get_resource_data(url)

    def get_concept_detail(self, id):
        url = '/concept/%d/' % id
        return self.get_resource_data(url)

    def get_methods_detail(self, ids):
        """
        @ids is list of id values
        """
        url = '/method/set/%s/' % ";".join(map(str, ids))
        return self.get_resource_data(url)

    def get_method_detail(self, id):
        url = '/method/%d/' % id
        return self.get_resource_data(url)


    def get_path_data(self, path):
        """
        Adds API server before path
        e.g.: http://server/{path}
        """
        url = self.api_server + path
        return self.get_url_data(url)

    def get_resource_data(self, resource):
        """
        Adds API server and path before resource path
        e.g.: http://server/api/v1/{resource}
        """
        url = self.api_url + resource
        return self.get_url_data(url)

    def get_url_data(self, url):
        """
        Retrieves data from REST url,
        each request is authenticated using authorization header.
        Prepends API domain only relative path needed.
        """
        # print "opening: " + url
        request = urllib2.Request(url)
        base64string = '%s:%s' % (self.username, self.key)
        request.add_header("Authorization", "ApiKey %s" % base64string)
        response = urllib2.urlopen(request)
        data = json.loads(response.read())
        return data

