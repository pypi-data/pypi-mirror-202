def list_to_html_ul(string_list):
    ul_start = "<ul>"
    ul_end = "</ul>"
    li_elements = ""

    for string in string_list:
        li_elements += f"<li>{string}</li>"

    html_ul = ul_start + li_elements + ul_end
    return html_ul
