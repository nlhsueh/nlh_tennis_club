from django.template import Context, Template
from django.conf import settings
import django

settings.configure(
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }]
)
django.setup()

template = Template('{{ csrf_token }}')
context = Context({'csrf_token': 'my_raw_token_string_123'})
print(template.render(context))
