def install():
    """
    pip install torch==2.3 torchvision==0.18
    pip install lightning==2.3
    """

def example1():
    """
    import torch
    import torchvision
    from torch.autograd import Variable
    from torchvision import datasets, transforms
    import os            # os包集成了一些对文件路径和目录进行操作的类
    import matplotlib.pyplot as plt
    import time


    # 读取数据
    data_dir = 'C:/Users/17865/Desktop/超声医疗/sjb的数据集/Data'
    data_transform = {x:transforms.Compose([transforms.Scale([64,64]),
                                        transforms.ToTensor()]) for x in ['train', 'valid']}   # 这一步类似预处理
    image_datasets = {x:datasets.ImageFolder(root = os.path.join(data_dir,x),
                                            transform = data_transform[x]) for x in ['train', 'valid']}  # 这一步相当于读取数据
    dataloader = {x:torch.utils.data.DataLoader(dataset = image_datasets[x],
                                            batch_size = 4,
                                            shuffle = True) for x in ['train', 'valid']}  # 读取完数据后，对数据进行装载

    # 模型搭建
    class Models(torch.nn.Module):
        def __init__(self):
            super(Models, self).__init__()
            self.Conv = torch.nn.Sequential(
                torch.nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
                torch.nn.ReLU(),
                torch.nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
                torch.nn.ReLU(),
                torch.nn.MaxPool2d(kernel_size=2, stride=2),

                torch.nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
                torch.nn.ReLU(),
                torch.nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
                torch.nn.ReLU(),
                torch.nn.MaxPool2d(kernel_size=2, stride=2))

            self.Classes = torch.nn.Sequential(
                torch.nn.Linear(16 * 16 * 256, 512),
                torch.nn.ReLU(),
                torch.nn.Dropout(p=0.5),
                torch.nn.Linear(512, 3))

        def forward(self, inputs):
            x = self.Conv(inputs)
            x = x.view(-1, 16 * 16 * 256)
            x = self.Classes(x)
            return x

    model = Models()
    print(model)
    '''
    # 保存和加载整个模型
    torch.save(model, 'model.pth')
    model_1 = torch.load('model.pth')
    print(model_1)

    # 仅保存和加载模型参数
    torch.save(model.state_dict(), 'params.pth')
    dic = torch.load('params.pth')
    model.load_state_dict(dic)
    print(dic)
    '''
    loss_f = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.00001)

    Use_gpu = torch.cuda.is_available()
    if Use_gpu:
        model = model.cuda()

    epoch_n = 5
    time_open = time.time()

    for epoch in range(epoch_n):
        print('epoch {}/{}'.format(epoch, epoch_n - 1))
        print('-' * 10)

        for phase in ['train', 'valid']:
            if phase == 'train':
                # # 设置为True，会进行Dropout并使用batch mean和batch var
                print('training...')
                model.train(True)
            else:
                # # 设置为False，不会进行Dropout并使用running mean和running var
                print('validing...')
                model.train(False)

            running_loss = 0.0
            running_corrects = 0.0
            # 输出标号 和对应图片，下标从1开始
            for batch, data in enumerate(dataloader[phase], 1):
                X, Y = data
                # 将数据放在GPU上训练
                X, Y = Variable(X).cuda(), Variable(Y).cuda()
                # 模型预测概率
                y_pred = model(X)
                # pred，概率较大值对应的索引值，可看做预测结果，1表示行
                _, pred = torch.max(y_pred.data, 1)
                # 梯度归零
                optimizer.zero_grad()
                # 计算损失
                loss = loss_f(y_pred, Y)
                # 训练 需要反向传播及梯度更新
                if phase == 'train':
                    # 反向传播出现问题
                    loss.backward()
                    optimizer.step()
                # 损失和
                running_loss += loss.data.item()
                # 预测正确的图片个数
                running_corrects += torch.sum(pred == Y.data)
                # 训练时，每500个batch输出一次，训练loss和acc
                if batch % 500 == 0 and phase == 'train':
                    print('batch{},trainLoss:{:.4f},trainAcc:{:.4f}'.format(batch, running_loss / batch,
                                                                            100 * running_corrects / (4 * batch)))
            # 输出每个epoch的loss和acc
            epoch_loss = running_loss * 4 / len(image_datasets[phase])
            epoch_acc = 100 * running_corrects / len(image_datasets[phase])
            print('{} Loss:{:.4f} Acc:{:.4f}%'.format(phase, epoch_loss, epoch_acc))
    time_end = time.time() - time_open
    print(time_end)
    """

