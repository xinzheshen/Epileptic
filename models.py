import torch
from torch import nn
from torch.nn import functional as F


class DCNN(nn.Module):
    def __init__(self, n_conv, input_init_channel, output_channel):
        super(DCNN, self).__init__()
        self.n_conv = n_conv
        self.input_init_channel = input_init_channel
        self.output_channel = output_channel
        self.convolutions = nn.ModuleList()
        self.pool = torch.nn.MaxPool2d(2)
        for i in range(self.n_conv):
            if i == 0:
                conv_layer = nn.Sequential(
                    nn.Conv2d(self.input_init_channel, self.output_channel, (2, 2)),
                    nn.BatchNorm2d(self.output_channel))
            else:
                conv_layer = nn.Sequential(
                    nn.Conv2d(self.output_channel, self.output_channel, (2, 2)),
                    nn.BatchNorm2d(self.output_channel))
            self.convolutions.append(conv_layer)

    def forward(self, x):
        # x ： (B, 1, 1280, 23)
        for i in range(self.n_conv):
            x = F.relu(self.convolutions[i](x))
            if i < self.n_conv - 1:
                x = self.pool(x)

        # print("size after DCNN: ", x.size())
        # size after DCNN:  torch.Size([B, 32, 158, 1])
        return x


class SeizurePredict(nn.Module):
    def __init__(self):
        super(SeizurePredict, self).__init__()
        self.n_conv = 4
        self.input_init_channel = 1
        self.output_channel_for_conv = 32
        self.output_D_for_lstm = 20

        self.dcnn = DCNN(self.n_conv, self.input_init_channel, self.output_channel_for_conv)

        # TODO add dropout for lstm
        self.lstm = nn.LSTM(self.output_channel_for_conv, int(self.output_D_for_lstm / 2), 1,
                            batch_first=True, bidirectional=True)

    def forward(self, x):
        x = self.dcnn(x)
        x = x.squeeze().permute(0, 2, 1)
        output, _ = self.lstm(x)
        output = output.permute(0, 2, 1)
        # print("size after BiLSTM: ", output.size())
        # size after BiLSTM:  torch.Size([B, 20, 158])
        # should calculate mean value of last time_step result?
        return torch.sigmoid(torch.mean(output[:, :, -1], 1))