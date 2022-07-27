import re

from requesting_urls import get_html


def find_dates (html_string , output = None ) :
    """Finds all dates in a html string .

    The returned list is in the following format:
        - 1998/10/12
        - 1998/11/04
        - 1999/01/13

    The following formats are considered when searching:
        DMY: 13 Oct( ober ) 2020
        MDY: Oct( ober ) 13 , 2020
        YMD: 2020 Oct ( ober ) 13
        ISO: 2020 -10 -13

    Args:
        html_string (str): A string containing the html code for a wikipedia article
        output (str, optional): Filename, for writing results to file. Defaults to None.

    Returns:
        results (list): A list with all the dates found in Y/M/D
    """

    # defining regex for all the months
    jan = r"\b[jJ]an(?:uary)?\b"
    feb = r"\b[fF]eb(?:ruary)?\b"
    mar = r"\b[mM]ar(?:ch)?\b"
    apr = r"\b[aA]pr(?:il)?\b"
    may = r"\b[mM]ay\b"
    apr = r"\b[aA]pr(?:il)?\b"
    jun = r"\b[jJ]un(?:e)?\b"
    jul = r"\b[jJ]ul(?:y)?\b"
    aug = r"\b[aA]ug(?:ust)?\b"
    sep = r"\b[sS]ep(?:tember)?\b"
    oct = r"\b[oO]ct(?:ober)?\b"
    nov = r"\b[nN]ov(?:ember)?\b"
    dec = r"\b[dD]ec(?:ember)?\b"

    # defining regex for day, month and year
    day = rf"[0-9]{{1,2}}"
    month = rf"(?:{jan}|{feb}|{mar}|{apr}|{may}|{jun}|{jul}|{aug}|{sep}|{oct}|{nov}|{dec})"
    year = rf"[0-9]{{4}}"

    iso_month_format = r"\b(?:0\d|1[0-2])\b" # special iso case

    # defining DMY format
    dmy = rf"{day}\s{month}\s{year}"
    mdy = rf"{month}\s{day},\s{year}"
    ymd = rf"{year}\s{month}\s{day}"
    iso = rf"{year}-{iso_month_format}-{day}"

    # finding all date formats matches using re.findall
    dates_dmy = re.findall(rf"{dmy}", html_string)
    dates_mdy = re.findall(rf"{mdy}", html_string)
    dates_ymd = re.findall(rf"{ymd}", html_string)
    dates_iso = re.findall(rf"{iso}", html_string)

    results = []
    month_list = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]

    # reformat DMY as Y/M/D and append the result to the results list
    for date_element in dates_dmy:
        month_tmp = re.findall(rf"{month}", date_element)[0]
        for i, month_re in enumerate(month_list):
            if re.match(rf"{month_re}", month_tmp):
                month_num = i+1
                break
        date_element = re.sub(rf"({day})\s({month})\s({year})", rf"\3/{month_num}/\1", date_element)
        results.append(date_element)

    # reformat MDY as Y/M/D and append the result to the results list
    for date_element in dates_mdy:
        month_tmp = re.findall(rf"{month}", date_element)[0]
        for i, month_re in enumerate(month_list):
            if re.match(rf"{month_re}", month_tmp):
                month_num = i+1
                break
        date_element = re.sub(rf"({month})\s({day}),\s({year})", rf"\3/{month_num}/\2", date_element)
        results.append(date_element)

    # reformat YMD as Y/M/D and append the result to the results list
    for date_element in dates_ymd:
        month_tmp = re.findall(rf"{month}", date_element)[0]
        for i, month_re in enumerate(month_list):
            if re.match(rf"{month_re}", month_tmp):
                month_num = i+1
                break
        date_element = re.sub(rf"({year})\s({month})\s({day})", rf"\1/{month_num}/\3", date_element)
        results.append(date_element)

    # reformat ISO as Y/M/D and append the result to the results list
    for date_element in dates_iso:
        date_element = date_element.replace("-", "/")
        results.append(date_element)
    
    # write the result to file if the argument is specified
    if output != None:
        with open(output, 'w') as outfile:
            for date in results:
                outfile.write(date + '\n')

    return results


if __name__ == '__main__':
    folder = "collect_dates_regex/"

    rowling_url = 'https://en.wikipedia.org/wiki/J._K._Rowling'
    feynman_url = 'https://en.wikipedia.org/wiki/Richard_Feynman'
    rosling_url = 'https://en.wikipedia.org/wiki/Hans_Rosling'

    rowling_html = get_html(rowling_url)
    feynman_html = get_html(feynman_url)
    rosling_html = get_html(rosling_url)

    rowling_dates = find_dates(rowling_html, output=folder+"rowling_dates.txt")
    feynman_dates = find_dates(feynman_html, output=folder+"feynman_dates.txt")
    rosling_dates = find_dates(rosling_html, output=folder+"rosling_dates.txt")
