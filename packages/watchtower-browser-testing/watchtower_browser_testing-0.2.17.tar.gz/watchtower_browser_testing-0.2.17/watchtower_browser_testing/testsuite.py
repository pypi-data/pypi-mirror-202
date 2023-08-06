import os
import re
import glob
import importlib.util
import inspect
import sys
import types
import functools
import json

from playwright.sync_api import sync_playwright
from marko.ext.gfm import gfm

from watchtower_browser_testing.tracking_validation import EventQueue, RequestValidator, Validator
from watchtower_browser_testing import exceptions
from watchtower_browser_testing import config
from watchtower_browser_testing import helpers

markdown = gfm

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

def new_page_from_gtm(self, ta_page, *args, **kwargs):

    with ta_page.expect_popup() as page_info:
        ta_page.get_by_role("button", name="Reopen").click()
    return page_info.value


class TrackingTest(object):

    browsers = config.DEFAULT_BROWSERS

    pipeline_patterns = [config.DEFAULT_PIPELINE_PATTERN]

    def setUpInstance(self,
                      playwright,
                      browser,
                      gtm_web_preview_link=None,
                      tag_assistant_path=None,
                      headless=False):

        self.app = getattr(playwright, browser)

        if gtm_web_preview_link and re.match(config.GTM_WEB_PREVIEW_LINK_REGEX, gtm_web_preview_link):
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
            self.ta_page = self.context.new_page()
            self.ta_page.goto(gtm_web_preview_link)
            with self.ta_page.expect_popup() as page_info:
                self.ta_page.get_by_role("button", name="Connect").click()
            self.page = page_info.value
            self.ta_page.get_by_role("button", name="Continue", exact=True).click()
            self.page.close()
            func = functools.partial(new_page_from_gtm, ta_page=self.ta_page)
            self.context.new_page = types.MethodType(func, self.context)

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
            gtm_web_preview_link=None,
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
                                   gtm_web_preview_link=gtm_web_preview_link,
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

    @classmethod
    def scen_methods(cls):

        return [x for x in dir(cls) if x.startswith(config.SCENARIO_METHOD_PREFIX)]

    @classmethod
    def md_description(cls):

        md = markdown.parse(helpers.trim(cls.__doc__) or '')

        for scenario_method in cls.scen_methods():
            md.children.extend(markdown.parse(helpers.trim(getattr(cls, scenario_method).__doc__) or '').children)
            validation_method = config.VALIDATION_METHOD_PREFIX + scenario_method[len(config.SCENARIO_METHOD_PREFIX):]
            val = getattr(cls, validation_method)()
            for event_name, obj in val.items():
                body_validator = obj['validators'].get('body')
                if body_validator and isinstance(body_validator, Validator):
                    body_validator = body_validator.schema
                json_string = json.dumps(dict(body_validator), indent=4, cls=helpers.ExtendedEncoder)
                mdstring = config.VALIDATION_MD_STRING.format(event_name=event_name, json_string=json_string)
                md.children.extend(markdown.parse(mdstring).children)

        return md

    @classmethod
    def html_description(cls):

        return markdown.render(cls.md_description())


class MeasurementPlan(object):

    test_modules = None
    test_directory = None

    def __init__(self,
                 test_modules=None,
                 test_directory=None):

        self.test_modules = self.test_modules or test_modules
        self.test_directory = self.test_directory or test_directory

    def get_tests(self):

        directory = self.test_directory or os.getcwd()

        mods = glob.glob(os.path.join(directory, '*.py'))
        test_modules = [os.path.basename(f)[:-3] for f in mods
                        if os.path.isfile(f) and os.path.basename(f).startswith(config.TEST_FILE_PREFIX)]

        if self.test_modules:

            missing = set(self.test_modules) - set(test_modules)
            if len(missing) > 0:
                raise exceptions.NotFoundError(f'Did not find test module(s): {", ".join(missing)}')

            test_modules = [tf for tf in test_modules if tf in self.test_modules]

        tests = []

        for module_name in test_modules:

            spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory, module_name + '.py'))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            for attr in module.__dir__():
                if inspect.isclass(getattr(module, attr)) and issubclass(getattr(module, attr), TrackingTest):
                    if any(x.startswith(config.SCENARIO_METHOD_PREFIX) for x in dir(getattr(module, attr))):
                        tests.append({'module': module_name, 'class': getattr(module, attr)})

        missing_validation_methods = []
        for test in tests:
            for method in dir(test['class']):
                if method.startswith(config.SCENARIO_METHOD_PREFIX):
                    scenario = method[len(config.SCENARIO_METHOD_PREFIX):]
                    if not hasattr(test['class'], config.VALIDATION_METHOD_PREFIX + scenario):
                        missing_validation_methods.append(
                            test['module'] +
                            '.' + test['class'].__name__ +
                            '.' + config.VALIDATION_METHOD_PREFIX + scenario)

        if len(missing_validation_methods) > 0:
            raise exceptions.NotFoundError(
                f'The following validation methods are missing: {", ".join(missing_validation_methods)}')

        return tests

    def run_tests(self,
                  headless=False,
                  browser=None,
                  gtm_web_preview_link=None,
                  tag_assistant_path=None):

        if not gtm_web_preview_link is None and not re.match(config.GTM_WEB_PREVIEW_LINK_REGEX, gtm_web_preview_link):
            raise exceptions.InvalidInputError(f'This does not look like a valid gtm-preview link: {gtm_web_preview_link}')

        if not gtm_web_preview_link is None and browser != 'chromium':
            raise exceptions.InvalidInputError(f'Debugging with GTM preview only works in chromium, not {browser}')

        if not gtm_web_preview_link is None:
            tag_assistant_path = tag_assistant_path or config.DEFAULT_PATH_TO_TAG_ASSISTANT_EXTENSION
            if not (os.path.isdir(tag_assistant_path)
                    and os.path.isfile(os.path.join(tag_assistant_path, 'manifest.json'))):
                raise exceptions.InvalidInputError(f'No tag assistant extension found at {tag_assistant_path}')

        tests = self.get_tests()

        results = []
        for test in tests:

            test_instance = test['class']()
            report_data = {'module': test['module']}
            test_instance.run(headless=headless,
                              browser=browser,
                              gtm_web_preview_link=gtm_web_preview_link,
                              tag_assistant_path=tag_assistant_path,
                              report_data=report_data)
            results.extend(test_instance.results)

        return results

    def md_description(self):

        tests = self.get_tests()

        md = markdown.parse(helpers.trim(self.__doc__) or '')

        for test in tests:
            md.children.extend(test['class'].md_description().children)

        return md

    def html_description(self):

        return markdown.render(self.md_description())



