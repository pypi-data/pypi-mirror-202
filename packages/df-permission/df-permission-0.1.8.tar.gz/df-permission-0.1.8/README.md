# DFPermission

### Installation
```text
pip install df-permission
```

### Configuration
```pycon
INSTALLED_APPS = [
    ...,
    'df_permission'
]
```

### Generate permissions
```text
./manage.py generate_df_permissions
```

### Attributes

`df_method`
- Method of action
- Valid values are `create`, `update`, `retrieve`, `list`, `destroy`

```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_method = 'create'
    ...
```

or

```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_method = DFMethods.CREATE
    ...
```

`df_model`
- Model

```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_model = MyModel
    ...
```

`df_fields`
- Fields

```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_fields = ['field1', 'field2', ...]
    ...
```

`df_permissions`
- Permissions
- type: `string`, `list`, `tuple`

```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_permissions = ['permission1', 'permission2', ...]
    ...
```

or

```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    df_permissions = 'permission1'
    ...
```

`df_allow_superuser`
- Allow superuser if value is True
- Type: `boolean`
- Default: `False`

### Methods

`get_df_permissions`
- Customize df_permissions

```pycon
class MyView(CreateAPIView):
    permission_classes = [DFPermission]
    
    def get_df_permissions(self):
        # write your logic code
        return # single permission or permissions
```

### How does it work?
First, find `df_permissions` attribute. If it 
does not exist, find `get_df_permissions` method. 
If it does not exist too, generate permissions.

First for this, collect fields that are permission 
required. Find `df_fields`, if it exist. Else get 
serializer class to get fields and get intersection
with model fields.

Then, generate required perms using fields and `df_method`.

Finally, user's permissions are checked.
