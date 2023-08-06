import os
import re
import glob
import importlib.util
import inspect
import sys

from playwright.sync_api import sync_playwright

from watchtower_browser_testing.tracking_validation import EventQueue, RequestValidator
from watchtower_browser_testing import exceptions
from watchtower_browser_testing import config

class TestContext(object):

    def __init__(self):

        self.scenario_context = {}
        self.context = {}

    def get(self, key):

        return self.scenario_context.get(key) or self.context.get(key)

    def set(self, key, value, level='test'):

        assert level in ('test', 'scenario'), '`level` should be test or scenario'

        if level == 'test':
            self.context[key] = value
            self.scenario_context.pop(key, None)
        else:
            self.scenario_context[key] = value
            self.context.pop(key, None)

    def reset_scenario_context(self):

        self.scenario_context = {}

    def reset_context(self):

        self.context = {}


class TestResult(object):

    def __init__(self,
                 test_name,
                 browser,
                 scenario=None,
                 event=None,
                 ok=True,
                 errors=None,
                 data=None):

        self.test_name = test_name
        self.scenario = scenario
        self.event = event
        self.browser = browser
        self.ok = ok
        self.errors = errors
        self.data = data

    def as_dict(self):

        return {
            'name': self.test_name,
            'scenario': self.scenario,
            'event': self.event,
            'browser': self.browser,
            'ok': self.ok,
            'errors': self.errors,
            'data': self.data
        }


class TrackingTest(object):

    browsers = config.DEFAULT_BROWSERS

    pipeline_patterns = [config.DEFAULT_PIPELINE_PATTERN]

    def setUpInstance(self,
                      playwright,
                      browser,
                      gtm_preview_link=None,
                      tag_assistant_path=None,
                      headless=False):

        self.app = getattr(playwright, browser)

        if gtm_preview_link and re.match(config.GTM_PREVIEW_LINK_REGEX, gtm_preview_link):
            self.browser = None
            tag_assistant_path is tag_assistant_path or config.DEFAULT_PATH_TO_TAG_ASSISTANT_EXTENSION
            args = [
                f'--disable-extensions-except={tag_assistant_path}',
                f'--load-extension={tag_assistant_path}']
            if headless:
                args.append('--headless=new')
            self.context = self.app.launch_persistent_context(
                '',
                headless=False,
                args=args
            )
        else:
            self.browser = self.app.launch(headless=headless)
            self.context = self.browser.new_context()

        self.data_context = TestContext()

    def tearDownInstance(self):

        self.context.close()
        if self.browser:
            self.browser.close()

    def beforeEach(self):

        self.page = self.context.new_page()
        self.data_context.reset_scenario_context()

    def afterEach(self):

        self.page.close()

    def record_events(self):

        self.event_queue = EventQueue(url_patterns=self.pipeline_patterns)
        self.page.on('request', self.event_queue.register)

    def run(self,
            browser=None,
            headless=False,
            gtm_preview_link=None,
            tag_assistant_path=None,
            report_data=None):

        if browser is None:
            browsers = self.browsers
        else:
            browsers = [browser]

        self.results = []
        report_data = report_data or {}

        for browser in browsers:

            with sync_playwright() as playwright:

                self.setUpInstance(playwright,
                                   browser,
                                   gtm_preview_link=gtm_preview_link,
                                   tag_assistant_path=tag_assistant_path,
                                   headless=headless)

                tests = [func for func in dir(self) if func.startswith(config.SCENARIO_METHOD_PREFIX)]

                for test in tests:

                    scenario = test[len(config.SCENARIO_METHOD_PREFIX):]

                    self.beforeEach()

                    getattr(self, test)()
                    validation_setup = getattr(self, config.VALIDATION_METHOD_PREFIX + scenario)()

                    for event, setup in validation_setup.items():

                        validator = RequestValidator(**setup)
                        validator.select(self.event_queue.requests)

                        if validator.is_valid():
                            self.result(browser=browser, scenario=scenario, event=event, ok=True,
                                        data={'n_matched_requests': validator.n_matched_requests, **report_data})
                        else:
                            self.result(browser=browser, scenario=scenario, event=event, ok=False,
                                        errors=validator.errors,
                                        data={'n_matched_requests': validator.n_matched_requests, **report_data})

                    self.afterEach()

                self.tearDownInstance()

    def result(self,
               browser,
               scenario,
               event,
               ok,
               errors=None,
               data=None):

        self.results.append(
            TestResult(
                test_name=self.name,
                scenario=scenario,
                event=event,
                browser=browser,
                ok=ok,
                errors=errors,
                data=data)
        )

    @property
    def name(self):

        return self.__class__.__name__

    @property
    def description(self):

        return config.DEFAULT_TEST_DESCRIPTION



class TestRunner(object):

    def __init__(self,
                 modules=None,
                 directory=None):

        self.modules = modules
        self.directory = directory

    def run_tests(self,
                  headless=False,
                  browser=None,
                  gtm_preview_link=None,
                  tag_assistant_path=None):

        if not gtm_preview_link is None and not re.match(config.GTM_PREVIEW_LINK_REGEX, gtm_preview_link):
            raise exceptions.InvalidInputError(f'This does not look like a valid gtm-preview link: {gtm_preview_link}')

        if not gtm_preview_link is None and browser != 'chromium':
            raise exceptions.InvalidInputError(f'Debugging with GTM preview only works in chromium, not {browser}')

        if not gtm_preview_link is None:
            tag_assistant_path = tag_assistant_path or config.DEFAULT_PATH_TO_TAG_ASSISTANT_EXTENSION
            if not (os.path.isdir(tag_assistant_path)
                    and os.path.isfile(os.path.join(tag_assistant_path, 'manifest.json'))):
                raise exceptions.InvalidInputError(f'No tag assistant extension found at {tag_assistant_path}')

        directory = self.directory or os.getcwd()

        mods = glob.glob(os.path.join(directory, '*.py'))
        test_modules = [os.path.basename(f)[:-3] for f in mods
                      if os.path.isfile(f) and os.path.basename(f).startswith(config.TEST_FILE_PREFIX)]

        if self.modules:

            missing = set(self.modules) - set(test_modules)
            if len(missing) > 0:
                raise exceptions.NotFoundError(f'Did not find test module(s): {", ".join(missing)}')

            test_modules = [tf for tf in test_modules if tf in self.modules]

        results = []

        for module_name in test_modules:

            spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory, module_name + '.py'))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            tests = []
            for attr in dir(module):
                if inspect.isclass(getattr(module, attr)) and issubclass(getattr(module, attr), TrackingTest):
                    if any(x.startswith(config.SCENARIO_METHOD_PREFIX) for x in dir(getattr(module, attr))):
                        tests.append({'module': module_name, 'class': getattr(module, attr)})

            for test in tests:

                test_instance = test['class']()
                report_data = {'module': module_name}
                test_instance.run(headless=headless,
                                  browser=browser,
                                  gtm_preview_link=gtm_preview_link,
                                  tag_assistant_path=tag_assistant_path,
                                  report_data=report_data)
                results.extend(test_instance.results)

        return results




