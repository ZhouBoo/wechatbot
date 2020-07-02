#! /usr/bin/env python2.7
#coding=utf-8

# import logging
from gensim import corpora, models, similarities
import jieba, jieba.analyse
from model import Message, Report, DBError

class WeekReporter(object):

    def __init__(self, name, next_week=None, title=None, desc=None):
        # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
        #     level=logging.INFO)
        self.name = name
        self.next_week = next_week
        self.title = title
        self.description = desc

    def create_report(self):
        """
        生成周报，使用 lsi 进行相似度判断，然后 text rank 进行关键词选取
        """
        jieba.analyse.set_stop_words('./stopwords.dat')
        messages = Message.query_weekly_message(self.name).all()
        tokenized = [jieba.analyse.extract_tags(note.message) \
            for note in messages]
        
        dictionary = corpora.Dictionary(tokenized)
        token_vectors = [dictionary.doc2bow(tokens) for tokens in tokenized]
        tfidf = models.TfidfModel(token_vectors)
        tfidf_vectors = tfidf[token_vectors]

        # 当前发现 lsi 的模型效果比 tf-idf 效果好
        # print list(enumerate(tfidf_vectors))
        # for token in tokenized:
        #     query_bow = dictionary.doc2bow(token)
        #     index = similarities.MatrixSimilarity(tfidf_vectors)
        #     sims = index[query_bow]
        #     print list(enumerate(sims))

        lsi = models.LsiModel(tfidf_vectors, \
            id2word=dictionary, num_topics=2)
        lsi_vector = lsi[tfidf_vectors]

        sim_set = set()
        record_group = []
        for idx, token in enumerate(tokenized):
            query_bow = dictionary.doc2bow(token)
            query_lsi = lsi[query_bow]
            index = similarities.MatrixSimilarity(lsi_vector)
            sims = index[query_lsi]
            sim_records = None
            records = []
            print(list(enumerate(sims)))
            for sim_idx, sim in enumerate(sims):
                # 如果已经添加到相似的数据中的话
                if sim_idx in sim_set:
                    continue
                elif idx == sim_idx:
                    # 比较的是自己的话先添加到 set 中
                    sim_records = sim_idx
                    sim_set.add(idx)
                    records.append(sim_records)
                elif sim > 0.85:
                    # 如果相似度高于 85%，则算为同一条记录
                    sim_set.add(sim_idx)
                elif sim > 0.65:
                    sim_set.add(sim_idx)
                    records.append(sim_idx)

            print('a round records = %s' % records)
            if records:
                record_group.append(records)
        print('group = %s, messages = %s' % (record_group, messages))
        messages, keywords = self._keyword(record_group, messages)
        result = self._build_report(messages, keywords)
        return result

    def _build_report(self, messages, keywords):
        """
        周报的构造方法

        Arguments:
            name {string} -- 谁的周报
            messages {[string]} -- 本周的所有根据相似度分好 group 的消息
            keywords {[string]} -- 每组分好 group 的关键字，用作日报头
        """
        try:
            report = u''
            for msgs, keyword in zip(messages, keywords):
                report += u'-%s %s\n' % (keyword, u'【100%】')
                for msg in msgs:
                    report += u'%s\n' % msg
            r_id = Report.create_report(self.name, report, \
                    self.next_week, self.title, self.description)
            if r_id:
                return u'创建周报成功，id = %s' % r_id
            return u'创建周报失败，确认是否已经存在'
        except DBError:
            return u'创建周报失败'

    def _keyword(self, indexs_list, messages):
        """
        返回原记录中 index list 中指定 index 文字集合的关键词。
        取前 3 个拼接。

        Arguments:
            text_lis {[int]} -- 需要在一起的 index 集合
            tokenized {[string]} -- 原文本记录
        """
        keywords = []
        result_messages = []
        for indexs in indexs_list:
            texts = []
            for index in indexs:
                print(index)
                texts.append(messages[index].message)
            message_text = ' '.join(texts)
            print(message_text)
            result_messages.append(texts)
            keywords.append(''.join( \
                jieba.analyse.textrank(message_text)[0:3]))
        return (result_messages, keywords)
