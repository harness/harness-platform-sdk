"""Module provided Jinja Template Rendering"""
from os import environ, makedirs
import sys
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import logging
import argparse
class ConfigException(Exception):
    """Custom Error Handler"""

class Config():
    """Standard Configuration Manager"""
    def __init__(self):
        self.workdir=environ.get("PLUGIN_WORKING_DIR", Path(__file__).resolve().parent.parent)

        # Logging Setup
        self.logger=self.logging_setup()
        self.logger.debug("%s Initialized", __class__.__name__)

    def logging_setup(self):
        """Setups up the Logging Format"""
        logging.basicConfig(stream=sys.stdout,
                            level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        if environ.get("PLUGIN_DEBUG_MODE", "false") == "true":
            logger.setLevel("DEBUG")
        return logger

    def return_logging_instance(self, name):
        """Generic Logging Handler to allow modules to create instance of logging"""
        this_logger = logging.getLogger(name)
        this_logger.setLevel(self.logger.getEffectiveLevel())
        return this_logger

    def makedir(self, dir_path):
        """Creates local directories if not exists"""
        makedirs(dir_path, exist_ok=True)
        return dir_path


class TemplateException(Exception):
    """Custom Error Handler"""

class TemplateManager():
    """Main Class to manage rendering Jinja templates"""
    def __init__(self, config,
                 template_path=None,
                 template=None):
        self.config = config
        self.template_path = template_path if template_path else config.workdir
        self.template = template if template else environ.get("PLUGIN_ENTITY_TEMPLATE")
        self.logger=config.return_logging_instance(__name__)
        self.logger.debug(f"{__class__.__name__} Initialized")

    @property
    def template_path(self):
        """Set Template Directory Source Path"""
        return self._template_path

    @template_path.setter
    def template_path(self, template_path):
        """Update Template Directory Source Path"""
        # Since we are using Jinja natively, we need to override the SemGrep Rule
        #   Rule: python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2
        # https://semgrep.dev/docs/cheat-sheets/flask-xss#2b-using-a-jinja2-environment-directly
        # nosemgrep
        self._template_path=Environment(
            loader=FileSystemLoader(template_path),
            autoescape=True
        )

    @property
    def template(self):
        """Return Chosen Template Name"""
        return self._template

    @template.setter
    def template(self, template_name):
        """Update Chosen Template Name"""
        self._template=self.template_path.get_template(template_name)

    def render(self, payload):
        """Render Template with Payload"""
        return self.template.render(payload)

    def store_output(self, file_path, content):
        """Store Rendered Template"""
        with open(file_path, mode="w", encoding="utf-8") as message:
            message.write(content)
            self.logger.debug(f"... wrote {file_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate new API Class and Models"
    )
    parser.add_argument(
        '--endpoint-target',
        type=str,
        help='Provide the Class Hierarchy path (e.g ng_api, authz, pipeline, etc)'
    )
    parser.add_argument(
        '--class-prefix',
        type=str,
        help='Provide the exact Class Name to create'
    )
    parser.add_argument(
        '--class-version',
        type=str,
        default=None,
        required=False,
        help='Provide the exact API root path'
    )
    parser.add_argument(
        '--root-api-path',
        type=str,
        help='Provide the exact API root path'
    )
    parser.add_argument(
        '--should-wrap',
        action='store_true',
        help='Should the request payload be wrapped?'
    )
    parser.add_argument(
        '--unwrap-key',
        type=str,
        default=None,
        help='Provide the exact API root path'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Compare against baseline (requires baseline to exist)'
    )

    # If no arguments were provided (sys.argv[1:] is empty)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.debug:
        environ["PLUGIN_DEBUG_MODE"] = "true"
    config = Config()
    template_dir = Path(config.workdir).joinpath("templates")

    root_output_dir = Path(config.workdir).joinpath("src","harness_python_sdk")

    data = {
        "base_api_class.py.j2": {
            "ENDPOINT_TARGET": args.endpoint_target,
            "CLASS_NAME_PREFIX" : args.class_prefix,
            "ROOT_API_PATH": args.root_api_path,
            "SHOULD_WRAP": args.should_wrap,
            "UNWRAP_KEY": args.unwrap_key,
            "ROOT_DIR": "",
            "CLASS_VERSION": args.class_version
        },
        "base_api_model.py.j2": {
            "CLASS_NAME_PREFIX" : args.class_prefix,
            "ROOT_DIR": "models",
            "CLASS_VERSION": args.class_version
        },
        "base_smoke_test.py.j2": {
            "CLASS_NAME_PREFIX" : args.class_prefix,
            "ROOT_DIR": "tests/smoke",
            "PARENT": True,
            "CLASS_VERSION": args.class_version
        }
    }
    for tpl_file_name, raw_payload in data.items():
        config.logger.info("Processing the File %s", [tpl_file_name])
        payload = {k: v for k, v in raw_payload.items() if v is not None}
        config.logger.debug("\t Payload")
        config.logger.debug("\t %s", [payload])

        if "PARENT" in raw_payload:
            output_dir = Path(config.workdir).joinpath(payload['ROOT_DIR'])
        else:
            output_dir = Path(root_output_dir).joinpath(payload['ROOT_DIR'], args.endpoint_target)
        config.logger.debug("\t Output Directory")
        config.logger.debug("\t %s", [output_dir])
        config.makedir(output_dir)
        tpl_manager = TemplateManager(
            config=config, template_path=template_dir,
            template=tpl_file_name
        )
        payload = {k: v for k, v in payload.items() if v is not None}
        rendered = tpl_manager.render(payload=payload)
        output_file_name = args.class_prefix.lower()
        if not output_file_name.endswith("s"):
            output_file_name = f"{output_file_name}s"
        if "CLASS_VERSION" in payload:
            output_file_name = f"{output_file_name}_{payload["CLASS_VERSION"].lower()}"
        output_file = Path(output_dir).joinpath(f"{output_file_name}.py")
        config.logger.debug("\t Output File")
        config.logger.debug("\t %s", [output_file])
        tpl_manager.store_output(file_path=output_file, content=rendered)


if __name__ == '__main__':
    sys.exit(main())
