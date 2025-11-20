from requests import get
from regex import findall

response = get("https://github.com/Jah135")
page = response.text

a_tag_pattern = r"<a\s*([^>]+)>(.+)</a>"
attribute_pattern = r"([\w\-]+)\s*=\s*\"([^\"]*)\""
href_pattern = r"href\s*=\s*\"([^\"]*)\""
link_pattern = r"https?://(.+)"

tags = findall(a_tag_pattern, page)
attributes = findall(attribute_pattern, tags[8][0])

print(attributes, tags[8][0])

print(findall(href_pattern, page))