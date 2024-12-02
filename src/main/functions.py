

def generate_form_error(form):
    message = ""
    for field in form:
        if field.errors:
            message += f"{field.label}: {', '.join(field.errors)}\n"
    for err in form.non_field_errors():
        message += f"{err}\n"
    return message


