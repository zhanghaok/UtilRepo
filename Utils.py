class Utils:
    def __init__():
        pass
        
    def remove_html(line):
        """
        正则去掉HTML标签元素
        """
        reg = re.compile('<[^>]*>')
        content = reg.sub('', line)
        return content.strip()
    
    def logger():
        """
        日志记录管理
        """
        import logging
        import datetime

        #第一步 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        now_date  = datetime.datetime.now()
        now_date = now_date.strftime("%Y-%m-%d_%H-%M-%S")
        #第2步，创建一个handler，用于写入日志文件
        file_handler = logging.FileHandler("./log/"+str(now_date)+".log",mode='w')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
            
        )
        # 添加handler到logger中
        logger.addHandler(file_handler)

        # 第三步，创建一个handler，用于输出到控制台
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.INFO)
        # console_handler.setFormatter(
        #     logging.Formatter(
        #         fmt='%(asctime)s - %(levelname)s: %(message)s',
        #         datefmt='%Y-%m-%d %H:%M:%S')  
        # )
        # logger.addHandler(console_handler)
        # logger.critical('this is a logger critical message')

        logger.info("XXXX模型")
        
     def extract_entity(chars,tags):
        """
        根据标签和原始句子返回，对应的实体
        chars：一句话 "CLS  张    三   是我们  班    主   任   SEP"
        tags：标签列表[O   B-LOC,I-LOC,O,O,O,B-PER,I-PER,i-PER,O]
        返回一段话中的实体
        """
        result = []
        pre = ''
        w = []
        for idx,tag in enumerate(tags):
            if not pre:
                if tag.startswith('B'):
                    pre = tag.split('-')[1] #pre LOC
                    w.append(chars[idx])#w 张
            else:
                if tag == f'I-{pre}': #I-LOC True
                    w.append(chars[idx]) #w 张三
                else:
                    result.append([w,pre])
                    w = []
                    pre = ''
                    if tag.startswith('B'):
                        pre = tag.split('-')[1]
                        w.append(chars[idx])
        return [[''.join(x[0]),x[1]] for x in result]
        
    def read_CoNLL(filename):
        """
        读取CoNLL文件，返回句子和标签集合
        """
        X, y = [], []
        labels = []
        with open(filename, 'r', encoding='utf-8') as f:
            x0, y0 = [], []
            for line in f:
                data = line.strip()
                if data:
                    x0.append(data.split()[0])
                    y0.append(data.split()[1])
                else:
                    if len(x0)!=0:
                        X.append(x0)
                        y.append(y0)
                    x0, y0 = [], []
            if len(x0)!=0:
                X.append(x0)
                y.append(y0)
        return X, y
     
    def encode_plus(tokenizer, sequence):
        """
        位一句话编码
        """
        # sequence: ["中", "国", "的", "首", "都", "是", "北", "京"]
        input_ids = []
        pred_mask = []
        # wordpiece 只取第一个sub token预测
        for word in sequence:
            sub_tokens_ids = tokenizer.encode(word, add_special_tokens=False)
            input_ids = input_ids + sub_tokens_ids
            pred_mask = pred_mask + [1] + [0 for i in range(len(sub_tokens_ids)-1)]
            
        assert len(input_ids) == len(pred_mask)
        return input_ids, pred_mask

    def sequence_padding_for_bert(X, y, tokenizer, labels, max_len):
        """
        为一个批量的句子编码
        """
        input_ids_list = []
        attention_mask_list = []
        pred_mask_list = []
        input_labels_list = []

        cls_id = tokenizer.convert_tokens_to_ids("[CLS]")
        sep_id = tokenizer.convert_tokens_to_ids("[SEP]")
        pad_id = tokenizer.convert_tokens_to_ids("[PAD]")
        
        for i, sequence in tqdm(enumerate(X)):
            # get input_ids, pred_mask
            input_ids, pred_mask = encode_plus(tokenizer, sequence)
            attention_mask = [1] * len(input_ids)

            # padding
            input_ids = [cls_id] + input_ids[:max_len-2] + [sep_id] + [pad_id]* (max_len - len(input_ids) - 2) 
            pred_mask = [0] + pred_mask[:max_len-2] + [0] + [0]* (max_len - len(pred_mask) - 2)
            
            # get attention_mask
            attention_mask = [1] + attention_mask[:max_len-2] + [1] + [0]* (max_len - len(attention_mask) - 2)

            # get input_labels
            sequence_labels = [labels.index(l) for l in y[i][:sum(pred_mask)]]
            sequence_labels = sequence_labels[::-1]
            input_labels = [sequence_labels.pop() if pred_mask[i]==1 else labels.index("O") for i in range(len(pred_mask))]
            
            input_ids_list.append(input_ids)
            attention_mask_list.append(attention_mask)
            pred_mask_list.append(pred_mask)
            input_labels_list.append(input_labels)

        return torch.LongTensor(input_ids_list), \
                torch.ByteTensor(attention_mask_list), \
                torch.ByteTensor(pred_mask_list), \
                torch.LongTensor(input_labels_list)
    def q():
        pass