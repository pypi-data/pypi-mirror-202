from django.contrib.contenttypes.fields import ReverseGenericManyToOneDescriptor
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.conf import settings
from jinja2 import Template
import os

__version__ = '0.0.1'


class Command(BaseCommand):
    help = 'Generates files (serializers, views, urls) necessary to host apis via DRF'

    def __init__(self):
        self.app = None
        self.model_list = None
        super(Command, self).__init__()

    def add_arguments(self, parser):
        """ define command arguments """
        parser.add_argument('app', type=str, help='enter the name of the django app')
        parser.add_argument('--all', action='store_true', help='generate filtersets, serializers, viewsets, and urls')
        parser.add_argument('--filterset', action='store_true', help='generate filtersets and create filters.py')
        parser.add_argument('--serializer', action='store_true', help='generate serializers and create serializers.py')
        parser.add_argument('--url', action='store_true', help='generate urls and create urls.py')
        parser.add_argument('--viewset', action='store_true', help='generate viewsets and create viewsets.py')
        parser.add_argument('--output_path', type=str, default=None, help='path where files should be created')
        parser.add_argument('--output_file', type=str, default=None,
                            help='fully qualified name of file to be created; only use this when generating one file')
        parser.add_argument('--filterset_template', type=str, default=None,
                            help='path to Jinja template used to create filtersets')
        parser.add_argument('--serializer_template', type=str, default=None,
                            help='path to Jinja template used to create serializers')
        parser.add_argument('--url_template', type=str, default=None, help='path to Jinja template used to create urls')
        parser.add_argument('--viewset_template', type=str, default=None, help='path to Jinja template used to create viewsets')

    def handle(self, *args, **options):
        """ command entry point """
        if options['app'] not in settings.INSTALLED_APPS:
            raise CommandError(f'\'{options["app"]}\' is not an available application in this project')

        self.app = options['app']
        self.model_list = self.get_model_list()
        files_created_list = []

        # build filtersets file
        if options['filterset'] or options['all']:
            files_created_list.append(
                self.build_filters(output_path=options['output_path'],
                                   output_file=options['output_file'],
                                   template_file=options['filterset_template'])
            )

        # build serializers file
        if options['serializer'] or options['all']:
            files_created_list.append(
                self.build_serializers(output_path=options['output_path'],
                                       output_file=options['output_file'],
                                       template_file=options['serializer_template'])
            )

        # build urls file
        if options['url'] or options['all']:
            files_created_list.append(
                self.build_urls(output_path=options['output_path'],
                                output_file=options['output_file'],
                                template_file=options['url_template'])
            )

        # build viewsets file
        if options['viewset'] or options['all']:
            files_created_list.append(
                self.build_viewsets(output_path=options['output_path'],
                                    output_file=options['output_file'],
                                    template_file=options['viewset_template'])
            )

        for item in files_created_list:
            self.stdout.write(self.style.SUCCESS(f'generated {item}'))

    def get_model_list(self):
        """ return a list of all models in application """
        app = apps.get_app_config(self.app)
        model_list = list(app.get_models())
        model_list.sort(key=lambda x: x.__name__)
        return model_list

    @staticmethod
    def get_model_field_names(model, exclude_list=()):
        """ return a list of field names for a given model """
        return [i.name for i in model._meta.fields if type(i).__name__ not in exclude_list]

    def build_filters(self, output_path=None, output_file=None, template_file=None):
        """ build the filters.py file for a list of model names """
        try:
            if not template_file:
                template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             'drf_templates', 'filterset.jinja')

            if output_file:
                output_path = output_file
            elif not output_path:
                output_path = 'filtersets.py'
            elif os.path.isdir(output_path):
                output_path = f'{output_path}/filtersets.py'

            model_list = self.model_list
            for model in model_list:
                # check for GenericRelation
                generic_relation_list = []
                for name in dir(model):
                    if name in ['history', 'eav_values']:
                        continue
                    if type(getattr(model, name)) == ReverseGenericManyToOneDescriptor:
                        generic_relation_list.append(name)
                setattr(model, 'generic_relation_list', generic_relation_list)
                # check for JSONField
                for field in model._meta.fields:
                    if field.get_internal_type() in ['JSONField']:
                        setattr(model, 'has_json', True)
                        break

            data = {'model_list': model_list,
                    'app_name': self.app,
                    'models_file': 'models',
                    }
            with open(template_file) as f:
                template = Template(f.read(), trim_blocks=True)
            file_text = template.render(data)
            with open(output_path, 'w') as f:
                f.write(file_text)

            return output_path

        except Exception as err:
            self.stdout.write(self.style.ERROR(f'error generating filter: {err}'))

    def build_serializers(self, output_path=None, output_file=None, template_file=None):
        """ build the serializers.py file for a list of model names """
        try:
            if not template_file:
                template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             'drf_templates', 'serializer.jinja')

            if output_file:
                output_path = output_file
            elif not output_path:
                output_path = 'serializers.py'
            elif os.path.isdir(output_path):
                output_path = f'{output_path}/serializers.py'

            model_list = self.model_list
            for model in model_list:
                for field in model._meta.fields:
                    if field.get_internal_type() in ['ForeignKey', 'OneToOneField']:
                        setattr(model, 'has_related', True)
                        break

            data = {'model_list': model_list,
                    'app_name': self.app,
                    'models_file': 'models',
                    'file_path': output_path.replace(f'{self.app}/', '').replace('.py', ''),
                    }
            with open(template_file) as f:
                template = Template(f.read())
            file_text = template.render(data)
            with open(output_path, 'w') as f:
                f.write(file_text)

            return output_path

        except Exception as err:
            self.stdout.write(self.style.ERROR(f'error generating filter: {err}'))

    def build_viewsets(self, output_path=None, output_file=None, template_file=None):
        """ build the viewsets.py file for a list of model names """
        try:
            if not template_file:
                template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             'drf_templates', 'viewset.jinja')
            if output_file:
                output_path = output_file
            elif not output_path:
                output_path = 'viewsets.py'
            elif os.path.isdir(output_path):
                output_path = f'{output_path}/viewsets.py'

            model_list = self.model_list
            for model in model_list:
                for field in model._meta.fields:
                    if field.get_internal_type() in ['ForeignKey', 'OneToOneField']:
                        setattr(model, 'select_related', True)

            data = {'model_list': model_list,
                    'app_name': self.app,
                    'models_file': 'models',
                    'serializers_file': 'serializers',
                    'filtersets_file': 'filtersets',
                    'viewset_type': 'viewsets.ReadOnlyModelViewSet',
                    }

            with open(template_file) as f:
                template = Template(f.read())
            file_text = template.render(data)
            with open(output_path, 'w') as f:
                f.write(file_text)

            return output_path

        except Exception as err:
            self.stdout.write(self.style.ERROR(f'error generating filter: {err}'))

    def build_urls(self, output_path=None, output_file=None, template_file=None):
        """ build the urls.py file for a list of model names """
        try:
            if not template_file:
                template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             'drf_templates', 'urls.jinja')
            if output_file:
                output_path = output_file
            elif not output_path:
                output_path = 'urls.py'
            elif os.path.isdir(output_path):
                output_path = f'{output_path}/urls.py'

            data = {'import_models': 'my import statement here',
                    'model_list': self.model_list,
                    'app_name': self.app,
                    'viewset_file': 'viewsets',
                    }
            with open(template_file) as f:
                template = Template(f.read())
            file_text = template.render(data)
            with open(output_path, 'w') as f:
                f.write(file_text)

            return output_path

        except Exception as err:
            self.stdout.write(self.style.ERROR(f'error generating filter: {err}'))
