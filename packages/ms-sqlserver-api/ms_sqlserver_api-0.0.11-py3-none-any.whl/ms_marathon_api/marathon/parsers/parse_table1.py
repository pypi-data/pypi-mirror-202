def build_table1_export_query(data):
    values = []
    for row in data:
        values.append(f"('{row[0]}','{row[1]}')")

    return ",".join(values)
