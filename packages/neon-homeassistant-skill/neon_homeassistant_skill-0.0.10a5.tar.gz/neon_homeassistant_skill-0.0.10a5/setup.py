# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neon_homeassistant_skill']

package_data = \
{'': ['*'], 'neon_homeassistant_skill': ['dialog/en-us/*', 'vocab/en-us/*']}

install_requires = \
['pfzy>=0.3.4,<0.4.0']

entry_points = \
{'console_scripts': ['neon-homeassistant-skill = '
                     'neon_homeassistant_skill:NeonHomeAssistantSkill'],
 'ovos.plugin.skill': ['neon_homeassistant_skill.mikejgray = '
                       'neon_homeassistant_skill:NeonHomeAssistantSkill']}

setup_kwargs = {
    'name': 'neon-homeassistant-skill',
    'version': '0.0.10a5',
    'description': 'A Neon AI Skill for Home Assistant, which integrates with ovos-PHAL-plugin-homeassistant.',
    'long_description': "# Home Assistant Neon Skill\n\nUses [PHAL Home Assistant plugin](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-homeassistant)\n\nStill a work in progress - PRs and issues welcome\n\nAvailable on PyPi: `pip install neon-homeassistant-skill`\n\n## Installation on Neon\n\n\\***\\*Note\\*\\***: This skill and the required PHAL plugin come pre-installed on Neon images for the Mycroft Mark II and Neon's published Docker images. These instructions are for custom development builds or creating your own Neon instance from scratch.\n\nInstall ovos-PHAL-plugin-homeassistant [per their documentation](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-homeassistant)\n\nThen, you can `pip install neon-homeassistant-skill`, or handle the installation from the `~/.config/neon/neon.yaml` file if you prefer:\n\n```yaml\nskills:\n  default_skills:\n    # Jokes skill included because it cannot be pip installed to the image\n    - https://github.com/JarbasSkills/skill-icanhazdadjokes/tree/dev\n    - neon-homeassistant-skill # Optionally with a version, such as neon-homeassistant-skill==0.0.10\n```\n\n### Authenticating to Home Assistant\n\nOn a device with a screen, such as the Mycroft Mark II, you can say `open home assistant dashboard` and use the OAuth login flow to authenticate from the PHAL plugin. If you don't have a screen available or prefer to edit the configuration directly, read on.\n\n---\n\nThe documentation for ovos-PHAL-plugin-homeassistant specifies which configuration file to put your Home Assistant hostname/port and API key. Note that Neon uses a YAML configuration, not a JSON file, so edit `~/.config/neon/neon.yaml` and make the following update for a minimal installation:\n\n```yaml\nPHAL:\n  ovos-PHAL-plugin-homeassistant:\n    host: http://<HA_IP_OR_HOSTNAME>:8123\n    api_key: <HA_LONG_LIVED_TOKEN>\n```\n\nThe `PHAL` node above should be at the root of the Neon user configuration file, appended to the end of file if existing content exists, and will merge with system configuration per [Neon Configuration Docs.](https://neongeckocom.github.io/neon-docs/quick_reference/configuration/)\n\nMycroft Mark II does not always support .local hostnames such as the default `homeassistant.local` DNS. You may need to use the IP of your Home Assistant instance instead. If you have a Nabu Casa subscription and don't mind traffic going out to the internet using your public Nabu Casa DNS is also a supported option. However, if your internet connectivity drops from your Neon instance, you will be unable to control your smart home devices from Neon. A local DNS/IP is preferable.\n\n## Upcoming Features\n\n- Start OAuth workflow with voice\n- Start an instance of the ovos-PHAL-plugin-homeassistant if PHAL isn't already running\n- Vacuum functions\n- HVAC functions\n",
    'author': 'Mike Gray',
    'author_email': 'mike@graywind.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
