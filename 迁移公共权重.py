self.model = BertForTokenClassificationCtr.from_pretrained(BertBase,config=config,num_labels=len(label_list),label_to_id=data['train'].label_to_id)
train_writer.write("model init from Pretrained Model, without checkpoint\n")

if checkpoint_path:
    checkpoint_model = torch.load(checkpoint_path)
    # for name, params in self.model.named_parameters():
    #     print(f'原模型参数：{name}')
    counter = 1
    for name, params in self.model.named_parameters():
    # print(f'目标模型参数：{name}')
        if 'bert' in name:  # 仅仅迁移bert参数
            self.model.state_dict()[name].copy_(checkpoint_model[name])
            counter+=1
        # self.model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    train_writer.write("loaded checkpoint from: "+checkpoint_path+"\n")
    print(f"加载成功，加载了{counter}个参数\n")
    train_writer.write(f"加载成功，加载了{counter}个参数\n")