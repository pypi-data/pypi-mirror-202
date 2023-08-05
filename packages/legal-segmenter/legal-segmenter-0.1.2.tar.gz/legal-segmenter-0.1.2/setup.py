# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['legal_segmenter', 'legal_segmenter.constants']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'legal-segmenter',
    'version': '0.1.2',
    'description': 'A simple library for segmenting legal texts.',
    'long_description': '# legal-segmenter\n\n## About\n\n**What is it?** `legal-segmenter` is a simple library for segmenting legal texts.\n\n**How does it work?** A bunch of heuristic rules and a manually assembled list of common BlueBook abbreviations. (Yes it\'s that dumb.)\n\n**Can I add to it?** Absolutely! If you notice a place where the code can be improved--perhaps by addressing an edge case or adding another common abbreviation--please create a PR in the repository.\n\n## Installation\n\n```bash\n> pip3 install legal-segmenter\n```\n\n## Use\n\n```python\nfrom legal_segmenter.segmenter import Segmenter\n\n# Input data\ntext = """Rule 23 does not set forth a mere pleading standard. A party seeking class certification must affirmatively demonstrate his compliance with the Rule—that is, he must be prepared to prove that there are in fact sufficiently numerous parties, common questions of law or fact, etc. We recognized in Falcon that “sometimes it may be necessary for the court to probe behind the pleadings before coming to rest on the certification question,” 457 U. S., at 160, and that certification is proper only if “the trial court is satisfied, after a rigorous analysis, that the prerequisites of Rule 23(a) have been satisfied,” id., at 161; see id., at 160 (“[A]ctual, not presumed, conformance with Rule 23(a) remains … indispensable”). Frequently that “rigorous analysis” will entail some overlap with the merits of the plaintiff ’s underlying claim. That cannot be helped. “ ‘[T]he class determination generally involves considerations that are enmeshed in the factual and legal issues comprising the plaintiff ’s cause of action.’ ” Falcon, supra, at 160 (quoting Coopers & Lybrand v. Livesay, 437 U. S. 463, 469 (1978); some internal quotation marks omitted). Nor is there anything unusual about that consequence: The necessity of touching aspects of the merits in order to resolve preliminary matters, e.g., jurisdiction and venue, is a familiar feature of litigation. See Szabo v. Bridgeport Machines, Inc., 249 F. 3d 672, 676–677 (CA7 2001) (Easterbrook, J.)."""\n\n# Print out each sentence extracted\nseg = Segmenter()\nparagraphs = seg.segment(text)\nfor paragraph in paragraphs:\n    for sentence in paragraph:\n        print(sentence.strip())\n        print()\n```\n\nThe output of the above code is:\n\n```text\nRule 23 does not set forth a mere pleading standard.\n\nA party seeking class certification must affirmatively demonstrate his compliance with the Rule—that is, he must be prepared to prove that there are in fact sufficiently numerous parties, common questions of law or fact, etc.\n\nWe recognized in Falcon that “sometimes it may be necessary for the court to probe behind the pleadings before coming to rest on the certification question,” 457 U. S., at 160, and that certification is proper only if “the trial court is satisfied, after a rigorous analysis, that the prerequisites of Rule 23(a) have been satisfied,” id., at 161; see id., at 160 (“[A]ctual, not presumed, conformance with Rule 23(a) remains … indispensable”).\n\nFrequently that “rigorous analysis” will entail some overlap with the merits of the plaintiff ’s underlying claim.\n\nThat cannot be helped.\n\n“ ‘[T]he class determination generally involves considerations that are enmeshed in the factual and legal issues comprising the plaintiff ’s cause of action.’ ” Falcon, supra, at 160 (quoting Coopers & Lybrand v. Livesay, 437 U. S. 463, 469 (1978); some internal quotation marks omitted).\n\nNor is there anything unusual about that consequence: The necessity of touching aspects of the merits in order to resolve preliminary matters, e.g., jurisdiction and venue, is a familiar feature of litigation.\n\nSee Szabo v. Bridgeport Machines, Inc., 249 F. 3d 672, 676–677 (CA7 2001) (Easterbrook, J.).\n```\n\nwhich is not terrible!\n\n## Contact\n\nIf you have a question or any other issue, please reach out to Neel Guha (nguha@cs.stanford.edu).\n',
    'author': 'Neel Guha',
    'author_email': 'nguha@cs.stanford.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neelguha/legal-segmenter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
