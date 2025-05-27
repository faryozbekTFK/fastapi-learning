def dict_to_sql_query_string(model, id):
    model_to_dict = model.dict(exclude_unset=True)

    fields = ", ".join([f"{field}=%s" for field in model_to_dict.keys()])
    print(f"---- {fields}")
    values = list(model_to_dict.values())
    values.append(id)
    return {"str": fields, "values": values}
