from novadata_utils.models import NovadataModel

# ChoicesField é um CharField com choices
props_dict = {
    # Admin props
    "list_display": [
        "BigAutoField",
        "BooleanField",
        "CharField",
        "DateField",
        "DateTimeField",
        "DecimalField",
        "ForeignKey",
        "IntegerField",
        "PositiveIntegerField",
        "ChoicesField",
    ],
    "search_fields": [
        "BigAutoField",
        "CharField",
        "DateField",
        "DateTimeField",
        "DecimalField",
        "IntegerField",
        "PositiveIntegerField",
        "ChoicesField",
    ],
    "list_filter": [
        "BooleanField",
        "DateField",
        "DateTimeField",
        "ForeignKey",
        "ChoicesField",
    ],
    "autocomplete_fields": [
        "ForeignKey",
    ],
    "list_select_related": [
        "ForeignKey",
    ],
    "filter_horizontal": [
        "ManyToManyField",
    ],
    # Generic props
    "foreign_keys": [
        "ForeignKey",
    ],
    "many_to_many": [
        "ManyToManyField",
    ],
    # Viewset props
    "filterset_fields": [
        "BooleanField",
        "DateField",
        "DateTimeField",
        "ForeignKey",
        "ChoicesField",
    ],
    "ordering_fields": [
        "BigAutoField",
        "CharField",
        "DateField",
        "DateTimeField",
        "DecimalField",
        "IntegerField",
        "PositiveIntegerField",
        "BooleanField",
        "ForeignKey",
        "ChoicesField",
    ],
    # Especific props
    "choices_fields": [
        "ChoicesField",
    ],
}


def get_fields(model):
    """get_fields personalizado."""
    parents = model._meta.parents
    if parents:
        first_parent = next(iter(parents))
        is_subclass = issubclass(NovadataModel, first_parent)

        if is_subclass:
            super_fields_whinout_id = list(first_parent._meta.fields)[1:]
            fields = list(model._meta.get_fields())
            duplicated_fields = filter(
                lambda field: field in super_fields_whinout_id,
                super_fields_whinout_id,
            )
            list(map(lambda field: fields.remove(field), duplicated_fields))

            new_fields = fields + super_fields_whinout_id
            return new_fields

    return model._meta.get_fields()


def get_field_type(field):
    """Retorna o tipo de um campo."""
    field_type = field.get_internal_type()
    is_choices = (
        hasattr(field, "choices")
        and field.choices
        and field_type == "CharField"
    )

    if is_choices:
        field_type = "ChoicesField"

    return field_type


def get_prop(model, prop, str=False):
    """
    Retorna uma lista de campos de um model baseado em uma propriedade.

    Exemplo:
        get_prop(model, "list_display") retorna todos os campos que podem ser
        exibidos na listagem do admin. Que são:
            "BigAutoField",
            "BooleanField",
            "CharField",
            "DateField",
            "DateTimeField",
            "DecimalField",
            "ForeignKey",
            "IntegerField" e
            "PositiveIntegerField".
    """
    props = []
    fields = get_fields(model)
    for field in fields:
        field_type = get_field_type(field)

        is_original_field = not hasattr(field, "field")
        if field_type in props_dict[prop] and is_original_field:
            if str:
                field_str = f'"{field.name}",'
                props.append(field_str)
            else:
                props.append(field.name)

    return props
