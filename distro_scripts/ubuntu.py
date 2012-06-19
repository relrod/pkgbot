import requests
from BeautifulSoup import BeautifulSoup


class Ubuntu:
    @classmethod
    def search(self, name, arch=None, repository=None):
        results = requests.get('http://packages.ubuntu.com/%s/%s' % (
            repository,
            name))
        soup = BeautifulSoup(results.text)
        summary = soup.find('h1').text.replace('\n', '')

        if not summary:
            return []

        name_ver = summary.split()

        arches = []
        for arch in soup.findAll('table')[-1].findAll('a'):
            if 'list of files' not in arch:
                arches.append(arch.text)

        # Ubuntu doesn't include license info :(
        licenses = ['License unknown']

        return [
            {
                'name': name_ver[1],
                'version': name_ver[2],
                'repo': repository,
                'licenses': licenses
            }
        ]
