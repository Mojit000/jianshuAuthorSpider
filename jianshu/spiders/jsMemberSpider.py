# -*- coding: utf-8 -*-
import scrapy
from jianshu.items import ArticleItem

class JsmemberspiderSpider(scrapy.Spider):
    name = "jsMemberSpider"
    # allowed_domains = ["jianshu"]
    jianshu = 'http://www.jianshu.com'
    start_urls = ['http://www.jianshu.com/u/54b5900965ea?order_by=shared_at&page=1', ]
    
    article_all = []

    start_url = 'http://www.jianshu.com/u/54b5900965ea?order_by=shared_at&page={}'
    start_page = 1
    userID = '54b5900965ea'
    pageNumber = 1
    stop_url = 'http://www.jianshu.com/u/{USERID}?order_by=shared_at&page={pageNumber}'.format(USERID = userID, pageNumber = pageNumber)

    def parse(self, response):
        # 获取文章总数
        article_count = response.css(
            'body > div.container.person > div > div.col-xs-16.main > div.main-top > div.info > ul > li:nth-child(3) > div > a > p::text').extract_first()
        # 计算共分了多少页，每页9篇文章
        countPageNumber = int(int(article_count) / 9 + 0.5)
        # 获取文章列表
        articles = response.css('ul.note-list > li')
        for article in articles:
            articleItem = ArticleItem()
            # 获取作者名称
            articleItem['author_name'] = article.css('a.blue-link::text').extract_first()
            # author_name = article.css('a.blue-link::text').extract_first()
            # 获取作者的头像连接
            articleItem['author_image'] = 'http:' + article.css('div.author > a > img::attr(src)').extract_first()
            # author_image = 'http:' + article.css('div.author > a > img::attr(src)').extract_first()
            # 获取文章发布时间
            articleItem['article_release_time'] = article.css('div.name > span.time::attr(data-shared-at)').extract_first()
            article_release_time = article.css('div.name > span.time::attr(data-shared-at)').extract_first()
            # 获取标题
            articleItem['article_title'] = article.css('a.title::text').extract_first()
            # article_title = article.css('a.title::text').extract_first()
            # 获取文章描述 
            articleItem['article_desc'] = article.css('p.abstract::text').extract_first().strip()
            # article_desc = article.css('p.abstract::text').extract_first().strip()
            # 获取文章链接
            articleItem['article_link'] = JsmemberspiderSpider.jianshu + article.css('div.content > a::attr(href)').extract_first()
            # article_link = JsmemberspiderSpider.jianshu + article.css('div.content > a::attr(href)').extract_first()
            # 获取阅读量，回复量，喜欢人数，赞赏人数
            articleItem['read_count'] = article.css('div.meta > a')[0].css('::text').extract()[-1].strip()
            articleItem['reply_count'] = article.css('div.meta > a')[1].css('::text').extract()[-1].strip()
            articleItem['likeit_count'] = article.css('div.meta > span')[0].css('::text').extract_first().strip()
            articleItem['payit_count'] = article.css('div.meta > span')[1].css('::text').extract_first().strip() if len(article.css('div.meta > span'))>=2 else 0
            # read_count = article.css('div.meta > a')[0].css('::text').extract()[-1].strip()
            # reply_count = article.css('div.meta > a')[1].css('::text').extract()[-1].strip()
            # likeit_count = article.css('div.meta > span')[0].css('::text').extract_first().strip()
            # payit_count = article.css('div.meta > span')[1].css('::text').extract_first().strip() if len(article.css('div.meta > span'))>=2 else 0
            # yield {
            #     'author_name': author_name, 
            #     'author_image': author_image, 
            #     'article_release_time': article_release_time, 
            #     'article_title': article_title,
            #     'article_desc': article_desc,
            #     'article_link': article_link,
            #     'read_count': read_count, 
            #     'reply_count': reply_count, 
            #     'likeit_count': likeit_count, 
            #     'payit_count': payit_count,
            # }
            JsmemberspiderSpider.article_all.append(articleItem)
            yield articleItem
            # pages = (i for i in range(2, countPageNumber + 1))
            current_page = int(response.url.split('page=')[1])
            next_page = JsmemberspiderSpider.start_url.format(current_page + 1)
            # 爬虫结束的条件，如果当前页是最后一页
            if current_page == countPageNumber:
                next_page = None
            if next_page is not None:
                next_page = response.urljoin(next_page)
                # yield {
                # '爬取中：': next_page,
                # }
                yield scrapy.Request(next_page, callback=self.parse)