def example2():
    """
    import pytorch_lightning as pl
    import torch
    import torch.nn as nn
    from pytorch_lightning.loggers import TensorBoardLogger
    from torchvision.models import resnet50, resnet18
    import torch.optim as optim
    from pytorch_lightning.callbacks import ModelCheckpoint
    from torchvision import transforms
    import torch.utils.data as data
    from PIL import Image
    import pandas as pd

    ###模型定义模块
    class ResNet50(nn.Module):
        def __init__(self):
            super().__init__()
            self.modle = resnet50(pretrained=True, progress=True)
            self.classifier1 = nn.Sequential(
                nn.Linear(1000, 512),
                nn.BatchNorm1d(512),
                nn.ReLU(),
                nn.Linear(512, 2)
            )
            self.classifier2 = nn.Sequential(
                nn.Linear(1000, 512),
                nn.BatchNorm1d(512),
                nn.ReLU(),
                nn.Linear(512, 9)
            )

        def forward(self, imgs):
            return self.classifier1(self.modle(imgs)), self.classifier2(self.modle(imgs))
    
    class CVModule(pl.LightningModule):
        def __init__(self) -> None:
            super().__init__()
            self.save_hyperparameters()
            self.modle = resnet18()
            self.loss = nn.CrossEntropyLoss()
            self.example_input_array = torch.zeros((1, 3, 32, 32), dtype=torch.float32)

        def forward(self, imgs):
            return self.modle(imgs)

        def configure_optimizers(self):
            optimizer = None
            scheduler = None
            optimizer = optim.AdamW(self.parameters(), lr=0.0001)

            return [optimizer]

        def training_step(self, batch, batch_idx):
            imgs, labels = batch
            preds = self.modle(imgs)
            loss = 0.5 * self.loss(preds[0], labels[0]) + 0.5 * self.loss(preds[1], labels[1])### 0.5*sex_loss + 0.5*age_loss
            acc = 0.5 * (preds[0].argmax(dim=-1) == labels[0]).float().mean() + 0.5 * (preds[1].argmax(dim=-1) == labels[1]).float().mean()
            self.log("train_acc", acc, on_step=True)
            self.log("train_loss", loss, on_step=True)
            return loss

        def validation_step(self, batch, batch_idx):
            imgs, labels = batch
            preds = self.modle(imgs)
            loss = 0.5 * self.loss(preds[0], labels[0]) + 0.5 * self.loss(preds[1], labels[1])
            acc = 0.5 * (preds[0].argmax(dim=-1) == labels[0]).float().mean() +  0.5 * (preds[1].argmax(dim=-1) == labels[1]).float().mean()
            self.log("val_acc", acc, on_step=True)
            self.log("val_loss", loss, on_step=True)

        @staticmethod
        def prepare_picture(img):
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
            img = Image.open(img).convert('RGB')
            img = transform(img)
            return img.unsqueeze(0)
    
    ###数据加载模块
    class MydataSet(data.Dataset):
        def __init__(self, path, label_path, transform):
            super(MydataSet, self).__init__()
            self.path = path
            self.label_path = label_path
            self.transform = transform
            self.imgs = self._get_images()
            # self.labels = self._get_labels()

        def __len__(self):
            return len(self.imgs[0])

        def __getitem__(self, item):
            img = self.imgs[0][item]
            img = Image.open(img).convert('RGB')
            img = self.transform(img)
            label = self.imgs[1][item]
            return img, label

        def _get_images(self): ##只训练性别和年龄的这两个识别器
            df = pd.read_csv(self.label_path)
            indexMap1 = {n: i for i, n in enumerate(sorted(df["gender"].unique()))}
            indexMap2 = {n: i for i, n in enumerate(sorted(df["age"].unique()))}
            print(indexMap1)
            print(indexMap2)
            labels1 = df["gender"].to_list()
            labels2 = df["age"].to_list()
            labels =  [(indexMap1[i], indexMap2[j]) for i, j in zip(labels1, labels2)]
            imgs = [self.path + i for i in df["file"].to_list()]
            return imgs, labels

        def _get_labels(self, item):
            return self.imgs[1][item]
    
    ###模型训练模块
    checkpoint_callback = ModelCheckpoint(
        monitor='val_loss',
        dirpath='./modle/',
        filename='model-{epoch:02d}-{val_loss:.2f}' 
    )
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                            std=[0.229, 0.224, 0.225])
    ])
    mydata = MydataSet(
        "datas/pictures/fairface-img-margin025-trainval/train",
        "datas/pictures/fairface-img-margin025-trainval/fairface_label_train.csv",
        transform
    )
    print(len(mydata))
    valdata = MydataSet(
        "datas/pictures/fairface-img-margin025-trainval/val",
        "datas/pictures/fairface-img-margin025-trainval/fairface_label_val.csv",
        transform
    )
    train_loader = data.DataLoader(mydata, batch_size=16, shuffle=True, drop_last=False, pin_memory=True, num_workers=8)
    val_loader = data.DataLoader(valdata, batch_size=16, shuffle=False, drop_last=False, pin_memory=True, num_workers=8)
    model = CVModule()
    logger = TensorBoardLogger("logs/lightning_logs", name="test")
    trainer = pl.Trainer(max_epochs=2, accelerator='cpu', devices=1, logger=logger, callbacks=[checkpoint_callback])

    trainer.fit(model, train_loader, val_loader)
    """
