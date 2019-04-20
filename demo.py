from lib import log
from lib import spider
from lib import helper

if __name__ == '__main__':
    # Define log file location
    log.set_custom_log_info('tmp/error.log')

    # SSL or HTTPS ISSUE
    helper.verify_https_issue()

    # create scraping object
    tnw_scrap = spider.Tnw(spider.url_tnw, log)
    bb_scrap = spider.Bb(spider.url_bb, log)

    # checking if we should redownload from url or not
    if helper.check_cache(spider.raw_html_tnw, spider.CACHE):
        tnw_scrap.retrieve_webpage()

    tnw_scrap.read_webpage_from_html()
    tnw_scrap.convert_data_to_bs4()
    #tnw_scrap.print_beautiful_soup()
    tnw_html_text = tnw_scrap.parse_soup_to_simple_html()

    # checking if we should redownload from url or not
    if helper.check_cache(spider.raw_html_bb, spider.CACHE):
        bb_scrap.retrieve_webpage()

    bb_scrap.read_webpage_from_html()
    bb_scrap.convert_data_to_bs4()
    #bb_scrap.print_beautiful_soup()
    bb_html_text = bb_scrap.parse_soup_to_simple_html()


    html_text = [tnw_html_text, bb_html_text]
    spider.write_webpage_as_html(data = html_text)
