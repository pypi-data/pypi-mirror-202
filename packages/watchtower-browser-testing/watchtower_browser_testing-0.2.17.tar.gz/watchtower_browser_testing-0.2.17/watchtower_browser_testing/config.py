TEST_FILE_PREFIX = 'tests_'
DEFAULT_PIPELINE_PATTERN = 'https?://pipeline[.].*'
SCENARIO_METHOD_PREFIX = 'scenario_'
VALIDATION_METHOD_PREFIX = 'validation_'
DEFAULT_TEST_DESCRIPTION = ''
DEFAULT_BROWSERS = ['chromium', 'firefox', 'webkit']
HARVEST_USER_SS_COOKIE_NAME = '_harvest_ss_user'
HARVEST_USER_WEB_COOKIE_NAME = '_harvest_web_user'
OLD_HARVEST_USER_ID_KEY = 'oldHarvestUserId'
GTM_WEB_PREVIEW_LINK_REGEX = r'^https://tagassistant[.]google[.]com/.*'
DEFAULT_PATH_TO_TAG_ASSISTANT_EXTENSION = r'tag_assistant'

VALIDATION_MD_STRING = '''<details>
<summary>Validation of {event_name}</summary>
```
{json_string}
```
</details>'''