from .parsers import OpenGraph, JSONLD, ItemProp, MetaProp, LinkCanonicalProp, TitleTag, URLParser, LastChanceParser
from bs4 import BeautifulSoup
from ..models import AnnotationTarget
from urllib.parse import urlparse
import requests


class RequestParser:
    def __init__(self):
        self.parsers = [
            JSONLD(),
            MetaProp(),
            OpenGraph(),
            TitleTag(),
            LinkCanonicalProp(),
            ItemProp(),
            URLParser(),
            LastChanceParser()

        ]

    def parse(self, target_url, target_html, target_content_type):
        annotation_target = AnnotationTarget()
        parse_valid = False
        if "text/html" in target_content_type or "application/json" in target_content_type \
                or "application/ld+json" in target_content_type or "text/plain" in target_content_type:
            beautiful_soup_document = BeautifulSoup(target_html, "html.parser")
            for parser in self.parsers:
                parser_parse_valid = parser.parse(annotation_target, target_url, beautiful_soup_document,
                                                  parse_valid)
                parse_valid = parse_valid or parser_parse_valid
        else:
            parsed_url = urlparse(target_url)
            filename = parsed_url.path.split("/")[-1]
            annotation_target.title = filename
            response = requests.head(target_url)
            last_modified = None
            if "Last-Modified" in response.headers :
                last_modified = response.headers.get("Last-Modified")
            elif "last-modified" in response.headers:
                last_modified = response.headers.get("last-modified")

            if last_modified is not None:
                jsonld_parser = JSONLD()
                annotation_target.publication_date = jsonld_parser.try_strptimeAll(last_modified)

            if "application/pdf" in target_content_type:
                parse_valid = True
            else:
                if "image/jpeg" in target_content_type:
                    annotation_target.image  = target_url
                    parse_valid = True
                elif "image/gif" in target_content_type:
                    annotation_target.image = target_url
                    parse_valid = True
                elif "image/png" in target_content_type:
                    annotation_target.image = target_url
                    parse_valid = True
                elif "image/svg" in target_content_type:
                    annotation_target.image = target_url
                    parse_valid = True
                else:
                    parse_valid = True

        return parse_valid, annotation_target
