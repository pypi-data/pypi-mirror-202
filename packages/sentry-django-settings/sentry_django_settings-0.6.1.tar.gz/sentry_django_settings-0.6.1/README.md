# DEPRECATED

This package is no longer being supported. While it should still work for the foreseeable feature,
we recommend using the official [sentry-sdk](https://github.com/getsentry/sentry-python)
package and following their documentation on
[integrating with Django](https://docs.sentry.io/platforms/python/guides/django/).

Read [the announcement issue](https://github.com/enervee/sentry-django-settings/issues/12) for more information.

# Sentry Django Settings

This is a package for Django that allows you to add Sentry integration by adding a Django setting.

## Installation

`pip install sentry_django_settings`

Add `sentry_django_settings.apps.Sentry` to your `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    # ...
    'sentry_django_settings.apps.Sentry',
    # ...
]
```

You can now add the `SENTRY` setting to your `settings.py` file:

```python
SENTRY = {
    'enabled': True,
    'dsn': "https://2e2ac79f64d34e4b85c3a3173e343464@sentry.mysite.com/5",
    'environment': "dev",  # Optional
    'release': '1.0',  # Optional
}
```

`enabled` is a boolean if Sentry should be initialized or not.

To find the DSN in Sentry:

- Go to the project settings in Sentry
- Under `Data`, select `Error Tracking`
- Click "Get your DSN."
- Use the "Public DSN" in all cases.

The `environment` should be appropriate to environment where the server will be running.

All other keys passed into the settings are forwarded onto the Sentry SDK `init` method.
See [their documentation](https://docs.sentry.io/platforms/python/configuration/options/) for more information.
