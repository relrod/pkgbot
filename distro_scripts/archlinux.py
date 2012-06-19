import json
import requests

class ArchLinux:
    @classmethod
    def search(self, name, arch=None, repository=None):
        params = {
            'name': name,
            'arch': arch,
            'repo': repository
        }
        results = requests.get(
            'https://www.archlinux.org/packages/search/json/',
            params=params).json
        packages = []
        for package in results['results']:
            packages.append({
                    'name': package['pkgname'],
                    'version': package['pkgver'],
                    'repo': package['repo'],
                    'arch': package['arch'],
                    'licenses': package['licenses'],
                    'packager': package['packager'],
                    'last_update': package['last_update'],
                    'size': package['installed_size']})        
        return packages
